import os
import json
from pathlib import Path
import questionary
from rich.console import Console

from .generator import ScopingPackGenerator

console = Console()

def run_tui(data_dir: Path):
    console.print("\n[bold blue]Welcome to the Strategic Nexus Scoper Engine[/bold blue]")
    console.print("[dim]Interactive Terminal Mode[/dim]\n")
    
    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Create New Scope",
                "Generate Master Compliance Pack",
                "View Compliance Dashboard",
                "Validate Data Integrity",
                "Update Framework Mappings",
                "Exit"
            ]
        ).ask()
        
        if action == "Exit" or action is None:
            console.print("[yellow]Exiting Scoper Engine...[/yellow]")
            break
        elif action == "Create New Scope":
            run_scoping_wizard(data_dir)
        elif action == "Generate Master Compliance Pack":
            import re
            def validate_client_name(text):
                if not text: return "Client name cannot be empty"
                if not re.match(r'^[\w\s\-\.]+$', text): return "Only alphanumeric, spaces, hyphens, and periods allowed"
                return True

            client_name = questionary.text(
                "Enter Client Name for Master Document:", 
                default="Global Enterprise Corp",
                validate=validate_client_name
            ).ask()
            if client_name:
                out_path = Path(f"output/{client_name.replace(' ', '_')}_Master_Scope.pdf")
                generator = ScopingPackGenerator(data_dir)
                console.print(f"\n[bold green]Generating Ultimate 7-Part Scoping Document for {client_name}...[/bold green]")
                # Use global-unified-pack which has all frameworks
                generator.generate(client_name, "Global", [], out_path, pack_id="global-unified-pack")
                console.print(f"[bold blue]✓ Master Document Saved to {out_path}[/bold blue]\n")
        elif action == "View Compliance Dashboard":
            os.system('scoper dashboard --compliance')
            console.print("\n")
        elif action == "Validate Data Integrity":
            os.system('scoper validate')
            console.print("\n")
        elif action == "Update Framework Mappings":
            from .downloader import fetch_and_map_frameworks
            fetch_and_map_frameworks(data_dir)

def run_scoping_wizard(data_dir: Path):
    # 1. Client Info
    import re
    def validate_client_name(text):
        if not text: return "Client name cannot be empty"
        if not re.match(r'^[\w\s\-\.]+$', text): return "Only alphanumeric, spaces, hyphens, and periods allowed"
        return True
        
    client_name = questionary.text("Enter Client Name:", validate=validate_client_name).ask()
    if not client_name: return
    
    region = questionary.text("Enter Region:", default="Global").ask()
    if region is None: return
    
    # 2. Pack Selection
    packs_path = data_dir / "compliance" / "packs.json"
    packs_data = []
    if packs_path.exists():
        packs_data = json.loads(packs_path.read_text(encoding='utf-8')).get('packs', [])
    
    pack_choices = [{"name": f"{p['label']} ({p['id']})", "value": p['id']} for p in packs_data]
    pack_choices.insert(0, {"name": "None (Manual Service Selection)", "value": None})
    
    pack_id = questionary.select("Select a Compliance Pack:", choices=pack_choices).ask()
    
    # 3. Services Selection
    catalog_path = data_dir / "services" / "catalog.json"
    catalog_data = []
    if catalog_path.exists():
        catalog_data = json.loads(catalog_path.read_text(encoding='utf-8'))
    
    service_choices = [{"name": f"{s['code']} - {s['label']}", "value": s['code']} for s in catalog_data]
    
    selected_services = questionary.checkbox(
        "Select additional technical services:",
        choices=service_choices
    ).ask()
    
    if selected_services is None:
        selected_services = []
        
    # Validation
    if not pack_id and not selected_services:
        console.print("[red]Error: You must select at least a Pack or one Service.[/red]\n")
        return
    
    # 4. Generate
    out_file = f"{client_name.replace(' ', '_')}_Scope.pdf"
    output_path = questionary.text("Output PDF filename:", default=out_file).ask()
    if not output_path: return
    
    console.print(f"\n[bold green]Generating Scoping Pack for {client_name}...[/bold green]")
    try:
        generator = ScopingPackGenerator(data_dir)
        final_path = generator.generate(client_name, region, selected_services, Path(output_path), pack_id=pack_id)
        console.print(f"[bold blue]✓ Success! Saved to {final_path}[/bold blue]\n")
    except Exception as e:
        console.print(f"[red]Error during generation: {e}[/red]\n")
