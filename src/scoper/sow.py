"""SOW Generator Module - Core SOW generation logic."""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .export import convert_format
from .templates import get_template, get_template_path
from .variables import VariableProcessor


def generate_sow(
    project_name: str,
    output_path: Path,
    template: str = "standard",
    variables: Optional[Dict[str, Any]] = None
) -> Path:
    """Generate a new SOW project with template and variables."""
    # Create project directory
    project_dir = output_path / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    # Get template
    template_content = get_template(template) or get_template("standard")
    if template_content is None:
        template_content = ""

    # Build variables
    vars_dict = variables or {}
    vars_dict.setdefault("project_name", project_name)
    vars_dict.setdefault("author", "ZeroDevLLC")
    vars_dict.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
    vars_dict.setdefault("version", "1.0")
    vars_dict.setdefault("company", "ZeroDevLLC")

    # Process template with variables
    processor = VariableProcessor(vars_dict)
    content = processor.process(template_content)

    # Save SOW file
    sow_file = project_dir / "SOW.md"
    sow_file.write_text(content)

    # Copy assets if they exist (style.css, logo.png, etc.)
    tp = get_template_path(template)
    if tp:
        # Check for style.css in the template's directory
        style_css = tp.parent / "style.css"
        if style_css.exists():
            shutil.copy2(style_css, project_dir / "style.css")
        
        # Could extend this to copy an entire 'assets' folder
        assets_dir = tp.parent / "assets"
        if assets_dir.exists() and assets_dir.is_dir():
            shutil.copytree(assets_dir, project_dir / "assets", dirs_exist_ok=True)

    # Create metadata file
    meta_file = project_dir / ".scoper.json"
    meta = {
        "name": project_name,
        "template": template,
        "created": datetime.now().isoformat(),
        "variables": vars_dict
    }
    meta_file.write_text(json.dumps(meta, indent=2))

    return sow_file


def parse_and_generate(
    input_file: str,
    format: str = "md",
    output: Optional[str] = None,
    variables: Optional[Dict[str, Any]] = None
) -> Path:
    """Parse input file and generate SOW with variables."""
    input_path = Path(input_file)
    content = input_path.read_text()

    # Process variables
    processor = VariableProcessor(variables)
    processed = processor.process(content)

    # Write processed content
    output_path = Path(output) if output else input_path
    output_path.write_text(processed)

    # Convert format if needed
    if format != "md":
        return convert_format(str(output_path), format)

    return output_path


def read_sow(sow_file: str) -> dict:
    """Read and parse an SOW file."""
    path = Path(sow_file)
    content = path.read_text()

    # Extract sections
    sections: Dict[str, Any] = {}
    current_section = "meta"
    lines = content.split('\n')

    for line in lines:
        if line.startswith('## '):
            current_section = line[3:].strip().lower().replace(' ', '_')
            sections[current_section] = []
        elif current_section != "meta":
            if current_section not in sections:
                sections[current_section] = []
            sections[current_section].append(line)

    # Clean up
    for key in sections:
        sections[key] = '\n'.join(sections[key]).strip()

    return {
        "content": content,
        "sections": sections,
        "file": str(path),
        "name": path.stem
    }


def update_sow(sow_file: str, section_name: str, content: str) -> None:
    """Update a section in SOW file robustly."""
    path = Path(sow_file)
    lines = path.read_text().split('\n')

    section_pattern = re.compile(
        f"^## .*?{re.escape(section_name)}", re.IGNORECASE
    )

    start_idx = -1
    for i, line in enumerate(lines):
        if section_pattern.match(line):
            start_idx = i
            break

    if start_idx != -1:
        # Find the end of the section (next header or end of file)
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            if lines[i].startswith("## "):
                end_idx = i
                break

        # Insert content before the next section
        insert_at = end_idx
        while insert_at > start_idx + 1 and not lines[insert_at-1].strip():
            insert_at -= 1

        lines.insert(insert_at, f"- {content}")
    else:
        # Section not found, append to end
        lines.append(f"\n## {section_name.title()}")
        lines.append(f"- {content}")

    path.write_text('\n'.join(lines))


def list_projects(directory: str = ".") -> list:
    """List all SOW projects in directory."""
    projects = []

    for path in Path(directory).glob("*/"):
        if not path.is_dir():
            continue
        sow_file = path / "SOW.md"
        if sow_file.exists():
            meta_file = path / ".scoper.json"
            meta = {}
            if meta_file.exists():
                try:
                    meta = json.loads(meta_file.read_text())
                except Exception:
                    pass

            projects.append({
                "name": path.name,
                "template": meta.get("template", "unknown"),
                "created": meta.get("created", ""),
                "path": str(path)
            })

    return projects


def get_project_info(project_name: str) -> dict:
    """Get project information."""
    project_dir = Path(project_name)
    if not project_dir.exists():
        raise ValueError(f"Project not found: {project_name}")

    sow_file = project_dir / "SOW.md"
    if not sow_file.exists():
        raise ValueError(f"SOW not found in: {project_name}")

    meta_file = project_dir / ".scoper.json"
    meta = {}
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
        except Exception:
            pass

    return {
        "name": project_name,
        "sow": sow_file.read_text()[:500],
        "meta": meta
    }
