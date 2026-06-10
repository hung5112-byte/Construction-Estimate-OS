import subprocess
import sys
from pathlib import Path


def test_onboard_creates_valid_vault(tmp_path):
    repo = Path(__file__).parent.parent.parent
    vault = tmp_path / "test-vault"

    result = subprocess.run(
        [sys.executable, str(repo / "scripts" / "onboard.py"),
         "--vault", str(vault), "--non-interactive"],
        capture_output=True, text=True,
    )

    assert result.returncode == 0, f"Failed: {result.stderr}"

    assert (vault / "00-Brain" / "strategy.md").exists()
    assert (vault / "00-Templates-Custom" / "README.md").exists()
    assert (vault / "01-Departments").exists()
    assert (vault / "02-Tasks").exists()
    assert (vault / ".vncoderc").exists()
    assert (vault / ".git").exists()


def test_onboard_with_pack_installs_dept(tmp_path):
    """The pack-install mechanism copies a pack's adds_departments into the vault."""
    repo = Path(__file__).parent.parent.parent
    vault = tmp_path / "v2"

    subprocess.run(
        [sys.executable, str(repo / "scripts" / "onboard.py"),
         "--vault", str(vault), "--non-interactive"],
        capture_output=True, text=True,
    )

    # Synthetic pack (no packs ship by default — the mechanism is what we test)
    pack_dir = tmp_path / "packs" / "testpack"
    dept_dir = pack_dir / "departments" / "06-test-dept"
    (dept_dir / "agents").mkdir(parents=True)
    (pack_dir / "pack.yaml").write_text(
        "name: Test Pack\ncode: testpack\nadds_departments:\n  - 06-test-dept\n",
        encoding="utf-8",
    )
    (dept_dir / "department.yaml").write_text(
        "code: 06-test-dept\nname_vn: Test Dept\ntier: 3\nagents: []\ndefault_speaker: ''\n",
        encoding="utf-8",
    )

    sys.path.insert(0, str(repo))
    from scripts.onboard import _install_pack
    _install_pack(pack_dir, vault)

    assert (vault / "01-Departments" / "06-test-dept").exists()
