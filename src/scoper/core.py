"""Coherent Scoper Engine - Unified project management core with Phasing support."""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader

from .export import convert_format
from .templates import get_template, get_template_path, get_template_info
from .variables import VariableProcessor, load_variables_from_file


class ScoperProject:
    """A coherent representation of a Scoper project."""

    def __init__(self, path: Path):
        self.path = path.resolve()
        self.sow_file = self.path / "SOW.md"
        self.meta_file = self.path / ".scoper.json"
        self.meta = self._load_meta()

    def _load_meta(self) -> Dict[str, Any]:
        if self.meta_file.exists():
            try:
                return json.loads(self.meta_file.read_text())
            except Exception:
                return {}
        return {}

    def save_meta(self):
        """Save project metadata to disk."""
        self.meta_file.write_text(json.dumps(self.meta, indent=2))

    @classmethod
    def create(cls, name: str, output_dir: Path, template: str, variables: Dict[str, Any]) -> 'ScoperProject':
        """Initialize a new project from a template."""
        project_dir = output_dir / name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        vars_dict = variables.copy()
        vars_dict.setdefault("project_name", name)
        vars_dict.setdefault("author", "ZeroDevLLC")
        vars_dict.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
        vars_dict.setdefault("company", "ZeroDevLLC")
        
        meta = {
            "name": name,
            "template": template,
            "created": datetime.now().isoformat(),
            "variables": vars_dict,
            "modules": [],
            "phases": [
                {"name": "Discovery", "duration": "2 weeks"},
                {"name": "Development", "duration": "8 weeks"},
                {"name": "Launch", "duration": "2 weeks"}
            ],
            "build": {"formats": ["html", "pdf"], "theme": None},
            "budget": {"items": [], "currency": "$"}
        }
        (project_dir / ".scoper.json").write_text(json.dumps(meta, indent=2))
        
        project = cls(project_dir)
        project.sync()
        return project

    def add_phase(self, name: str, duration: str):
        """Add a new project phase."""
        if "phases" not in self.meta:
            self.meta["phases"] = []
        self.meta["phases"].append({"name": name, "duration": duration})
        self.save_meta()
        self.sync()

    def add_module(self, module_name: str):
        """Add a dynamic module to the SOW metadata and sync."""
        if "modules" not in self.meta:
            self.meta["modules"] = []
        if module_name not in self.meta["modules"]:
            self.meta["modules"].append(module_name)
            self.save_meta()
            self.sync()

    def sync(self):
        """Synchronize SOW.md with latest templates, snippets, and variables."""
        template_name = self.meta.get("template", "standard")
        variables = self.meta.get("variables", {}).copy()
        variables["modules"] = self.meta.get("modules", [])
        variables["phases"] = self.meta.get("phases", [])
        
        template_content = get_template(template_name) or get_template("standard")
        processor = VariableProcessor(variables)
        new_content = processor.process(template_content)
        
        # Check if modules are already rendered by the template
        has_auth = "Authentication & Identity Management" in new_content
        has_api = "API Infrastructure" in new_content
        
        # Only append modules that aren't already present
        modules_to_append = []
        for module in self.meta.get("modules", []):
            if module == "auth" and has_auth: continue
            if module == "api" and has_api: continue
            modules_to_append.append(module)

        for module in modules_to_append:
            module_tmpl = get_template(f"modules/{module}") or f"\n## {module.title()}\n- TBD"
            processed_module = processor.process(module_tmpl)
            new_content += "\n" + processed_module
            
        self.sow_file.write_text(new_content)
        self._update_timeline_section()
        self._update_budget_table()
        return self.sow_file

    def _update_timeline_section(self):
        """Regenerate the Timeline section based on phases."""
        phases = self.meta.get("phases", [])
        if not phases:
            return

        timeline = "\n## 5. Project Timeline\n\n"
        timeline += "| Phase | Estimated Duration | Description |\n"
        timeline += "|-------|--------------------|-------------|\n"
        for p in phases:
            timeline += f"| {p['name']} | {p['duration']} | |\n"

        content = self.sow_file.read_text()
        if "## 5. Timeline" in content:
            content = re.sub(r"## 5. Timeline.*?(?=\n##|$)", timeline, content, flags=re.DOTALL)
        elif "## 5. Project Timeline" in content:
            content = re.sub(r"## 5. Project Timeline.*?(?=\n##|$)", timeline, content, flags=re.DOTALL)
        else:
            # Look for where to insert
            if "## 4. Deliverables" in content:
                content = re.sub(r"(## 4. Deliverables.*?\n)(?=##|$)", r"\1" + timeline, content, flags=re.DOTALL)
            else:
                content += "\n" + timeline
        self.sow_file.write_text(content)

    def add_budget_item(self, description: str, amount: float, phase: Optional[str] = None):
        """Add a line item to the project budget."""
        if "budget" not in self.meta:
            self.meta["budget"] = {"items": [], "currency": "$"}
        self.meta["budget"]["items"].append({
            "description": description, 
            "amount": amount,
            "phase": phase
        })
        self.save_meta()
        self._update_budget_table()

    def _update_budget_table(self):
        """Regenerate the budget section in SOW.md with phasing support."""
        items = self.meta.get("budget", {}).get("items", [])
        if not items:
            return

        currency = self.meta["budget"].get("currency", "$")
        total = sum(item["amount"] for item in items)
        
        table = "\n## 6. Investment Summary\n\n"
        
        # Group by phase
        phases = {}
        for item in items:
            p = item.get("phase", "General")
            if p not in phases: phases[p] = []
            phases[p].append(item)
            
        for phase_name, p_items in phases.items():
            table += f"### {phase_name}\n"
            table += "| Item Description | Investment |\n"
            table += "|------------------|------------|\n"
            p_total = 0
            for item in p_items:
                table += f"| {item['description']} | {currency}{item['amount']:.2f} |\n"
                p_total += item["amount"]
            table += f"| *Phase Total* | *{currency}{p_total:.2f}* |\n\n"

        table += f"**Total Estimated Project Investment: {currency}{total:.2f}**\n"

        content = self.sow_file.read_text()
        if "## 6. Investment Summary" in content:
            content = re.sub(r"## 6. Investment Summary.*?(?=\n##|$)", table, content, flags=re.DOTALL)
        else:
            content += "\n" + table
        self.sow_file.write_text(content)

    def build(self, formats: Optional[List[str]] = None, css: Optional[str] = None):
        """Build the project exports."""
        build_fmts = formats or self.meta.get("build", {}).get("formats", ["html", "pdf"])
        theme = css or self.meta.get("build", {}).get("theme")
        results = {}
        for fmt in build_fmts:
            try:
                res = convert_format(str(self.sow_file), fmt, css_file=theme)
                results[fmt] = res
            except Exception as e:
                results[fmt] = f"Error: {e}"
        return results

    def get_health(self) -> Dict[str, Any]:
        """Perform a comprehensive health check of the project."""
        content = self.sow_file.read_text()
        processor = VariableProcessor()
        missing_vars = processor.extract_variables(content)
        mandatory = ["Overview", "Scope", "Deliverables", "Timeline", "Investment"]
        missing_sections = []
        for section in mandatory:
            if not re.search(f"## .*?{section}", content, re.IGNORECASE):
                missing_sections.append(section)
        word_count = len(content.split())
        total_budget = sum(i["amount"] for i in self.meta.get("budget", {}).get("items", []))
        score = 100
        score -= len(missing_vars) * 10
        score -= len(missing_sections) * 15
        if word_count < 200: score -= 10
        return {
            "score": max(0, score),
            "missing_vars": missing_vars,
            "missing_sections": missing_sections,
            "word_count": word_count,
            "total_budget": total_budget,
            "module_count": len(self.meta.get("modules", []))
        }
