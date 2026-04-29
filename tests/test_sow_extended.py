import pytest
from scoper.sow import (
    generate_sow, parse_and_generate, read_sow,
    list_projects, get_project_info
)


def test_generate_sow(tmp_path):
    project_name = "test_project"
    vars_dict = {"client_name": "Test Client"}

    sow_file = generate_sow(project_name, tmp_path, "standard", vars_dict)

    assert sow_file.exists()
    assert sow_file.name == "SOW.md"

    content = sow_file.read_text()
    assert "test_project" in content
    assert "Test Client" in content

    # Check meta file
    meta_file = tmp_path / project_name / ".scoper.json"
    assert meta_file.exists()
    assert '"template": "standard"' in meta_file.read_text()


def test_parse_and_generate(tmp_path):
    input_file = tmp_path / "input.md"
    input_file.write_text("Hello {{name}}")

    output_file = parse_and_generate(
        str(input_file), format="md",
        variables={"name": "World"}
    )

    assert output_file.exists()
    assert output_file.read_text() == "Hello World"


def test_read_sow(tmp_path):
    sow_file = tmp_path / "SOW.md"
    content = (
        "## Meta Info\nSome content\n\n"
        "## Budget\n1000\n\n"
        "## Scope\nScope content\n"
    )
    sow_file.write_text(content)

    result = read_sow(str(sow_file))
    assert result["name"] == "SOW"
    assert "budget" in result["sections"]
    assert result["sections"]["budget"] == "1000"
    assert "scope" in result["sections"]
    assert result["sections"]["scope"] == "Scope content"


def test_list_projects_and_info(tmp_path):
    project1 = tmp_path / "proj1"
    project1.mkdir()
    (project1 / "SOW.md").write_text("SOW 1")
    meta_content = '{"template": "simple", "created": "2023"}'
    (project1 / ".scoper.json").write_text(meta_content)

    projects = list_projects(str(tmp_path))
    assert len(projects) == 1
    assert projects[0]["name"] == "proj1"
    assert projects[0]["template"] == "simple"

    info = get_project_info(str(project1))
    assert info["name"] == str(project1)
    assert info["sow"] == "SOW 1"
    assert info["meta"]["template"] == "simple"


def test_get_project_info_errors(tmp_path):
    with pytest.raises(ValueError, match="Project not found"):
        get_project_info(str(tmp_path / "nonexistent"))

    project_empty = tmp_path / "empty_proj"
    project_empty.mkdir()

    with pytest.raises(ValueError, match="SOW not found"):
        get_project_info(str(project_empty))
