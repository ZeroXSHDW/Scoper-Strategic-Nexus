import pytest
from click.testing import CliRunner
from scoper.cli import main

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_main_help(runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Scoper - Statement of Work Scoper CLI Tool" in result.output

def test_init_command(runner, tmp_path):
    result = runner.invoke(
        main, ['init', 'my_project', '-o', str(tmp_path), '-t', 'simple']
    )
    assert result.exit_code == 0
    assert "Created Phased SOW project:" in result.output
    assert (tmp_path / 'my_project' / 'SOW.md').exists()
