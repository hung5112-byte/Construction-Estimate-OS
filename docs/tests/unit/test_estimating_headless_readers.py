"""Headless readers run through a fake `claude` binary: prompt assembly, argv contract, output parsing, merge and RFI fold-in."""
import json
import os
import stat
from pathlib import Path

import pytest

from core.estimating import headless_readers as hr
from core.estimating import pipeline

REPO = Path(__file__).resolve().parents[3]
FIXTURE = REPO / "docs" / "tests" / "fixtures" / "sample-set-prairie-creek"

FAKE_RESULT = {
    "type": "result", "subtype": "success", "is_error": False, "duration_ms": 1200, "num_turns": 3,
    "result": "(structured)",
    "structured_output": {
        "lines": [
            {"division": "08", "item_code": "08-hm-door-single", "description": "HM single doors confirmed on the tiles", "qty": 8, "unit": "EA",
             "sheet": "A-101", "method": "vision", "confidence": 0.95, "tags": {"mark": "1"}},
            {"division": "10", "item_code": "10-fire-extinguisher-cabinet", "description": "FEC symbols seen on plan", "qty": 3, "unit": "EA",
             "sheet": "A-101", "method": "vision", "confidence": 0.7},
        ],
        "questions": [{"text": "Door 108 swings into the corridor on the plan but the schedule lists a LH hand — which governs?",
                       "citation": "A-101 tile r1c2 vs A-601", "severity": "WARN", "exposure": "1 leaf + hardware set"}],
        "tiles_read": ["renders/A-101-p1-overview.png", "renders/A-101-p1-tile-r0c0.png"],
    },
    "usage": {"input_tokens": 10, "output_tokens": 20}, "modelUsage": {"claude-fable-5": {"costUSD": 0.12}},
}


@pytest.fixture()
def fake_claude(tmp_path, monkeypatch):
    log = tmp_path / "fakelog"
    log.mkdir()
    (tmp_path / "result.json").write_text(json.dumps(FAKE_RESULT), encoding="utf-8")
    script = tmp_path / "claude"
    script.write_text("#!/bin/bash\n" f"printf '%s\\n' \"$@\" > '{log}/argv.txt'\n" f"cat > '{log}/stdin.txt'\n" f"cat '{tmp_path}/result.json'\n", encoding="utf-8")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-should-be-scrubbed")
    return script, log


@pytest.fixture()
def folder(tmp_path):
    f = pipeline.intake(tmp_path, FIXTURE, "Prairie Creek Bldg 2", "office-warehouse", "Plano", 2, render=False)
    pipeline.seed_takeoff(f)
    return f


def test_system_prompt_uses_vault_agent_and_skill():
    sp = hr.system_prompt(REPO, "architectural-lead")
    assert "Architectural Lead" in sp and "## Headless run — output contract" in sp
    assert "cards first" in sp.lower() or "Read the card" in sp        # drawing-reading skill protocol included
    assert "---\nid:" not in sp                                          # frontmatter stripped


def test_build_prompt_lists_sheets_seeds_and_cards(folder):
    prompt, stats = hr.build_prompt(folder, "architectural-lead")
    assert stats["sheets"] >= 3 and stats["seed_lines"] > 0 and stats["tiles"] == 0   # no renders in this fixture run
    assert "## Sheet A-101" in prompt and "## Sheet A-601" in prompt and "## Sheet S-101" not in prompt
    assert "(no overview rendered)" in prompt and "### Shadow card" in prompt
    mep, _ = hr.build_prompt(folder, "mep-lead")
    assert "## Sheet M-101" in mep and "## Sheet A-101" not in mep


def test_run_reader_argv_contract_and_output(folder, fake_claude):
    script, log = fake_claude
    res = hr.run_reader(folder, REPO, "architectural-lead", claude_bin=str(script))
    argv = (log / "argv.txt").read_text(encoding="utf-8").split("\n")
    assert argv[0] == "-p" and "--tools" in argv and argv[argv.index("--tools") + 1] == "Read"
    assert argv[argv.index("--allowedTools") + 1] == "Read" and "--json-schema" in argv and "--no-session-persistence" in argv
    assert json.loads(argv[argv.index("--json-schema") + 1]) == hr.LINE_SCHEMA
    assert "Architectural Lead" in argv[argv.index("--system-prompt") + 1]
    stdin = (log / "stdin.txt").read_text(encoding="utf-8")
    assert "## Sheet A-101" in stdin and "### Shadow card" in stdin
    assert res["lines"] == 2 and res["questions"] == 1 and res["tiles_read"] == 2
    out = json.loads(Path(res["file"]).read_text(encoding="utf-8"))
    assert out["lines"][0]["confidence"] == 0.8                          # vision confidence capped
    assert out["_meta"]["provider"] == "claude-cli" and out["_meta"]["num_turns"] == 3


def test_read_folder_merges_and_rfi_folds_questions(folder, fake_claude):
    script, log = fake_claude
    results = hr.read_folder(folder, REPO, readers=["architectural-lead"], claude_bin=str(script), parallel=False)
    assert results[0]["ledger_lines"] > 0
    led = json.loads((folder / "04-takeoff-ledger.json").read_text(encoding="utf-8"))
    items = led["items"] if isinstance(led, dict) else led
    fec = [i for i in items if i["item_code"] == "10-fire-extinguisher-cabinet" and i["method"] == "vision"]
    assert len(fec) == 1 and fec[0]["qty"] == 3                          # vision line kept next to the derived seed line
    doors = [i for i in items if i["item_code"] == "08-hm-door-single"]
    assert {i["method"] for i in doors} == {"schedule"} and sum(i["qty"] for i in doors) == 8   # schedule governs; the vision count confirmed it, never doubled it
    assert any("confirmed by vision" in (i.get("notes") or "") for i in doors)
    qs = pipeline.rfi(folder)
    mine = [q for q in qs if "reader" in q.tags]
    assert len(mine) == 1 and mine[0].severity == "WARN" and "architectural-lead" in mine[0].tags
    assert (folder / "05-clarification.md").exists()


def test_env_is_scrubbed_of_api_keys(folder, fake_claude, tmp_path):
    script, log = fake_claude
    script.write_text("#!/bin/bash\n" f"env | grep -c ANTHROPIC_API_KEY > '{log}/keycount.txt' || true\n" f"cat > /dev/null\n" f"cat '{tmp_path}/result.json'\n", encoding="utf-8")
    hr.run_reader(folder, REPO, "mep-lead", claude_bin=str(script))
    assert (log / "keycount.txt").read_text(encoding="utf-8").strip() == "0"


def test_dry_run_makes_no_call(folder, fake_claude):
    script, log = fake_claude
    res = hr.read_folder(folder, REPO, claude_bin=str(script), dry_run=True)
    assert all(r.get("dry_run") for r in res) and not (log / "argv.txt").exists()
    assert {r["reader"] for r in res} == {"civil-structural-lead", "architectural-lead", "mep-lead"}


def test_unknown_binary_fails_loudly(folder):
    with pytest.raises((RuntimeError, FileNotFoundError, OSError)):
        hr.run_reader(folder, REPO, "mep-lead", claude_bin="/nonexistent/claude")
    assert not os.environ.get("BD_OS_CLAUDE_BIN_TEST_LEAK")
