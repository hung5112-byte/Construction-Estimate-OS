"""Test core.onboard library — pure Python API (no subprocess)."""
from __future__ import annotations

from core.onboard import onboard_vault


def test_onboard_creates_minimal_vault(tmp_path):
    vault = tmp_path / "test-vault"
    result = onboard_vault(vault_path=vault, packs=[], init_git=False)

    assert result["ok"] is True
    assert (vault / "00-Brain" / "strategy.md").exists()
    assert (vault / "00-Templates-Custom" / "README.md").exists()
    assert (vault / "01-Departments").exists()
    assert (vault / "02-Tasks").exists()
    assert (vault / ".vncoderc").exists()
    # Git init disabled
    assert not (vault / ".git").exists()


def test_onboard_with_pack_installs_pack_dept(tmp_path, monkeypatch):
    """Pack mechanism: a pack's adds_departments land in the vault (no packs ship by default)."""
    import shutil
    from pathlib import Path
    import core.onboard as onboard_mod

    # Build a minimal repo root: real vault-template + departments, plus a synthetic pack
    real_repo = Path(onboard_mod.REPO_ROOT)
    fake_repo = tmp_path / "repo"
    shutil.copytree(real_repo / "vault-template", fake_repo / "vault-template")
    shutil.copytree(real_repo / "departments", fake_repo / "departments")
    dept_dir = fake_repo / "packs" / "testpack" / "departments" / "06-test-dept"
    (dept_dir / "agents").mkdir(parents=True)
    (fake_repo / "packs" / "testpack" / "pack.yaml").write_text(
        "name: Test Pack\ncode: testpack\nadds_departments:\n  - 06-test-dept\n",
        encoding="utf-8",
    )
    (dept_dir / "department.yaml").write_text(
        "code: 06-test-dept\nname_vn: Test Dept\ntier: 3\nagents: []\ndefault_speaker: ''\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(onboard_mod, "REPO_ROOT", fake_repo)

    vault = tmp_path / "v"
    result = onboard_vault(vault_path=vault, packs=["testpack"], init_git=False)

    assert "testpack" in result["packs"]
    assert (vault / "01-Departments" / "06-test-dept").exists()


def test_onboard_with_unknown_pack_warns(tmp_path):
    vault = tmp_path / "v"
    result = onboard_vault(
        vault_path=vault, packs=["nonexistent"], init_git=False
    )

    assert result["ok"] is True
    assert any("nonexistent" in w for w in result["warnings"])


def test_onboard_idempotent(tmp_path):
    """Re-running onboard on existing vault is safe."""
    vault = tmp_path / "v"
    onboard_vault(vault_path=vault, packs=[], init_git=False)
    result = onboard_vault(vault_path=vault, packs=[], init_git=False)

    assert result["ok"] is True
