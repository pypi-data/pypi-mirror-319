# Package management functionality providing dependency handling and requirements.txt management
from pathlib import Path
import subprocess
import os
from typing import Dict, Optional, Set
from rich.console import Console
from rich.table import Table
from rich.text import Text
import pkg_resources
from rich.prompt import Confirm
import sys
import time
import importlib
import importlib.metadata
from packaging.requirements import Requirement
from rich.style import Style
from .utils import get_current_shell
from rich.panel import Panel

console = Console()


def normalize_package_name(name: str) -> str:
    """
    Normalize package name by converting both hyphen and underscore to hyphen
    """
    return name.lower().replace("_", "-")


def get_system_packages() -> Set[str]:
    """
    Get a set of known system packages that should be excluded from analysis
    """
    return {
        "pip",
        "setuptools",
        "wheel",
        "pkg-resources",
        "distribute",
        "six",
        "distlib",
        "packaging",
        "pyparsing",
    }


def get_package_dependencies(package_name: str) -> Set[str]:
    """
    Get direct dependencies for a package
    """
    try:
        dist = importlib.metadata.distribution(package_name)
        direct_deps = set()

        if dist.requires:
            for req in dist.requires:
                try:
                    req_obj = Requirement(req)
                    dep_name = normalize_package_name(req_obj.name)
                    # Only add dependency if it's installed
                    try:
                        importlib.metadata.distribution(dep_name)
                        direct_deps.add(dep_name)
                    except importlib.metadata.PackageNotFoundError:
                        continue
                except:
                    continue

        return direct_deps
    except importlib.metadata.PackageNotFoundError:
        return set()


def get_top_level_packages() -> Set[str]:
    """
    Get packages that were explicitly installed by user
    (packages not required by other packages, excluding system packages)
    """
    # Get system packages to exclude
    system_pkgs = get_system_packages()

    # Get all installed packages except system packages
    all_packages = {
        normalize_package_name(dist.metadata["Name"])
        for dist in importlib.metadata.distributions()
        if normalize_package_name(dist.metadata["Name"]) not in system_pkgs
    }

    all_dependencies = set()
    for pkg in all_packages:
        all_dependencies.update(get_package_dependencies(pkg))

    # Top level packages are those that are not dependencies of any other package
    return all_packages - all_dependencies


def get_venv_site_packages(python_path: str) -> str:
    """
    Get site-packages directory from Python interpreter
    """
    try:
        cmd = [
            python_path,
            "-c",
            "import site; print(site.getsitepackages()[0])",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to get site-packages path: {e}")


def switch_virtual_env(venv_path: str) -> None:
    """
    Switch to specified virtual environment
    """
    python_path = os.path.join(venv_path, "bin", "python")
    if not os.path.exists(python_path):
        raise ValueError(f"Python executable not found: {python_path}")

    site_packages = get_venv_site_packages(python_path)
    if not os.path.exists(site_packages):
        raise ValueError(f"Site-packages directory not found: {site_packages}")

    # Remove all existing site-packages from sys.path
    sys.path = [p for p in sys.path if "site-packages" not in p]

    # Add the virtual environment's site-packages at the beginning
    sys.path.insert(0, site_packages)

    # Clear all existing distributions cache
    importlib.metadata.MetadataPathFinder.invalidate_caches()
    importlib.reload(importlib.metadata)


class PackageManager:
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.requirements_file = self.project_root / "requirements.txt"
        self._installed_packages_cache = None
        self._dependencies_cache = {}
        self.venv_dir = self.project_root / "env"

        # Switch to virtual environment if exists
        if self.venv_dir.exists():
            try:
                switch_virtual_env(str(self.venv_dir))
            except Exception as e:
                console.print(
                    f"[yellow]Warning: Failed to switch virtual environment: {e}[/yellow]"
                )

    def _parse_requirements(self) -> Dict[str, str]:
        """Parse requirements.txt into a dictionary of package names and versions"""
        if not self.requirements_file.exists():
            return {}

        packages = {}
        with open(self.requirements_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Handle different requirement formats
                    if "==" in line:
                        name, version = line.split("==")
                        packages[name] = f"=={version}"
                    elif ">=" in line:
                        name, version = line.split(">=")
                        packages[name] = f">={version}"
                    elif "<=" in line:
                        name, version = line.split("<=")
                        packages[name] = f"<={version}"
                    else:
                        packages[line] = ""
        return packages

    def _write_requirements(self, packages: Dict[str, str]):
        """Write packages to requirements.txt"""
        with open(self.requirements_file, "w") as f:
            for name, version in sorted(packages.items()):
                f.write(f"{name}{version}\n")

    def _get_installed_version(self, package: str) -> Optional[str]:
        """Get installed version of a package using pip list"""
        try:
            result = subprocess.run(
                ["pip", "list", "--format=json"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json

                for pkg in json.loads(result.stdout):
                    if pkg["name"].lower() == package.lower():
                        return pkg["version"]
            return None
        except Exception:
            # Fallback to pkg_resources
            try:
                return pkg_resources.get_distribution(package).version
            except pkg_resources.DistributionNotFound:
                return None

    def _check_pip_upgrade(self, stderr: str):
        """Check if pip needs upgrade and handle it"""
        if "new release of pip is available" in stderr:
            if Confirm.ask(
                "[yellow]A new version of pip is available. Do you want to upgrade?[/yellow]"
            ):
                console.print("[yellow]Upgrading pip...[/yellow]")
                result = subprocess.run(
                    ["pip", "install", "--upgrade", "pip"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    console.print("[green]✓ Pip has been upgraded[/green]")
                else:
                    console.print(
                        f"[red]Failed to upgrade pip:[/red]\n{result.stderr}"
                    )

    def _check_package_exists(self, package: str) -> bool:
        """Check if package exists on PyPI"""
        try:
            result = subprocess.run(
                (
                    ["pip", "search", package]
                    if sys.version_info < (3, 7)
                    else ["pip", "index", "versions", package]
                ),
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _parse_version_from_pip_output(
        self, output: str, package: str
    ) -> Optional[str]:
        """Parse version from pip output"""
        for line in output.split("\n"):
            if f"Requirement already satisfied: {package}" in line:
                parts = line.split()
                if (
                    len(parts) >= 6
                ):  # Format: "Requirement already satisfied: package in path (version)"
                    version = parts[-1].strip("()")
                    return version
        return None

    def add(self, package: str, version: Optional[str] = None) -> bool:
        """Add a package to requirements.txt and install it"""
        if not Path(os.environ.get("VIRTUAL_ENV", "")).exists():
            console.print(
                "[red bold]No active virtual environment found.[/red bold]"
            )
            return False

        # Create requirements.txt if it doesn't exist
        if not self.requirements_file.exists():
            self.requirements_file.touch()
            console.print("[blue]Created requirements.txt[/blue]")

        packages = self._parse_requirements()

        try:
            # First check if pip needs upgrade
            result = subprocess.run(
                ["pip", "--version"], capture_output=True, text=True
            )
            if result.stderr:
                self._check_pip_upgrade(result.stderr)

            # Check if package is already installed
            pre_installed_version = self._get_installed_version(package)
            if pre_installed_version:
                # If version is specified and different from installed
                if version and version != pre_installed_version:
                    main_status = f"[yellow]Installing [cyan]{package}[/cyan]==[white]{version}[/white]..."
                    with console.status(main_status, spinner="dots") as status:
                        cmd = ["pip", "install", f"{package}=={version}"]
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            bufsize=1,
                            universal_newlines=True,
                        )

                        while True:
                            output = process.stdout.readline()
                            if output == "" and process.poll() is not None:
                                break
                            if output:
                                # Check for dependency installation messages
                                if "Collecting" in output:
                                    dep = output.split()[1].strip()
                                    if dep != package:
                                        status.update(
                                            f"{main_status}\n[dim]Installing dependency: {dep}[/dim]"
                                        )

                        _, stderr = process.communicate()
                        if process.returncode != 0:
                            console.print(
                                f"[red bold]Failed to update [cyan]{package}[/cyan]:[/red bold]\n{stderr}"
                            )
                            return False

                    installed_version = version
                else:
                    installed_version = pre_installed_version
            else:
                # Install new package
                cmd = ["pip", "install"]
                if version:
                    cmd.append(f"{package}=={version}")
                else:
                    cmd.append(package)

                main_status = f"[yellow]Installing [cyan]{package}[/cyan]..."
                with console.status(main_status, spinner="dots") as status:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                    )

                    while True:
                        output = process.stdout.readline()
                        if output == "" and process.poll() is not None:
                            break
                        if output:
                            # Check for dependency installation messages
                            if "Collecting" in output:
                                dep = output.split()[1].strip()
                                if dep != package:
                                    status.update(
                                        f"{main_status}\n[dim]Installing dependency: {dep}[/dim]"
                                    )

                    _, stderr = process.communicate()

                    if "already satisfied" in stderr:
                        # Try to get version from pip output first
                        installed_version = self._parse_version_from_pip_output(
                            stderr, package
                        )
                        if not installed_version:
                            installed_version = self._get_installed_version(
                                package
                            )

                        if not installed_version:
                            console.print(
                                f"[red bold]Failed to determine version for [cyan]{package}[/cyan][/red bold]"
                            )
                            return False
                    else:
                        if process.returncode != 0:
                            console.print(
                                f"[red bold]Failed to install [cyan]{package}[/cyan]:[/red bold]\n{stderr}"
                            )
                            return False

                        installed_version = self._get_installed_version(package)
                        if not installed_version:
                            console.print(
                                f"[red bold]Package [cyan]{package}[/cyan] was not installed correctly.[/red bold]"
                            )
                            return False

            # Only update requirements.txt if we have a valid version
            if installed_version:
                packages[package] = f"=={installed_version}"
                self._write_requirements(packages)
                console.print(
                    f"[green]✓ Added {package}=={installed_version}[/green]"
                )
                return True
            return False

        except Exception as e:
            console.print(
                f"[red bold]Error installing [cyan]{package}[/cyan]:[/red bold]\n{str(e)}"
            )
            return False

    def _get_all_dependencies_recursive(
        self, package: str, seen=None
    ) -> Set[str]:
        """Get all dependencies (including dependencies of dependencies) for a package"""
        if seen is None:
            seen = set()

        if package in seen:
            return set()

        seen.add(package)
        deps = get_package_dependencies(package)
        all_deps = deps.copy()

        for dep in deps:
            all_deps.update(self._get_all_dependencies_recursive(dep, seen))

        return all_deps

    def remove(self, package: str) -> bool:
        """Remove a package from requirements.txt and uninstall it"""
        if not Path(os.environ.get("VIRTUAL_ENV", "")).exists():
            console.print("[red]No active virtual environment found.[/red]")
            return False

        packages = self._parse_requirements()
        normalized_package = normalize_package_name(package)

        # Find the package in requirements.txt (case-insensitive)
        package_to_remove = None
        for pkg in packages:
            if normalize_package_name(pkg) == normalized_package:
                package_to_remove = pkg
                break

        if not package_to_remove:
            console.print(
                f"[yellow]Package {package} not found in requirements.txt[/yellow]"
            )
            return False

        try:
            # Get all dependencies recursively (including dependencies of dependencies)
            deps_to_remove = self._get_all_dependencies_recursive(
                package_to_remove
            )

            # Get all installed packages except the one being removed
            all_packages = {
                name: version
                for name, version in self._get_all_installed_packages().items()
                if normalize_package_name(name) != normalized_package
            }

            # Get all dependencies of other packages recursively
            used_deps = set()
            for pkg in all_packages:
                if (
                    pkg in packages
                ):  # Only check dependencies of packages in requirements.txt
                    pkg_deps = self._get_all_dependencies_recursive(pkg)
                    used_deps.update(pkg_deps)

            # Filter out dependencies that are used by other packages
            deps_to_remove = {
                dep
                for dep in deps_to_remove
                if normalize_package_name(dep)
                not in {normalize_package_name(d) for d in used_deps}
            }

            main_status = (
                f"[yellow]Removing [cyan]{package_to_remove}[/cyan]..."
            )
            with console.status(main_status, spinner="dots") as status:
                # Prepare all packages to remove
                all_to_remove = [package_to_remove] + sorted(deps_to_remove)

                # Show what will be removed
                if deps_to_remove:
                    status.update(
                        f"{main_status}\n[dim]Will also remove: {', '.join(sorted(deps_to_remove))}[/dim]"
                    )
                    time.sleep(
                        1
                    )  # Give user a moment to see what will be removed

                # Remove all packages in one command
                process = subprocess.Popen(
                    ["pip", "uninstall", "-y"] + all_to_remove,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                while True:
                    output = process.stdout.readline()
                    if output == "" and process.poll() is not None:
                        break
                    if output:
                        # Show uninstall progress
                        if "Removing" in output:
                            pkg = output.split()[-1].strip()
                            if pkg != package_to_remove:
                                status.update(
                                    f"{main_status}\n[dim]Removing: {pkg}[/dim]"
                                )

                _, stderr = process.communicate()
                if process.returncode != 0:
                    console.print(
                        f"[red]Failed to uninstall packages:[/red]\n{stderr}"
                    )
                    return False

            del packages[package_to_remove]
            self._write_requirements(packages)
            # Reset caches when removing package
            self._installed_packages_cache = None
            self._dependencies_cache = {}

            if deps_to_remove:
                console.print(
                    f"[green]✓ Removed {package_to_remove} and {len(deps_to_remove)} unused dependencies[/green]"
                )
            else:
                console.print(f"[green]✓ Removed {package_to_remove}[/green]")
            return True

        except Exception as e:
            console.print(
                f"[red]Error removing {package_to_remove}:[/red]\n{str(e)}"
            )
            return False

    def _get_all_installed_packages(self) -> Dict[str, str]:
        """Get all installed packages and their versions"""
        if self._installed_packages_cache is not None:
            return self._installed_packages_cache

        packages = {}
        try:
            # Get system packages to exclude
            system_pkgs = get_system_packages()

            # Get all installed packages
            for dist in importlib.metadata.distributions():
                name = dist.metadata["Name"]
                normalized_name = normalize_package_name(name)
                # Skip system packages, pip, and development package
                if (
                    normalized_name not in system_pkgs
                    and not normalized_name.startswith(
                        ("pip-", "setuptools-", "wheel-")
                    )
                    and normalized_name != "pymin"
                ):
                    packages[name] = dist.version
        except Exception as e:
            console.print(
                f"[yellow]Warning: Error getting installed packages: {e}[/yellow]"
            )

        self._installed_packages_cache = packages
        return packages

    def _get_package_dependencies(self, package: str) -> Dict[str, list]:
        """Get package dependencies using importlib.metadata"""
        if package in self._dependencies_cache:
            return self._dependencies_cache[package]

        try:
            dist = importlib.metadata.distribution(package)
            deps = {
                "requires": [],
                "required_by": [],
            }

            if dist.requires:
                for req in dist.requires:
                    try:
                        req_obj = Requirement(req)
                        dep_name = req_obj.name
                        # Only add dependency if it's installed
                        try:
                            importlib.metadata.distribution(dep_name)
                            deps["requires"].append(dep_name)
                        except importlib.metadata.PackageNotFoundError:
                            continue
                    except:
                        continue

            self._dependencies_cache[package] = deps
            return deps
        except Exception:
            empty_deps = {"requires": [], "required_by": []}
            self._dependencies_cache[package] = empty_deps
            return empty_deps

    def _get_all_main_packages(self) -> Dict[str, str]:
        """Get all installed main packages (not dependencies) and their versions"""
        installed = (
            self._get_all_installed_packages()
        )  # This already filters out pymin
        main_packages = {}

        # First, add all packages from requirements.txt
        req_packages = self._parse_requirements()
        for pkg in req_packages:
            main_packages[pkg] = installed.get(pkg, "")

        # Get top level packages using importlib.metadata
        try:
            # Get all installed packages except system packages and pymin
            all_packages = {
                normalize_package_name(dist.metadata["Name"]): dist.version
                for dist in importlib.metadata.distributions()
                if normalize_package_name(dist.metadata["Name"])
                not in get_system_packages()
                and normalize_package_name(dist.metadata["Name"]) != "pymin"
            }

            all_dependencies = set()
            for pkg in all_packages:
                all_dependencies.update(get_package_dependencies(pkg))

            # Add packages that are not dependencies
            for name, version in all_packages.items():
                if name not in main_packages and name not in all_dependencies:
                    main_packages[name] = version

        except Exception as e:
            console.print(
                f"[yellow]Warning: Could not get direct dependencies: {e}[/yellow]"
            )

        return main_packages

    def _get_original_package_name(self, name: str) -> str:
        """Get original package name from installed distributions"""
        try:
            normalized_name = normalize_package_name(name)
            for dist in importlib.metadata.distributions():
                if (
                    normalize_package_name(dist.metadata["Name"])
                    == normalized_name
                ):
                    return dist.metadata["Name"]
        except Exception:
            pass
        return name

    def _normalize_package_name(self, name: str) -> str:
        """Normalize package name for comparison"""
        return normalize_package_name(name)

    def _get_canonical_package_name(self, name: str) -> str:
        """Get the canonical package name from installed distributions"""
        try:
            normalized_name = normalize_package_name(name)
            if self._installed_packages_cache is None:
                self._installed_packages_cache = (
                    self._get_all_installed_packages()
                )

            # Find the package name with correct casing and format
            for pkg_name in self._installed_packages_cache:
                if normalize_package_name(pkg_name) == normalized_name:
                    return pkg_name
        except Exception:
            pass
        return name

    def _build_dependency_tree(self, package: str, seen=None) -> dict:
        """Build a dependency tree for a package"""
        if seen is None:
            seen = set()

        normalized_package = normalize_package_name(package)

        # First check if the package itself is installed
        try:
            dist = importlib.metadata.distribution(normalized_package)
            version = dist.version
        except importlib.metadata.PackageNotFoundError:
            return {}  # Return empty dict if package is not installed

        if normalized_package in {normalize_package_name(p) for p in seen}:
            return {
                "circular": True,
                "version": version,
            }  # Include version even for circular dependencies

        seen.add(package)
        tree = {"version": version}  # Add version to the tree node

        try:
            deps = get_package_dependencies(
                package
            )  # This already filters uninstalled packages
            for dep in deps:
                canonical_name = self._get_canonical_package_name(dep)
                if normalize_package_name(canonical_name) not in {
                    normalize_package_name(p) for p in seen
                }:
                    # Recursively build tree for installed dependencies
                    subtree = self._build_dependency_tree(canonical_name, seen)
                    if subtree:  # Only add if the dependency exists
                        tree[canonical_name] = subtree
        except Exception:
            pass

        return tree

    def _get_package_status(
        self, name: str, required_version: str, installed_version: str
    ) -> str:
        """Get package status with consistent logic across all views"""
        if required_version:
            if not installed_version:
                return "[red]✗[/red]"  # Most severe: Not installed
            elif required_version.startswith(
                "=="
            ) and installed_version != required_version.lstrip("=="):
                return "[yellow]≠[/yellow]"  # Version mismatch
            return "[green]✓[/green]"  # Installed and matches requirements
        elif installed_version:
            return "[blue]△[/blue]"  # Installed but not in requirements.txt
        return "[red]✗[/red]"  # Not installed

    def list_packages(
        self,
        show_all: bool = False,
        show_deps: bool = False,
        fix: bool = False,
        auto_fix: bool = False,
    ):
        """List packages in requirements.txt and/or all installed packages"""
        # Check virtual environment status
        venv_active = bool(os.environ.get("VIRTUAL_ENV"))
        current_venv = Path("env")
        current_venv_exists = current_venv.exists() and current_venv.is_dir()

        if not venv_active:
            console.print(
                "\n[red bold]⚠ Warning: No active virtual environment![/red bold]"
            )
            if current_venv_exists:
                console.print(
                    "[yellow]A virtual environment exists but is not activated.[/yellow]"
                )
                # 建構原本的指令參數
                cmd_args = ["pm", "list"]
                if show_all:
                    cmd_args.append("-a")
                if show_deps:
                    cmd_args.append("-t")
                if fix:
                    cmd_args.append("-f")
                if auto_fix:
                    cmd_args.append("-F")
                cmd = " ".join(cmd_args)

                if Confirm.ask(
                    f"\n[yellow]Do you want to activate the environment and run '[cyan]{cmd}[/cyan]'?[/yellow]"
                ):
                    shell, shell_name = get_current_shell()
                    activate_script = current_venv / "bin" / "activate"
                    os.execl(
                        shell,
                        shell_name,
                        "-c",
                        f"source {activate_script} && {cmd} && exec {shell_name}",
                    )
                    return
            else:
                console.print(
                    "[yellow]No virtual environment found in current directory.[/yellow]"
                )
                console.print("[yellow]Run: pm venv[/yellow]")
                return

        if fix or auto_fix:
            return self.fix_packages(auto_fix)

        req_packages = self._parse_requirements()
        installed_packages = (
            self._get_all_installed_packages()
        )  # This already filters out pymin

        # Convert package names to canonical form
        req_packages = {
            self._get_canonical_package_name(name): version
            for name, version in req_packages.items()
        }
        installed_packages = {
            self._get_canonical_package_name(name): version
            for name, version in installed_packages.items()
        }

        # Get main packages
        if show_deps:
            packages_to_show = (
                self._get_all_main_packages()
            )  # This already filters out pymin
        elif show_all:
            packages_to_show = installed_packages  # This already filters out pymin and system packages
        else:
            packages_to_show = (
                self._get_all_main_packages()
            )  # This already filters out pymin

        # Convert packages_to_show to canonical form
        packages_to_show = {
            self._get_canonical_package_name(name): version
            for name, version in packages_to_show.items()
        }

        if not packages_to_show:
            console.print("[yellow]No packages found[/yellow]")
            return

        # Create table
        table = Table(
            title="Package Dependencies",
            show_header=True,
            header_style="bold magenta",
            title_justify="left",
            expand=False,
        )

        if show_deps:
            table.add_column("Package Tree", style="cyan", no_wrap=True)
            table.add_column("Required", style="blue")
            table.add_column("Installed", style="cyan")
            table.add_column("Status", justify="right")

            # Build all trees at once with progress bar
            trees = {}
            package_list = sorted(packages_to_show.keys())
            with console.status(
                "[yellow]Building dependency tree...[/yellow]",
                spinner="dots",
            ) as status:
                # Build trees
                for i, name in enumerate(package_list):
                    status.update(
                        f"[yellow]Building dependency tree... ({i + 1}/{len(package_list)})[/yellow]"
                    )
                    if name in installed_packages:
                        trees[name] = self._build_dependency_tree(name)
                    elif (
                        name in req_packages
                    ):  # Add uninstalled but required packages
                        trees[name] = {}

                # Format trees with progress indicator
                status.update("[yellow]Formatting dependency tree...[/yellow]")
                for name in sorted(trees.keys()):

                    def format_tree(
                        pkg: str,
                        tree: dict,
                        level: int = 0,
                        last_sibling=True,
                        prefix="",
                    ) -> None:
                        # Get package information
                        pkg_required = req_packages.get(pkg, "")
                        pkg_installed = tree.get("version") if tree else None
                        pkg_status = self._get_package_status(
                            pkg, pkg_required, pkg_installed
                        )

                        # Create tree branches
                        if level > 0:
                            branch = "└── " if last_sibling else "├── "
                            display_name = f"{prefix}{branch}{pkg}"
                            if tree.get("circular"):
                                display_name += " [dim](circular)[/dim]"
                        else:
                            display_name = pkg

                        # Format display values
                        required_display = (
                            pkg_required.lstrip("=")
                            if pkg_required
                            else "[yellow]None[/yellow]" if level == 0 else ""
                        )

                        # Dim the display for dependencies
                        if level > 0:
                            display_name = f"[dim]{display_name}[/dim]"
                            if pkg_installed:
                                pkg_installed = f"[dim]{pkg_installed}[/dim]"
                            pkg_status = f"[dim]{pkg_status}[/dim]"

                        # Add row to table
                        table.add_row(
                            display_name,
                            required_display,
                            pkg_installed or "[yellow]None[/yellow]",
                            pkg_status,
                        )

                        # Process dependencies recursively
                        if not tree.get("circular"):
                            deps = [
                                (k, v)
                                for k, v in sorted(tree.items())
                                if k not in ("circular", "version")
                            ]
                            for i, (dep, subtree) in enumerate(deps):
                                new_prefix = prefix + (
                                    "    " if last_sibling else "│   "
                                )
                                format_tree(
                                    dep,
                                    subtree,
                                    level + 1,
                                    i == len(deps) - 1,
                                    new_prefix,
                                )

                    format_tree(name, trees[name])
                    if name != sorted(trees.keys())[-1]:
                        table.add_row("", "", "", "")

            # Count total dependencies
            total_deps = 0
            direct_deps = 0
            for tree in trees.values():

                def count_deps(tree_node):
                    if tree_node.get("circular"):
                        return 0
                    return len(
                        [
                            k
                            for k in tree_node.keys()
                            if k not in ("circular", "version")
                        ]
                    )

                def count_all_deps(tree_node):
                    if tree_node.get("circular"):
                        return 0
                    count = 0
                    for k, v in tree_node.items():
                        if k not in ("circular", "version"):
                            count += 1 + count_all_deps(v)
                    return count

                direct_deps += count_deps(tree)
                total_deps += count_all_deps(tree)

        else:
            table.add_column("Package", style="")
            table.add_column("Required", style="blue")
            table.add_column("Installed", style="cyan")
            table.add_column("Status", justify="right")

            # Get main packages for checking
            main_packages = self._get_all_main_packages()

            for name in sorted(packages_to_show.keys()):
                required_version = req_packages.get(name, "")
                installed_version = installed_packages.get(name)
                status = self._get_package_status(
                    name, required_version, installed_version
                )

                # Dim the display if it's not a main package
                if name not in main_packages:
                    name = f"[dim]{name}[/dim]"
                    if installed_version:
                        installed_version = f"[dim]{installed_version}[/dim]"
                    status = f"[dim]{status}[/dim]"

                table.add_row(
                    name,
                    (
                        required_version.lstrip("=")
                        if required_version
                        else ("" if show_all else "[yellow]None[/yellow]")
                    ),
                    installed_version or "[yellow]None[/yellow]",
                    status,
                )
        console.print(table)

        # 顯示統計摘要
        total_packages = len(packages_to_show)
        missing_count = sum(
            1
            for name in packages_to_show
            if name in req_packages and name not in installed_packages
        )
        unlisted_count = sum(
            1
            for name in packages_to_show
            if name not in req_packages and name in installed_packages
        )
        mismatch_count = sum(
            1
            for name in packages_to_show
            if name in req_packages
            and name in installed_packages
            and req_packages[name].lstrip("==") != installed_packages[name]
        )
        installed_count = sum(
            1
            for name in packages_to_show
            if name in installed_packages
            and name in req_packages
            and req_packages[name].lstrip("==") == installed_packages[name]
        )

        console.print("\nSummary:")
        console.print(f"  • Total Packages: [cyan]{total_packages}[/cyan]")
        if installed_count:
            console.print(
                f"  • Installed & Matched (✓): [green]{installed_count}[/green]"
            )
        if mismatch_count:
            console.print(
                f"  • Version Mismatches (≠): [yellow]{mismatch_count}[/yellow]"
            )
        if missing_count:
            console.print(f"  • Not Installed (✗): [red]{missing_count}[/red]")
        if unlisted_count:
            console.print(
                f"  • Not in requirements.txt (△): [blue]{unlisted_count}[/blue]"
            )
        if show_deps and total_deps:
            console.print(
                f"  • Total Dependencies: [dim]{total_deps}[/dim] (Direct: [dim]{direct_deps}[/dim])"
            )

        if mismatch_count or missing_count:
            console.print(
                "\n[dim]Tip: Run 'pm list --fix' to resolve package inconsistencies[/dim]"
            )
            python_path = os.path.join(self.venv_dir, "bin", "python")
            site_packages = get_venv_site_packages(python_path)
            console.print(
                f"\n[dim]Environment Information:\n"
                f"  Python Executable: {self._format_path_highlight(python_path)}\n"
                f"  Site Packages: {self._format_path_highlight(site_packages)}[/dim]"
            )

    def fix_packages(self, auto_fix: bool = False) -> bool:
        """Fix package inconsistencies:
        1. Install missing packages from requirements.txt
        2. Add installed packages to requirements.txt
        3. Fix version mismatches
        """
        req_packages = self._parse_requirements()
        installed_packages = self._get_all_installed_packages()
        fixed = False

        # Group issues by type
        missing_packages = []  # in requirements.txt but not installed
        unlisted_packages = []  # installed but not in requirements.txt
        version_mismatches = []  # version doesn't match requirements.txt

        for name, req_version in req_packages.items():
            if name not in installed_packages:
                missing_packages.append((name, req_version.lstrip("==")))
            elif req_version and installed_packages[name] != req_version.lstrip(
                "=="
            ):
                version_mismatches.append(
                    (name, req_version.lstrip("=="), installed_packages[name])
                )

        # Get directly installed packages using pip
        try:
            result = subprocess.run(
                ["pip", "list", "--not-required", "--format=json"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json

                for pkg in json.loads(result.stdout):
                    name = pkg["name"]
                    if name not in req_packages and not (
                        name.lower() in ("pip", "setuptools", "wheel")
                        or name.startswith(("pip-", "setuptools-", "wheel-"))
                    ):
                        unlisted_packages.append((name, pkg["version"]))
        except Exception:
            pass

        # Display issues
        if not (missing_packages or unlisted_packages or version_mismatches):
            console.print("[green]✓ No package inconsistencies found[/green]")
            return True

        # Build the panel content
        text = Text()

        if missing_packages:
            text.append(
                "\nNot Installed (✗):\n", style=Style(color="red", bold=True)
            )
            for name, version in missing_packages:
                text.append("  ", style=Style(color="red"))
                text.append("✗", style=Style(color="red"))
                text.append(" ")
                text.append(name, style=Style(color="white"))
                text.append("==", style=Style(dim=True))
                text.append(version, style=Style(color="white"))
                text.append("\n")

        if version_mismatches:
            text.append(
                "\nVersion Mismatches (≠):\n",
                style=Style(color="yellow", bold=True),
            )
            for name, req_version, inst_version in version_mismatches:
                text.append("  ", style=Style(color="yellow"))
                text.append("≠", style=Style(color="yellow"))
                text.append(" ")
                text.append(name, style=Style(color="white"))
                text.append(": ", style=Style(dim=True))
                text.append(inst_version, style=Style(color="red"))
                text.append(" (installed)", style=Style(dim=True))
                text.append(" → ", style=Style(dim=True))
                text.append(req_version, style=Style(color="green"))
                text.append(" (required)", style=Style(dim=True))
                text.append("\n")

        if unlisted_packages:
            text.append(
                "\nNot in requirements.txt (△):\n",
                style=Style(color="blue", bold=True),
            )
            for name, version in unlisted_packages:
                text.append("  ", style=Style(color="blue"))
                text.append("△", style=Style(color="blue"))
                text.append(" ")
                text.append(name, style=Style(color="white"))
                text.append("==", style=Style(dim=True))
                text.append(version, style=Style(color="white"))
                text.append("\n")

        # Show summary of actions
        text.append("\nActions to be taken:\n", style=Style(bold=True))
        if missing_count := len(missing_packages):
            text.append("  • Install ")
            text.append(str(missing_count), style=Style(color="red"))
            text.append(" missing package(s)\n")
        if mismatch_count := len(version_mismatches):
            text.append("  • Update ")
            text.append(str(mismatch_count), style=Style(color="yellow"))
            text.append(" package version(s)\n")
        if unlisted_count := len(unlisted_packages):
            text.append("  • Add ")
            text.append(str(unlisted_count), style=Style(color="blue"))
            text.append(" package(s) to requirements.txt\n")

        # Display the panel
        panel = Panel.fit(
            text,
            title="Package Inconsistencies",
            title_align="left",
            border_style="bright_blue",
        )
        console.print("\n")
        console.print(panel)
        console.print("\n")

        # Auto-fix or ask for confirmation
        if not auto_fix:
            if not Confirm.ask("Do you want to fix these issues?"):
                return False
        else:
            console.print(
                "[yellow]Auto-fixing package inconsistencies...[/yellow]"
            )

        with console.status(
            "[yellow]Fixing package inconsistencies...[/yellow]", spinner="dots"
        ) as status:
            # Fix version mismatches first (to avoid dependency conflicts)
            for name, req_version, _ in version_mismatches:
                main_status = f"[yellow]Updating [white]{name}[/yellow] to [white]{req_version}[/white]..."
                status.update(main_status)
                try:
                    process = subprocess.Popen(
                        ["pip", "install", f"{name}=={req_version}"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                    )

                    while True:
                        output = process.stdout.readline()
                        if output == "" and process.poll() is not None:
                            break
                        if output:
                            # Check for dependency installation messages
                            if "Collecting" in output:
                                dep = output.split()[1].strip()
                                if dep != name:
                                    status.update(
                                        f"{main_status}\n[dim]Installing dependency: {dep}[/dim]"
                                    )

                    _, stderr = process.communicate()
                    if process.returncode != 0:
                        console.print(
                            f"\n[red]Failed to update {name}:[/red]\n{stderr}"
                        )
                        if not auto_fix:
                            if not Confirm.ask(
                                "Continue with remaining updates?"
                            ):
                                return False
                    else:
                        fixed = True
                except Exception as e:
                    console.print(
                        f"\n[red]Error updating {name}:[/red]\n{str(e)}"
                    )
                    if not auto_fix:
                        if not Confirm.ask("Continue with remaining updates?"):
                            return False

            # Fix missing packages
            for name, version in missing_packages:
                main_status = f"[yellow]Installing [white]{name}[/yellow]==[white]{version}[/white]..."
                status.update(main_status)
                try:
                    process = subprocess.Popen(
                        ["pip", "install", f"{name}=={version}"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                    )

                    while True:
                        output = process.stdout.readline()
                        if output == "" and process.poll() is not None:
                            break
                        if output:
                            # Check for dependency installation messages
                            if "Collecting" in output:
                                dep = output.split()[1].strip()
                                if dep != name:
                                    status.update(
                                        f"{main_status}\n[dim]Installing dependency: {dep}[/dim]"
                                    )

                    _, stderr = process.communicate()
                    if process.returncode != 0:
                        console.print(
                            f"\n[red]Failed to install {name}:[/red]\n{stderr}"
                        )
                        if not auto_fix:
                            if not Confirm.ask(
                                "Continue with remaining installations?"
                            ):
                                return False
                    else:
                        fixed = True
                except Exception as e:
                    console.print(
                        f"\n[red]Error installing {name}:[/red]\n{str(e)}"
                    )
                    if not auto_fix:
                        if not Confirm.ask(
                            "Continue with remaining installations?"
                        ):
                            return False

            # Add unlisted packages to requirements.txt
            if unlisted_packages:
                status.update("[yellow]Updating requirements.txt...[/yellow]")
                try:
                    packages = self._parse_requirements()
                    for name, version in unlisted_packages:
                        packages[name] = f"=={version}"
                    self._write_requirements(packages)
                    fixed = True
                except Exception as e:
                    console.print(
                        f"\n[red]Error updating requirements.txt:[/red]\n{str(e)}"
                    )
                    return False

        if fixed:
            console.print("\n[green]✓ All issues have been fixed[/green]")
        return fixed

    def _format_path_highlight(self, full_path: str) -> str:
        """Format path to highlight the important parts"""
        try:
            # Convert to Path object for easier manipulation
            path = Path(full_path)
            # Get the home directory
            home = Path.home()

            if str(path).startswith(str(home)):
                # If path starts with home directory, replace with ~
                path = Path(str(path).replace(str(home), "~", 1))
                base = ""
            else:
                # For other paths, keep the root
                base = path.anchor
                path = path.relative_to(path.anchor)

            # Split the path parts
            parts = list(path.parts)

            # Get virtual env path from self.venv_dir
            venv = self.venv_dir
            if str(venv).startswith(str(home)):
                venv = Path(str(venv).replace(str(home), "~", 1))
            else:
                venv = venv.relative_to(venv.anchor)

            # Get the virtual env directory name
            venv_parts = list(venv.parts)

            # Find where the virtual env path starts in our target path
            for i in range(len(parts)):
                if "/".join(parts[i:]).startswith("/".join(venv_parts)):
                    # Highlight from virtual env onwards with cyan and italic
                    parts = parts[:i] + [
                        f"[cyan italic]{'/'.join(parts[i:])}[/cyan italic]"
                    ]
                    break

            return base + "/".join(parts)
        except Exception:
            # Fallback to original path if any error occurs
            return full_path
