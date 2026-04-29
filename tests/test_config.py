import pytest
from scoper.config import (
    load_config, save_config, get_config_value, set_config_value,
    init_config, DEFAULT_CONFIG
)


@pytest.fixture
def mock_config_path(monkeypatch, tmp_path):
    config_dir = tmp_path / ".config" / "scoper"
    config_file = config_dir / "config.json"

    monkeypatch.setattr('scoper.config.get_config_path', lambda: config_file)
    return config_file


def test_load_config_default(mock_config_path):
    config = load_config()
    assert config == DEFAULT_CONFIG


def test_save_and_load_config(mock_config_path):
    test_config = DEFAULT_CONFIG.copy()
    test_config["author"] = "Test Author"

    save_config(test_config)
    assert mock_config_path.exists()

    loaded = load_config()
    assert loaded["author"] == "Test Author"


def test_get_config_value(mock_config_path):
    save_config({"test_key": "test_val"})
    assert get_config_value("test_key") == "test_val"
    assert get_config_value("nonexistent", "fallback") == "fallback"


def test_set_config_value(mock_config_path):
    set_config_value("new_key", "new_val")
    config = load_config()
    assert config["new_key"] == "new_val"


def test_init_config(mock_config_path, capsys):
    init_config()
    assert mock_config_path.exists()
    captured = capsys.readouterr()
    assert "Created config at:" in captured.out

    init_config()
    captured = capsys.readouterr()
    assert "Config already exists at:" in captured.out
