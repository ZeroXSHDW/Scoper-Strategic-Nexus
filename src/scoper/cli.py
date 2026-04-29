"""Scoper CLI - Unified interface for Phased Scoping."""

import os
import subprocess
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

from . import __version__
from .config import load_config, set_config_value
from .core import ScoperProject
from .templates import (
    get_template, get_template_info, list_available_templates
)
from .variables import (
    VariableProcessor, list_available_variables, load_variables_from_file
)
from .validator import Validator
from .generator import ScopingPackGenerator
from .downloader import fetch_and_map_frameworks

console = Console()

@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctx):
    """Scoper - Statement of Work Scoper CLI Tool."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config()
    
    if ctx.invoked_subcommand is None:
        from .tui import run_tui
        data_dir = Path(__file__).parent / "data"
        run_tui(data_dir)


@main.command()
@click.argument("project_name")
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--template", "-t", default="standard", help="Template to use")
@click.option("--vars", "-v", multiple=True, help="Variables (key=value)")
@click.option("--var-file", "-f", type=click.Path(exists=True), help="Load variables from file")
@click.option("--interactive", "-i", is_flag=True, help="Prompt for missing variables")
@click.pass_context
def init(ctx, project_name: str, output: str, template: str, vars, var_file: str, interactive: bool):
    """Initialize a new SOW project."""
    config = ctx.obj.get('config', {})
    file_vars = load_variables_from_file(var_file) if var_file else {}
    cli_vars = dict(v.split("=", 1) for v in vars) if vars else {}
    variables = {**config.get("variables", {}), **file_vars, **cli_vars}

    if interactive:
        info = get_template_info(template)
        template_vars = info.get("variables", [])
        schema = info.get("schema", {})
        builtin_keys = list_available_variables().keys()
        excluded = set(builtin_keys) | {"project_name", "date", "author", "version", "company"}
        
        for v in template_vars:
            if v not in variables and v not in excluded:
                v_meta = schema.get(v, {})
                desc = v_meta.get("description", v)
                default = v_meta.get("default", "")
                val = click.prompt(f"Enter {desc}", default=default)
                variables[v] = val

    project = ScoperProject.create(project_name, Path(output), template, variables)
    console.print(f"[green][+] Created Phased SOW project:[/green] {project.sow_file}")


@main.command()
@click.argument("project_path", type=click.Path(exists=True), default=".")
@click.option("--format", "-f", multiple=True, help="Formats to build")
@click.option("--css", "-c", type=click.Path(exists=True), help="Custom CSS file")
def build(project_path: str, format: list, css: str):
    """Build project exports."""
    path = Path(project_path)
    if (path / "SOW.md").exists():
        project = ScoperProject(path)
    elif path.name == "SOW.md":
        project = ScoperProject(path.parent)
    else:
        console.print("[red]Error: Could not find SOW.md.[/red]")
        return

    console.print(f"Building project: [bold]{project.meta.get('name')}[/bold]")
    with Progress() as progress:
        task = progress.add_task("[cyan]Exporting...", total=len(format or project.meta.get("build", {}).get("formats", [])))
        results = project.build(formats=list(format) if format else None, css=css)
        for fmt, res in results.items():
            if "Error" in str(res):
                console.print(f"  [red][-] {fmt.upper()}: {res}[/red]")
            else:
                console.print(f"  [green][+] {fmt.upper()}: {res}[/green]")
            progress.update(task, advance=1)


@main.command()
@click.argument("module_name")
@click.argument("project_path", type=click.Path(exists=True), default=".")
def add(module_name: str, project_path: str):
    """Add a module to the SOW."""
    project = ScoperProject(Path(project_path))
    project.add_module(module_name)
    console.print(f"[green][+] Added module '{module_name}'[/green]")


@click.group()
def phase():
    """Manage project phases."""
    pass

@phase.command(name="add")
@click.argument("name")
@click.argument("duration")
@click.argument("project_path", type=click.Path(exists=True), default=".")
def add_phase(name: str, duration: str, project_path: str):
    """Add a new phase (e.g., 'Testing', '2 weeks')."""
    project = ScoperProject(Path(project_path))
    project.add_phase(name, duration)
    console.print(f"[green][+] Added phase '{name}' ({duration})[/green]")

main.add_command(phase)


@main.command()
@click.argument("description")
@click.argument("amount", type=float)
@click.option("--phase", "-p", help="Assign to a specific phase")
@click.argument("project_path", type=click.Path(exists=True), default=".")
def budget(description: str, amount: float, phase: str, project_path: str):
    """Add a budget item, optionally linked to a phase."""
    project = ScoperProject(Path(project_path))
    project.add_budget_item(description, amount, phase=phase)
    console.print(f"[green][+] Added budget item to {phase or 'General'}[/green]")


@main.command()
@click.argument("project_path", type=click.Path(exists=True), default=".")
def sync(project_path: str):
    """Sync project SOW.md with metadata."""
    project = ScoperProject(Path(project_path))
    result = project.sync()
    console.print(f"[green][+] Synchronized SOW:[/green] {result}")


@main.command()
@click.argument("directory", type=click.Path(exists=True), default=".")
@click.option("--compliance", is_flag=True, help="Show the Compliance Packs Matrix")
def dashboard(directory: str, compliance: bool):
    """Show dashboard of projects or compliance matrix."""
    if compliance:
        import json
        packs_path = Path(__file__).parent / "data" / "compliance" / "packs.json"
        
        table = Table(title="Compliance & Regulatory Pack Matrix", header_style="bold blue", show_lines=True)
        table.add_column("Pack ID / Label", style="cyan")
        table.add_column("Frameworks", style="magenta")
        table.add_column("Services (Ruleset)", style="green")
        table.add_column("Narrative", style="white", ratio=2)

        if packs_path.exists():
            packs_data = json.loads(packs_path.read_text(encoding='utf-8')).get('packs', [])
            for p in packs_data:
                table.add_row(
                    f"[bold]{p.get('id')}[/bold]\n[dim]{p.get('label')}[/dim]",
                    ", ".join(p.get('frameworks', [])),
                    ", ".join(p.get('services', [])),
                    p.get('narrative', '')
                )
        else:
            console.print("[red]Could not find compliance packs data.[/red]")
            return

        console.print(table)
        return

    table = Table(title="Scoper Dashboard", header_style="bold blue")
    table.add_column("Project", style="cyan")
    table.add_column("Budget", justify="right", style="green")
    table.add_column("Phases", justify="center")
    table.add_column("Health", justify="center")

    for path in Path(directory).glob("*/"):
        if not path.is_dir() or not (path / ".scoper.json").exists():
            continue
        project = ScoperProject(path)
        health = project.get_health()
        score = health["score"]
        color = "green" if score > 80 else "yellow" if score > 50 else "red"
        
        table.add_row(
            project.meta.get("name", path.name),
            f"${health['total_budget']:,.2f}",
            str(len(project.meta.get("phases", []))),
            f"[{color}]{score}%[/{color}]"
        )
    console.print(table)


@main.command()
@click.argument("project_path", type=click.Path(exists=True), default=".")
def doctor(project_path: str):
    """Check project health."""
    project = ScoperProject(Path(project_path))
    health = project.get_health()
    console.print(f"Health: [blue]{health['score']}%[/blue]")
    if health["missing_vars"]:
        console.print(f"[yellow]Missing Vars:[/yellow] {', '.join(health['missing_vars'])}")
    if health["missing_sections"]:
        console.print(f"[red]Missing Sections:[/red] {', '.join(health['missing_sections'])}")


@main.command()
@click.option("--data-dir", type=click.Path(exists=True), help="Path to data directory")
def validate(data_dir: str):
    """Validate the compliance catalog and packs."""
    import sys
    
    if data_dir:
        path = Path(data_dir)
    else:
        path = Path(__file__).parent / "data"
        
    validator = Validator(path)
    results = validator.validate()
    
    if results["passed"]:
        console.print(f"[green][+] Data catalog at {path} is valid.[/green]")
    else:
        console.print(f"[red][-] Validation failed for data catalog at {path}:[/red]")
        for err in results["errors"]:
            console.print(f"  [red]- {err}[/red]")
        sys.exit(1)


@main.command(name="generate-pack")
@click.option("--client", required=True, help="Client Name")
@click.option("--region", default="Global", help="Client Region")
@click.option("--pack", help="Compliance Pack ID (e.g. dora-bank-resilience)")
@click.option("--service", "-s", multiple=True, help="Additional Service Codes (e.g. PT-NET-EXT)")
@click.option("--output", "-o", type=click.Path(), default="output.pdf", help="Output PDF path")
@click.option("--data-dir", type=click.Path(exists=True), help="Path to data directory")
def generate_pack(client: str, region: str, pack: str, service: list, output: str, data_dir: str):
    """Generate an advanced Strategic Nexus scoping pack."""
    import sys
    
    if data_dir:
        path = Path(data_dir)
    else:
        path = Path(__file__).parent / "data"
        
    try:
        generator = ScopingPackGenerator(path)
        out_path = Path(output)
        
        console.print(f"Generating Nexus Pack for [bold]{client}[/bold]...")
        final_path = generator.generate(client, region, list(service), out_path, pack_id=pack)
        
        console.print(f"[green][+] Successfully generated: {final_path}[/green]")
        
        # Auto-open the document on macOS
        if sys.platform == "darwin":
            os.system(f"open '{final_path}'")

    except Exception as e:
        console.print(f"[red][-] Failed to generate pack: {e}[/red]")
        sys.exit(1)


@main.command(name="wizard")
@click.option("--data-dir", type=click.Path(exists=True), help="Path to data directory")
@click.pass_context
def wizard(ctx, data_dir: str):
    """Interactive guided wizard for generating scoping packs."""
    import sys
    from rich.prompt import Prompt, Confirm
    import json
    
    if data_dir:
        path = Path(data_dir)
    else:
        path = Path(__file__).parent / "data"
        
    console.print("\n[bold cyan]=== Regulatory Vendor Scoping Wizard ===[/bold cyan]\n")
    
    client_name = Prompt.ask("[bold]Enter the Client Name[/bold]")
    region = Prompt.ask("[bold]Enter the primary operating region[/bold]", default="Global")
    
    # Load packs
    packs_path = path / "compliance" / "packs.json"
    packs = []
    if packs_path.exists():
        packs = json.loads(packs_path.read_text(encoding='utf-8')).get('packs', [])
        
    if not packs:
        console.print("[red]No compliance packs found in data directory.[/red]")
        sys.exit(1)
        
    console.print("\n[bold]Select a Compliance Strategy:[/bold]")
    for i, pack in enumerate(packs):
        console.print(f"  [cyan]{i+1}[/cyan]. {pack.get('label')} ({pack.get('id')})")
        
    pack_idx = int(Prompt.ask("Enter number", default="1")) - 1
    selected_pack = packs[pack_idx]
    
    console.print(f"\n[green]Selected:[/green] {selected_pack.get('label')}")
    
    add_svcs = Confirm.ask("\nWould you like to add any additional ad-hoc services?")
    extra_services = []
    if add_svcs:
        catalog_path = path / "services" / "catalog.json"
        catalog = []
        if catalog_path.exists():
            catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
            
        console.print("\n[bold]Available Services:[/bold]")
        for i, svc in enumerate(catalog):
            console.print(f"  [cyan]{i+1}[/cyan]. {svc.get('code')} - {svc.get('label')}")
            
        svc_idxs = Prompt.ask("Enter numbers (comma-separated)", default="")
        if svc_idxs.strip():
            for idx_str in svc_idxs.split(','):
                idx = int(idx_str.strip()) - 1
                extra_services.append(catalog[idx].get('code'))
                
    output_pdf = Prompt.ask("\n[bold]Output PDF filename[/bold]", default=f"output/{client_name.replace(' ', '_')}_Scope.pdf")
    
    console.print("\n[cyan]Generating your premium scoping pack...[/cyan]")
    ctx.invoke(generate_pack, client=client_name, region=region, pack=selected_pack.get('id'), service=extra_services, output=output_pdf, data_dir=data_dir)


@main.command(name="fetch-frameworks")
@click.option("--data-dir", type=click.Path(exists=True), help="Path to data directory")
def fetch_frameworks_cmd(data_dir: str):
    """Download and map latest compliance frameworks."""
    import sys
    from pathlib import Path
    
    if data_dir:
        d_dir = Path(data_dir)
    else:
        d_dir = Path(__file__).parent / "data"
        
    fetch_and_map_frameworks(d_dir)
    
if __name__ == "__main__":
    main()
