from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
CONFIG = Path(__file__).resolve().parents[1] / "templates" / "openrouter.config.json"


def load_script(name: str):
    script = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(f"agent_plugin_{name}", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


openrouter = load_script("openrouter.py")


import pytest


@pytest.fixture
def home(tmp_path: Path) -> Path:
    directory = tmp_path / "home"
    directory.mkdir()
    return directory


def test_storage_root_defaults_to_project_local_agents(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    args = type("Args", (), {"storage_root": None})
    config = json.loads(CONFIG.read_text())

    root = openrouter.storage_root(args, config)

    assert root == (tmp_path / ".agents").resolve()


def test_storage_root_accepts_absolute_and_home_paths(tmp_path, monkeypatch, home):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(home))
    args = type("Args", (), {"storage_root": Path("~/.agents")})
    config = json.loads(CONFIG.read_text())

    root = openrouter.storage_root(args, config)

    assert root == home / ".agents"


def test_storage_root_accepts_absolute_override(tmp_path):
    args = type("Args", (), {"storage_root": tmp_path / "global-agents"})

    root = openrouter.storage_root(args, {"storageRoot": ".agents"})

    assert root == tmp_path / "global-agents"
