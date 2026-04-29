"""Variable Processor Module - Handle {{placeholder}} substitutions and template inheritance."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader


class VariableProcessor:
    """Process variables and handle template inheritance/snippets."""

    BUILTIN_VARIABLES = {
        "date": lambda: datetime.now().strftime("%Y-%m-%d"),
        "datetime": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "year": lambda: datetime.now().strftime("%Y"),
        "month": lambda: datetime.now().strftime("%B"),
        "timestamp": lambda: datetime.now().isoformat(),
    }

    def __init__(self, custom_vars: Optional[Dict[str, Any]] = None):
        self.custom_vars = custom_vars or {}
        self.builtin_values = {
            k: v() if callable(v) else v
            for k, v in self.BUILTIN_VARIABLES.items()
        }
        self.variables = {**self.builtin_values, **self.custom_vars}
        
        # Configure Jinja2 Environment for snippets AND template inheritance
        search_dirs = [
            Path.home() / ".config" / "scoper" / "snippets",
            Path.home() / ".config" / "scoper" / "templates",
            Path(__file__).parent / "snippets",
            Path(__file__).parent / "templates"
        ]
        valid_dirs = [str(d) for d in search_dirs if d.exists()]
        self.env = Environment(loader=FileSystemLoader(valid_dirs)) if valid_dirs else Environment()

    def get_variable(self, name: str) -> str:
        """Get variable value by name."""
        return str(self.variables.get(name, f"{{{{{name}}}}}"))

    def process(self, content: str) -> str:
        """Process content using Jinja2 with inheritance support."""
        try:
            template = self.env.from_string(content)
            return template.render(**self.variables)
        except Exception as e:
            # Fallback for simple cases if Jinja2 environment fails
            pattern = re.compile(r'\{\{(\w+)\}\}')

            def replace(match):
                var_name = match.group(1)
                return self.get_variable(var_name)
            return pattern.sub(replace, content)

    def process_jinja2(self, content: str) -> str:
        """Alias for process (legacy support)."""
        return self.process(content)

    def extract_variables(self, content: str) -> List[str]:
        """Extract all variable names from content."""
        pattern = re.compile(r'\{\{(\w+)\}\}')
        return list(set(pattern.findall(content)))

    def list_variables(self) -> Dict[str, str]:
        """List all available variables."""
        return {k: str(v) for k, v in self.variables.items()}


def load_variables_from_file(file_path: str) -> Dict[str, Any]:
    """Load variables from JSON or YAML file."""
    path = Path(file_path)
    if not path.exists():
        return {}

    content = path.read_text()
    if path.suffix == '.json':
        return json.loads(content)
    elif path.suffix in ['.yaml', '.yml']:
        return yaml.safe_load(content)
    else:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return yaml.safe_load(content)


def process_file(
    filepath: str, variables: Optional[Dict[str, Any]] = None
) -> str:
    """Process a file with variables."""
    content = Path(filepath).read_text()
    processor = VariableProcessor(variables)
    return processor.process(content)


def list_available_variables() -> Dict[str, str]:
    """List all built-in variables."""
    return VariableProcessor().list_variables()
