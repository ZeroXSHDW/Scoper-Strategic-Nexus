import pytest
from scoper.templates import (
    list_available_templates, get_template,
    get_template_info, copy_template
)


def test_list_available_templates():
    templates = list_available_templates()
    assert "default" in templates
    assert "standard" in templates
    assert "simple" in templates


def test_get_template_builtin():
    content = get_template("default")
    assert content is not None
    assert "# Statement of Work: {{project_name}}" in content


def test_get_template_not_found():
    assert get_template("nonexistent_template_name") is None


def test_get_template_info():
    info = get_template_info("simple")
    assert info["name"] == "simple"
    assert "variables" in info
    assert "project_name" in info["variables"]
    assert info["variable_count"] > 0


def test_get_template_info_not_found():
    info = get_template_info("nonexistent")
    assert info == {}


def test_copy_template(tmp_path):
    dest = tmp_path / "copied_template.md"
    copy_template("simple", str(dest))

    assert dest.exists()
    assert "Statement of Work" in dest.read_text()


def test_copy_template_not_found(tmp_path):
    dest = tmp_path / "copied_template.md"
    with pytest.raises(ValueError, match="Template 'nonexistent' not found"):
        copy_template("nonexistent", str(dest))
