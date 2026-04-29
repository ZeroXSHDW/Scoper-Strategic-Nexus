from .templates import TemplateLoader
from .variables import VariableProcessor

class SOWPipeline:
    def __init__(self):
        self.loader = TemplateLoader()
        self.var_processor = VariableProcessor()

    def assemble(self, modules):
        # Base template
        try:
            content = self.loader.load('SOW.md')
        except FileNotFoundError:
            content = "# Statement of Work\n"
        
        # Append modules
        for mod in modules:
            try:
                mod_content = self.loader.load(f"MODULE_{mod.upper()}.md")
                content += f"\n\n{mod_content}"
            except FileNotFoundError:
                content += f"\n\n## Module: {mod}\n[Content not found]\n"
        return content

    def get_required_variables(self, content):
        return self.var_processor.extract_variables(content)

    def render(self, content, variables):
        return self.var_processor.inject_variables(content, variables)
