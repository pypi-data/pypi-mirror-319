# Command-line interface providing PyPI package name validation and search functionality
import click
import os
import subprocess
from rich.console import Console
from rich.prompt import Confirm
from .check import PackageNameChecker
from .search import PackageSearcher
from .venv import VenvManager
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich.style import Style
from pathlib import Path
import sys
from .package import PackageManager
from typing import Optional
from .utils import get_current_shell, get_environment_display_name
from rich.markup import escape
import tomllib
import requests
import json
from urllib.error import HTTPError

# Force color output
console = Console(force_terminal=True, color_system="auto")


def find_next_test_version(project_name: str, base_version: str) -> str:
    """Find the next available test version number for Test PyPI"""

    def version_exists(version: str) -> bool:
        url = f"https://test.pypi.org/pypi/{project_name}/{version}/json"
        try:
            response = requests.get(url)
            return response.status_code == 200
        except:
            return False

    # If base version already has .dev, use it as is
    if ".dev" in base_version:
        return base_version

    test_version = f"{base_version}.dev0"
    index = 0

    while version_exists(test_version):
        index += 1
        test_version = f"{base_version}.dev{index}"

    return test_version


def update_version_in_pyproject(version: str):
    """Update version in pyproject.toml"""
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        content = f.read()

    # Use simple string replacement to preserve formatting
    import re

    pattern = r'(version\s*=\s*["\'])([^"\']*?)(["\'])'
    repl = lambda m: f"{m.group(1)}{version}{m.group(3)}"
    new_content = re.sub(pattern, repl, content)

    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(new_content)


def create_status_table(title: str, rows: list[tuple[str, str, str]]) -> Table:
    """Create a status table with consistent styling"""
    table = Table(
        title=title,
        show_header=False,
        box=None,
        padding=(0, 2),
        collapse_padding=True,
        expand=False,
        title_justify="left",
    )

    table.add_column("Key", style="dim")
    table.add_column("Value", style="bold")
    table.add_column("Status", justify="right")

    for row in rows:
        table.add_row(*row)

    return table


@click.group()
def cli():
    """[cyan]PyMin[/cyan] CLI tool for PyPI package management

    \b
    Core Commands:
      check       Check package name availability on PyPI
      search      Search for similar package names
      venv        Create a virtual environment

    \b
    Environment:
      activate    Activate virtual environment
      deactivate  Deactivate virtual environment
      info        Show environment information

    \b
    Package Management:
      add         Add package to requirements.txt
      remove      Remove package from requirements.txt
      list        List all packages in requirements.txt
    """
    pass


@cli.command()
@click.argument("name")
def check(name):
    """Check package name availability"""
    checker = PackageNameChecker()
    result = checker.check_availability(name)
    checker.display_result(result)


@cli.command()
@click.argument("name")
@click.option(
    "--threshold",
    "-t",
    default=0.8,
    help="Similarity threshold (0.0-1.0)",
    type=float,
)
def search(name: str, threshold: float):
    """Search for similar package names on PyPI"""
    searcher = PackageSearcher(similarity_threshold=threshold)
    results = searcher.search_similar(name)

    if not results:
        console.print("[yellow]No similar packages found.[/yellow]")
        return

    table = Table(
        title=Text.assemble(
            "Similar Packages to '",
            (name, "cyan"),
            "'",
        ),
        show_header=True,
        header_style="bold magenta",
        expand=False,
        title_justify="left",
    )

    table.add_column("Package Name", style="cyan")
    table.add_column("Similarity", justify="center")
    table.add_column("PyPI URL", style="blue")

    for pkg_name, similarity in results:
        url = searcher.get_package_url(pkg_name)
        table.add_row(
            pkg_name, f"{similarity:.2%}", f"[link={url}]{url}[/link]"
        )

    console.print("\n")  # Add empty line
    console.print(table)
    console.print(
        "\n[dim]Tip: Click on package names or URLs to open in browser[/dim]"
    )


@cli.command()
@click.argument("name", default="env")
def venv(name):
    """Create a virtual environment with specified name"""
    venv_path = Path(name)

    # Check if virtual environment already exists
    if venv_path.exists() and venv_path.is_dir():
        if Confirm.ask(
            f"\n[yellow]Virtual environment '{name}' already exists. Do you want to rebuild it?[/yellow]"
        ):
            # Deactivate if current environment is active
            if os.environ.get("VIRTUAL_ENV") == str(venv_path.absolute()):
                shell, shell_name = get_current_shell()
                deactivate_cmd = (
                    f"source {venv_path}/bin/activate && deactivate"
                )
                subprocess.run([shell, "-c", deactivate_cmd])

            # Remove existing virtual environment
            import shutil

            shutil.rmtree(venv_path)
            console.print(
                f"[green]✓ Removed existing environment: {name}[/green]"
            )
        else:
            console.print("[yellow]Operation cancelled.[/yellow]")
            return

    manager = VenvManager()
    success, message = manager.create_venv(name)

    if success:
        venv_info = manager.get_venv_info(name)
        text = Text.assemble(
            ("Virtual Environment: ", "dim"),
            (name, "cyan"),
            "\n",
            ("Python Version: ", "dim"),
            (venv_info["python_version"], "cyan"),
            "\n",
            ("Pip Version: ", "dim"),
            (venv_info["pip_version"], "cyan"),
            "\n",
            ("Location: ", "dim"),
            (str(venv_info["location"]), "cyan"),
            "\n",
            ("Status: ", "dim"),
            ("✓ Created", "green"),
        )
        panel = Panel.fit(
            text,
            title="Virtual Environment Creation Results",
            title_align="left",
            border_style="bright_blue",
        )
        console.print(panel)

        # Prepare to activate virtual environment
        activate_script = venv_path / "bin" / "activate"
        shell, shell_name = get_current_shell()

        # Check if requirements.txt exists
        if Path("requirements.txt").exists():
            if Confirm.ask(
                "\n[yellow]Found requirements.txt. Do you want to install the dependencies?[/yellow]"
            ):
                # Activate virtual environment and upgrade pip
                subprocess.run(
                    [
                        shell,
                        "-c",
                        f"source {activate_script} && pip install --upgrade pip",
                    ],
                    check=True,
                )

                # Install packages in virtual environment
                os.environ["VIRTUAL_ENV"] = str(venv_path)
                os.environ["PATH"] = f"{venv_path}/bin:{os.environ['PATH']}"
                package_manager = PackageManager()
                with open("requirements.txt") as f:
                    packages = [
                        line.strip()
                        for line in f
                        if line.strip() and not line.startswith("#")
                    ]
                for package in packages:
                    if "==" in package:
                        name, version = package.split("==")
                        package_manager.add(name, version)
                    else:
                        package_manager.add(package)

        # Activate virtual environment
        os.execl(
            shell,
            shell_name,
            "-c",
            f"source {activate_script} && exec {shell_name}",
        )
    else:
        text = Text.assemble(
            ("Status: ", "dim"),
            ("✗ Failed", "red"),
            "\n",
            ("Error: ", "dim"),
            (message, "red"),
        )
        panel = Panel.fit(
            text,
            title="Virtual Environment Creation Error",
            title_align="left",
            border_style="red",
        )
        console.print(panel)


@cli.command()
def info():
    """Show environment information"""
    manager = VenvManager()
    info = manager.get_environment_info()

    text = Text()
    text.append("\n")

    # System Information
    text.append("System Information", "bold white")
    text.append("\n")
    text.append("  Python Version: ", "dim")
    text.append(str(info["python_version"]), "cyan")
    text.append("\n")
    text.append("  Platform: ", "dim")
    text.append(str(info["platform"]), "cyan")
    text.append("\n")
    text.append("  Working Directory: ", "dim")
    text.append(str(info["working_dir"]), "cyan")
    text.append("\n")
    text.append("  Pip: ", "dim")
    text.append(
        f"{str(info['pip_version'])} at {str(info['pip_location'])}", "cyan"
    )

    # Show pip update if available
    if info.get("pip_update"):
        text.append(" (", "dim")
        text.append(f"update available: {str(info['pip_update'])}", "yellow")
        text.append(")", "dim")

    text.append("\n")
    text.append("  User Scripts: ", "dim")
    text.append(str(info["user_scripts"]), "cyan")
    text.append("\n")

    # Project info if available
    if "project" in info:
        project = info["project"]
        text.append("\n")
        text.append("Project Information", "bold white")
        text.append("\n")
        text.append("  Name: ", "dim")
        text.append(str(project["name"]), "green")
        text.append("\n")
        text.append("  Version: ", "dim")
        text.append(str(project["version"]), "green")
        text.append("\n")
        text.append("  Description: ", "dim")
        text.append(str(project["description"]), "green")
        text.append("\n")
        text.append("  Python Required: ", "dim")
        text.append(str(project["requires_python"]), "green")
        text.append("\n")
        text.append("  Build Backend: ", "dim")
        text.append(str(project["build_backend"]), "green")
        text.append("\n")

        # Show CLI commands if available
        if "scripts" in project:
            text.append("  Commands:", "dim")
            text.append("\n")
            for cmd_name, cmd_path in sorted(project["scripts"].items()):
                text.append("    ", "dim")
                text.append(cmd_name, "cyan")
                text.append("  ", "dim")
                text.append(cmd_path, "green")
                text.append("\n")

        # Show dependencies count if available
        if project.get("dependencies"):
            deps_count = len(project["dependencies"])
            text.append("  Dependencies: ", "dim")
            text.append(f"{deps_count} packages", "green")
            text.append("\n")

    # Virtual environment info
    text.append("\n")
    text.append("Virtual Environment", "bold white")
    text.append("\n")

    # Show active virtual environment if any
    if info["virtual_env"]:
        active_venv_path = Path(info["virtual_env"])
        text.append("  Active Environment:", "dim")
        text.append("\n")
        text.append("    Name: ", "dim")
        text.append(active_venv_path.name, "cyan")
        text.append("\n")
        text.append("    Path: ", "dim")
        text.append(str(active_venv_path), "cyan")
        text.append("\n")

    # Show current directory virtual environment status
    text.append("  Current Directory:", "dim")
    text.append("\n")

    current_venv = Path("env")
    if current_venv.exists() and current_venv.is_dir():
        text.append("    Name: ", "dim")
        text.append("env", "cyan")
        text.append("\n")
        text.append("    Path: ", "dim")
        text.append(str(current_venv.absolute()), "cyan")
        text.append("\n")
        text.append("    Status: ", "dim")
        if info["virtual_env"] and Path(info["virtual_env"]).samefile(
            current_venv
        ):
            text.append("✓ Active", "green")
        else:
            text.append("Not Active", "yellow")
    else:
        text.append("    Status: ", "dim")
        text.append("Not Found", "yellow")
    text.append("\n")

    panel = Panel.fit(
        text,
        title="Environment Information",
        title_align="left",
        border_style="bright_blue",
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@cli.command()
@click.argument("name", default="env")
def activate(name):
    """Activate the virtual environment"""
    venv_path = Path(name)
    activate_script = venv_path / "bin" / "activate"

    if not venv_path.exists():
        console.print(
            f"[red]Virtual environment '{name}' does not exist.[/red]"
        )
        return

    if not activate_script.exists():
        console.print(f"[red]Activation script not found in '{name}'.[/red]")
        return

    # Get current project name (directory name)
    project_name = Path.cwd().name
    venv_display = get_environment_display_name(venv_path)

    current_status = "No active environment"
    if "VIRTUAL_ENV" in os.environ:
        current_venv = Path(os.environ["VIRTUAL_ENV"])
        current_status = f"[cyan]{get_environment_display_name(current_venv)}{Path(current_venv).parent.name}[/cyan]"

    console.print(
        f"[yellow]Switching environment:[/yellow]\n"
        f"  From: {current_status}\n"
        f"  To:   [cyan]{venv_display}{project_name}[/cyan]"
    )
    shell, shell_name = get_current_shell()
    os.execl(
        shell,
        shell_name,
        "-c",
        f"source {activate_script} && exec {shell_name}",
    )


@cli.command()
def deactivate():
    """Deactivate the current virtual environment"""
    if "VIRTUAL_ENV" not in os.environ:
        console.print("[yellow]No active virtual environment found.[/yellow]")
        return

    current_venv = Path(os.environ["VIRTUAL_ENV"])
    project_name = current_venv.parent.name
    venv_display = get_environment_display_name(current_venv)

    console.print(
        f"[yellow]Deactivating environment:[/yellow]\n"
        f"  From: [cyan]{venv_display}{project_name}[/cyan]\n"
        f"  To:   No active environment"
    )
    shell, shell_name = get_current_shell()

    # If virtual environment folder doesn't exist, directly execute python -m venv deactivate
    if not current_venv.exists():
        os.execl(
            shell,
            shell_name,
            "-c",
            f"unset VIRTUAL_ENV && unset PYTHONHOME && export PATH=$(echo $PATH | tr ':' '\n' | grep -v {current_venv}/bin | tr '\n' ':' | sed 's/:$//') && exec {shell_name}",
        )
        return

    # If virtual environment folder exists, use the original method
    deactivate_script = current_venv / "bin" / "activate"
    os.execl(
        shell,
        shell_name,
        "-c",
        f"source {deactivate_script} && deactivate && exec {shell_name}",
    )


@cli.command()
@click.argument("packages", nargs=-1, required=True)
@click.option(
    "--version",
    "-v",
    help="Specific version to install (only works with single package)",
)
def add(packages, version: Optional[str]):
    """Add packages to requirements.txt and install them"""
    manager = PackageManager()
    if version and len(packages) > 1:
        console.print(
            "[yellow]Warning: Version option is ignored when installing multiple packages[/yellow]"
        )
        version = None

    failed_packages = []
    other_errors = []
    for package in packages:
        success, error = manager.add(package, version)
        if not success:
            if error == "version_not_found":
                failed_packages.append(package)
            elif error == "version_check_failed":
                other_errors.append((package, "Failed to verify installation"))
            elif error == "version_mismatch":
                other_errors.append(
                    (package, "Failed to install correct version")
                )
            else:
                other_errors.append((package, error))

    has_errors = False
    if failed_packages:
        has_errors = True
        # Get available versions for each failed package
        for package in failed_packages:
            if "==" in package:
                package_name, version = package.split("==")
            else:
                package_name = package
                version = None

            result = subprocess.run(
                ["pip", "index", "versions", package_name],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                versions = result.stdout.strip().split("\n")
                if len(versions) > 2:  # Skip header lines
                    # Get latest version from the first line
                    latest_version = versions[0].split("(")[-1].strip(")")
                    # Get closest versions
                    all_versions = []
                    for line in versions[1:]:
                        if "Available versions:" in line:
                            all_versions = (
                                line.split(":", 1)[1].strip().split(", ")[:5]
                            )
                            break
                    console.print(f"[red]✗ Failed to install {package}[/red]")
                    console.print(
                        f"[dim]Latest version: {latest_version}[/dim]"
                    )
                    if all_versions:
                        console.print(
                            f"[dim]Recent versions: {', '.join(all_versions)}[/dim]"
                        )
                    if package != failed_packages[-1]:
                        console.print("")

    if other_errors:
        has_errors = True
        for package, error in other_errors:
            console.print(f"[red]✗ {error}: {package}[/red]")

    if has_errors:
        sys.exit(1)


@cli.command()
@click.argument("packages", nargs=-1, required=True)
@click.option(
    "-y",
    is_flag=True,
    help="Automatically confirm all prompts",
)
def remove(packages, y: bool):
    """Remove packages from requirements.txt and uninstall them"""
    manager = PackageManager()
    for package in packages:
        manager.remove(package, auto_confirm=y)


# Add 'rm' as an alias for 'remove'
cli.add_command(remove, "rm")

# Add 'env' as an alias for 'venv'
cli.add_command(venv, "env")


@cli.command(name="list")
@click.option("-a", "--all", is_flag=True, help="List all installed packages")
@click.option("-t", "--tree", is_flag=True, help="Show dependency tree")
def list_packages(all, tree):
    """List installed packages and their dependencies"""
    pm = PackageManager()
    pm.list_packages(show_all=all, show_deps=tree)


@cli.command()
@click.option(
    "-y",
    is_flag=True,
    help="Automatically confirm all prompts",
)
def update(y: bool):
    """Update all packages to their latest versions"""
    manager = PackageManager()
    manager.update_all(auto_confirm=y)


# Add 'up' as an alias for 'update'
cli.add_command(update, "up")


@cli.command()
@click.option(
    "-y",
    is_flag=True,
    help="Automatically confirm all prompts",
)
def fix(y: bool):
    """Fix package inconsistencies"""
    pm = PackageManager()
    pm.fix_packages(auto_confirm=y)


@cli.command()
@click.option(
    "--test",
    is_flag=True,
    help="Publish to Test PyPI instead of PyPI",
)
def release(test: bool):
    """Build and publish package to PyPI or Test PyPI"""
    if not Path("pyproject.toml").exists():
        console.print("[red]No pyproject.toml found in current directory[/red]")
        return

    # Check if twine and build are installed
    required_packages = ["twine", "build"]
    need_install = []
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            need_install.append(pkg)

    # Install required packages
    if need_install:
        console.print("[blue]Installing required packages...[/blue]")
        for pkg in need_install:
            with console.status(
                f"[blue]Installing [cyan]{pkg}[/cyan]...[/blue]",
                spinner="dots",
            ) as status:
                process = subprocess.run(
                    ["pip", "install", pkg],
                    capture_output=True,
                    text=True,
                )
                if process.returncode != 0:
                    console.print(f"[red]Failed to install {pkg}:[/red]")
                    console.print(f"[red]{process.stderr}[/red]")
                    return
                console.print(f"[green]✓ Installed {pkg}[/green]")

    # Remove existing dist directory
    if Path("dist").exists():
        import shutil

        shutil.rmtree("dist")
        console.print("[green]✓ Removed existing dist directory[/green]")

    # Build package
    console.print("\n[blue]Building package...[/blue]")
    with console.status("[blue]Building...[/blue]", spinner="dots") as status:
        process = subprocess.run(
            ["python", "-m", "build"],
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            console.print("[red]Build failed:[/red]")
            console.print(f"[red]{process.stderr}[/red]")
            return
        console.print("[green]✓ Package built successfully[/green]")

    # Upload to PyPI or Test PyPI
    repo_flag = "--repository testpypi" if test else "--repository pypi"
    target = "Test PyPI" if test else "PyPI"

    # Read project info from pyproject.toml
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
        project_name = pyproject["project"]["name"]
        original_version = pyproject["project"]["version"]

    # For Test PyPI, use temporary test version
    if test:
        try:
            test_version = find_next_test_version(
                project_name, original_version
            )
            console.print(
                f"\n[blue]Using temporary version [cyan]{test_version}[/cyan] for Test PyPI...[/blue]"
            )
            update_version_in_pyproject(test_version)

            # Rebuild package with new version
            console.print(
                "\n[blue]Rebuilding package with test version...[/blue]"
            )
            with console.status(
                "[blue]Building...[/blue]", spinner="dots"
            ) as status:
                # Clean up dist directory first
                if Path("dist").exists():
                    import shutil

                    shutil.rmtree("dist")

                process = subprocess.run(
                    ["python", "-m", "build"],
                    capture_output=True,
                    text=True,
                )
                if process.returncode != 0:
                    console.print("[red]Build failed:[/red]")
                    console.print(f"[red]{process.stderr}[/red]")
                    # Restore original version before returning
                    update_version_in_pyproject(original_version)
                    return
                console.print("[green]✓ Package rebuilt successfully[/green]")
        except Exception as e:
            console.print("[red]Failed to update version number:[/red]")
            console.print(f"[red]{str(e)}[/red]")
            # Restore original version before returning
            update_version_in_pyproject(original_version)
            return

    console.print(f"\n[blue]Uploading to {target}...[/blue]")

    # Check if credentials exist in .pypirc
    pypirc_path = Path.home() / ".pypirc"
    has_credentials = False
    if pypirc_path.exists():
        with open(pypirc_path) as f:
            content = f.read()
            section = "testpypi" if test else "pypi"
            has_credentials = (
                f"[{section}]" in content and "password =" in content
            )

    if not has_credentials:
        console.print(
            f"\n[yellow]No saved credentials found for {target}[/yellow]"
        )
        if Confirm.ask(
            "Would you like to save your credentials for future use?"
        ):
            token = click.prompt("Enter your API token", hide_input=True)

            # Create or update .pypirc
            if pypirc_path.exists():
                with open(pypirc_path) as f:
                    current_config = f.read()

                # Parse existing config
                sections = {}
                current_section = None
                for line in current_config.splitlines():
                    line = line.strip()
                    if line.startswith("[") and line.endswith("]"):
                        current_section = line[1:-1]
                        sections[current_section] = []
                    elif line and current_section:
                        sections[current_section].append(line)

                # Update the target section
                section = "testpypi" if test else "pypi"
                sections[section] = [
                    "username = __token__",
                    f"password = {token}",
                ]

                # Reconstruct the config
                config = []
                for section_name, lines in sections.items():
                    config.append(f"[{section_name}]")
                    config.extend(lines)
                    config.append("")  # Empty line between sections
                config = "\n".join(config)
            else:
                # Create new config with only the required section
                section = "testpypi" if test else "pypi"
                config = f"""[{section}]
username = __token__
password = {token}
"""

            # Write the config file
            with open(pypirc_path, "w") as f:
                f.write(config.strip() + "\n")
            os.chmod(pypirc_path, 0o600)  # Set secure permissions
            console.print(
                f"[green]✓ Credentials saved to {pypirc_path}[/green]"
            )

    # Try uploading
    try:
        result = subprocess.run(
            f"twine upload {repo_flag} --verbose --disable-progress-bar dist/*",
            shell=True,
            capture_output=True,
            text=True,
            env={"PYTHONIOENCODING": "utf-8", **os.environ},
        )
    except Exception as e:
        console.print("[red]Upload failed:[/red]")
        console.print(f"[red]{str(e)}[/red]")
        if test:
            update_version_in_pyproject(original_version)
            console.print(
                f"[green]✓ Restored original version [cyan]{original_version}[/cyan][/green]"
            )
        return

    if result.returncode == 0:
        # Display success message with project info
        console.print(
            f"[green]✓ Package published successfully to {target}[/green]"
        )

        # Clean up dist directory
        if Path("dist").exists():
            import shutil

            shutil.rmtree("dist")
            console.print("[green]✓ Cleaned up dist directory[/green]")

        # Restore original version for Test PyPI
        if test:
            update_version_in_pyproject(original_version)
            console.print(
                f"[green]✓ Restored original version [cyan]{original_version}[/cyan][/green]"
            )

        # Generate URLs
        version_for_url = test_version if test else original_version
        if test:
            web_url = f"https://test.pypi.org/project/{project_name}/{version_for_url}"
            install_url = "https://test.pypi.org/simple/"
        else:
            web_url = (
                f"https://pypi.org/project/{project_name}/{version_for_url}"
            )
            install_url = "https://pypi.org/simple/"

        console.print(f"\n[cyan]Project Information:[/cyan]")
        console.print(f"  • Name: [bold cyan]{project_name}[/bold cyan]")
        console.print(f"  • Version: [bold cyan]{original_version}[/bold cyan]")
        if test:
            console.print(
                f"  • Test Version: [bold cyan]{test_version}[/bold cyan]"
            )
        console.print(f"  • URL: [link={web_url}][blue]{web_url}[/blue][/link]")

        if test:
            console.print("\n[yellow]To install from Test PyPI:[/yellow]")
            console.print(
                f"[cyan]pip install -i {install_url} {project_name}=={test_version}[/cyan]"
            )
        else:
            console.print("\n[yellow]To install:[/yellow]")
            console.print(
                f"[cyan]pip install {project_name}=={original_version}[/cyan]"
            )
    else:
        console.print(f"[red]✗ Upload to {target} failed[/red]")
        error_msg = result.stderr or result.stdout

        # Extract and format error messages
        error_lines = error_msg.splitlines()
        upload_info_shown = False
        has_error_details = False
        shown_messages = set()  # Track shown messages to avoid duplicates

        for line in error_lines:
            if not line.startswith(("[2K", "[?25")):  # Skip progress bar lines
                if line.strip():
                    # Skip HTML content and entity references
                    if (
                        any(
                            html_tag in line.lower()
                            for html_tag in [
                                "<html",
                                "</html>",
                                "<head",
                                "</head>",
                                "<body",
                                "</body>",
                                "<title",
                                "</title>",
                                "<h1",
                                "</h1>",
                                "<br",
                            ]
                        )
                        or "&#" in line
                        or "&quot;" in line
                        or "See http" in line
                    ):
                        continue

                    # Convert ANSI to plain text and clean up
                    clean_line = Text.from_ansi(line.strip()).plain

                    # Skip INFO lines in verbose output
                    if clean_line.startswith(("INFO", "See http")):
                        continue

                    # Skip lines with hash values
                    if any(
                        pattern in clean_line
                        for pattern in [
                            "blake2_256 hash",
                            "with hash",
                            "). See",
                        ]
                    ):
                        continue

                    # Handle version conflict errors
                    version_conflict_patterns = [
                        "File already exists",
                        "already exists",
                        "filename has already been used",
                        "filename is already registered",
                    ]

                    if (
                        any(
                            pattern in clean_line
                            for pattern in version_conflict_patterns
                        )
                        and "File already exists" not in shown_messages
                    ):
                        has_error_details = True
                        shown_messages.add("File already exists")
                        # Read current version from pyproject.toml
                        with open("pyproject.toml", "rb") as f:
                            current_version = tomllib.load(f)["project"][
                                "version"
                            ]

                        console.print(
                            "\n[yellow]This version has already been uploaded.[/yellow]"
                        )
                        console.print(
                            "1. Update the version number in pyproject.toml"
                        )
                        if test:
                            console.print(
                                "2. For testing, you can append [cyan].dev0[/cyan] to version"
                            )
                            console.print(
                                f"   Example: {current_version} -> {current_version}[cyan].dev0[/cyan]"
                            )
                        else:
                            console.print(
                                f"   Current version: {current_version}"
                            )
                        continue

                    if "Uploading" in clean_line and not upload_info_shown:
                        if "legacy" in clean_line:
                            continue  # Skip the legacy URL line
                        pkg_name = clean_line.split()[-1]
                        if pkg_name not in shown_messages:
                            console.print(
                                f"[blue]Uploading [cyan]{pkg_name}[/cyan][/blue]"
                            )
                            shown_messages.add(pkg_name)
                            upload_info_shown = True
                    elif (
                        "HTTPError:" in clean_line
                        or "Bad Request" in clean_line
                    ):
                        if (
                            "400 Bad Request" in clean_line
                            and "Upload rejected by server"
                            not in shown_messages
                        ):
                            has_error_details = True
                            shown_messages.add("Upload rejected by server")
                            console.print(
                                "[red]Upload rejected by server[/red]"
                            )
                            # Check common issues
                            if not test:
                                console.print("[yellow]Please verify:[/yellow]")
                                console.print(
                                    "1. Package name is registered on PyPI"
                                )
                                console.print(
                                    "2. You have the correct permissions"
                                )
                                console.print("3. Version number is unique")
                            else:
                                console.print(
                                    "Try a unique version number (e.g. append [cyan].dev0[/cyan])"
                                )
                        elif (
                            "403 Forbidden" in clean_line
                            and "Authentication failed" not in shown_messages
                        ):
                            has_error_details = True
                            shown_messages.add("Authentication failed")
                            console.print("[red]Authentication failed[/red]")
                            console.print("[yellow]Please check:[/yellow]")
                            if test:
                                console.print(
                                    "1. Create an account at Test PyPI:"
                                )
                                console.print(
                                    "[blue]https://test.pypi.org/account/register/[/blue]"
                                )
                                console.print("2. Generate a token at:")
                                console.print(
                                    "[blue]https://test.pypi.org/manage/account/#api-tokens[/blue]"
                                )
                                console.print(
                                    "3. Make sure you're using a Test PyPI token (not PyPI)"
                                )
                            else:
                                console.print(
                                    f"1. Your API token is correct for {target}"
                                )
                                console.print("2. Token has upload permissions")
                    elif (
                        "File already exists" in clean_line
                        and "File already exists" not in shown_messages
                    ):
                        has_error_details = True
                        shown_messages.add("File already exists")
                        # Read current version from pyproject.toml
                        with open("pyproject.toml", "rb") as f:
                            current_version = tomllib.load(f)["project"][
                                "version"
                            ]

                        console.print(
                            "\n[yellow]This version has already been uploaded.[/yellow]"
                        )
                        console.print(
                            "1. Update the version number in pyproject.toml"
                        )
                        if test:
                            console.print(
                                "2. For testing, you can append [cyan].dev0[/cyan] to version"
                            )
                            console.print(
                                f"   Example: {current_version} -> {current_version}[cyan].dev0[/cyan]"
                            )
                    elif not any(
                        skip in clean_line
                        for skip in [
                            "Uploading",
                            "WARNING",
                            "ERROR",
                            "See https://",
                            "information.",
                        ]
                    ):
                        if "error: " in clean_line.lower():
                            if clean_line not in shown_messages:
                                console.print(f"[red]{clean_line}[/red]")
                                shown_messages.add(clean_line)
                        elif clean_line not in shown_messages:
                            console.print(clean_line)
                            shown_messages.add(clean_line)

        if not has_error_details:
            console.print("\n[yellow]Additional troubleshooting:[/yellow]")
            if test:
                console.print(
                    "1. Register at Test PyPI: [blue link=https://test.pypi.org/account/register/]https://test.pypi.org/account/register/[/blue]"
                )
                console.print(
                    "2. Create a project: [blue link=https://test.pypi.org/manage/projects/]https://test.pypi.org/manage/projects/[/blue]"
                )
            console.print(f"3. Check your {target} account status")
            console.print("4. Verify package metadata in pyproject.toml")

        # Restore original version if test upload failed
        if test:
            update_version_in_pyproject(original_version)
            console.print(
                f"\n[green]✓ Restored original version [cyan]{original_version}[/cyan][/green]"
            )
        return

    # Clean up temporary packages
    if need_install:
        console.print("\n[blue]Cleaning up temporary packages...[/blue]")
        for pkg in need_install:
            with console.status(
                f"[blue]Removing [cyan]{pkg}[/cyan]...[/blue]",
                spinner="dots",
            ) as status:
                process = subprocess.run(
                    ["pip", "uninstall", "-y", pkg],
                    capture_output=True,
                    text=True,
                )
                if process.returncode == 0:
                    console.print(f"[green]✓ Removed {pkg}[/green]")
                else:
                    console.print(
                        f"[yellow]Warning: Failed to remove {pkg}[/yellow]"
                    )


if __name__ == "__main__":
    cli()
