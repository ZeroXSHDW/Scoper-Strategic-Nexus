from scoper.sow import update_sow


def test_update_sow_existing_section(tmp_path):
    sow_file = tmp_path / "SOW.md"
    sow_file.write_text(
        "## 1. Overview\n- Old content\n\n## 2. Scope\n- Existing content"
    )

    update_sow(str(sow_file), "Scope", "New content")

    content = sow_file.read_text()
    assert "- Existing content" in content
    assert "- New content" in content


def test_update_sow_new_section(tmp_path):
    sow_file = tmp_path / "SOW.md"
    sow_file.write_text("## 1. Overview\n- Old content")

    update_sow(str(sow_file), "Budget", "1000")

    content = sow_file.read_text()
    assert "## Budget" in content
    assert "- 1000" in content
