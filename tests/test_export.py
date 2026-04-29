import pytest
import re
from scoper.export import (
    convert_markdown_to_html, export_to_html, export_to_text,
    export_to_markdown, convert_format
)


def test_convert_markdown_to_html():
    md = "# Title\n\n**Bold** and *Italic*\n\n- Item 1\n- Item 2"
    html = convert_markdown_to_html(md)

    # Use regex or check for presence of tags and content separately
    assert re.search(r'<h1.*?>Title</h1>', html)
    assert "<strong>Bold</strong>" in html
    assert "<em>Italic</em>" in html
    assert "<li>Item 1</li>" in html


def test_export_to_html(tmp_path):
    input_file = tmp_path / "input.md"
    input_file.write_text("# Hello HTML")

    output_file = tmp_path / "output.html"
    result = export_to_html(str(input_file), str(output_file))

    assert result.exists()
    assert re.search(r'<h1.*?>Hello HTML</h1>', result.read_text())


def test_export_to_text(tmp_path):
    input_file = tmp_path / "input.md"
    input_file.write_text("# Plain Text\n**bold**")

    output_file = tmp_path / "output.txt"
    result = export_to_text(str(input_file), str(output_file))

    assert result.exists()
    text = result.read_text()
    assert "Plain Text" in text
    assert "bold" in text
    assert "#" not in text
    assert "**" not in text


def test_export_to_markdown_vars(tmp_path):
    input_file = tmp_path / "input.md"
    input_file.write_text("Hello {{year}}")

    result = export_to_markdown(str(input_file))

    assert result.exists()
    content = result.read_text()
    assert "{{year}}" not in content
    assert "20" in content  # Checking if year processed


def test_convert_format_unknown():
    with pytest.raises(ValueError, match="Unknown format"):
        convert_format("input.md", "unknown_fmt")
