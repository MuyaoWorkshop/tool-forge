#!/usr/bin/env python3
"""
Tool-Forge CLI - One-time installer for Claude Code tool creation system.

Usage:
    uv tool run tool-forge init
    tool-forge
"""

import sys
import shutil
import inquirer
import json
from pathlib import Path
from typing import Dict, Any
import importlib.resources

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

BANNER = f"""{Colors.CYAN}
╔════════════════════════════════════════╗
║   _____       _ _   _     _     ___  _ ║
║  |_   _| __ _| | | / /   / /   / _ \\(_)║
║    | || (_| | |   V  V /   | | /| | |║
║   |___\\__,_|_|  _/\\_\\_\\   |_|\\_\\_,_|_║
║                                          ║
║  Tool Creation System v3.0                ║
╚════════════════════════════════════════╝
{Colors.RESET}"""

def print_success(msg: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_info(msg: str) -> None:
    """Print info message in cyan."""
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")

def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET}  {msg}")

def print_header(msg: str) -> None:
    """Print header message in bold magenta."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}{msg}{Colors.RESET}")

def print_dim(msg: str) -> None:
    """Print dimmed message."""
    print(f"{Colors.DIM}{msg}{Colors.RESET}")

def print_error(msg: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def get_templates_dir() -> Path:
    """Get templates directory from installed package or source fallback."""
    import importlib.resources as resources

    # Method 1: Try importlib.resources first (for installed packages)
    try:
        # Check if we can access templates as package data
        if resources.is_resource("tool_forge", "templates"):
            try:
                # Python 3.9+ method
                with resources.files("tool_forge") as pkg_dir:
                    templates_path = Path(pkg_dir) / "templates"
                    if templates_path.exists():
                        return templates_path
            except (AttributeError, TypeError):
                # Python 3.7-3.8 fallback
                with resources.path("tool_forge", "templates") as templates_path:
                    return Path(templates_path)
    except Exception:
        pass

    # Method 2: Fallback to source directory (for editable installs)
    # This ensures tool works during development
    return Path(__file__).parent.parent / "templates"


def create_or_update_settings(claude_dir: Path) -> None:
    """Create or update .claude/settings.local.json."""
    settings_file = claude_dir / "settings.local.json"

    # Default settings for Tool-Forge
    default_settings = {
        "permissions": {
            "allow": [
                "Bash(python3 .forge/scripts/*)",
                "Bash(ls:*)",
                "Read(.forge/**)",
                "Write(.forge/**)",
                "Write(**/*.md)",
                "Read(**/*.md)"
            ],
            "deny": [
                "Bash(rm:*)",
                "Bash(curl:*)",
                "Read(.env)",
                "Read(.env.*)",
                "Write(.env)",
                "Write(.env.*)"
            ]
        },
        "companyAnnouncements": [
            "🔨 Tool-Forge is active! Use /create to start tool creation",
            "",
            "📋 Tool-Forge workflow:",
            "  1. Describe your tool requirement",
            "  2. Review existing solutions (AI will search)",
            "  3. Decide: Use existing / Customize / Build new",
            "  4. Develop with AI assistance (if building)",
            "  5. Publish and share with community",
            "",
            "💡 Run 'tool-forge init' to reinitialize",
            "📖 Run 'tool-forge --help' for more info"
        ]
    }

    if settings_file.exists():
        # Load existing settings
        with open(settings_file, "r") as f:
            settings = json.load(f)

        # Merge with defaults
        if "permissions" not in settings:
            settings["permissions"] = default_settings["permissions"]
        else:
            # Merge permissions allow list
            if "allow" not in settings["permissions"]:
                settings["permissions"]["allow"] = []

            for perm in default_settings["permissions"]["allow"]:
                if perm not in settings["permissions"]["allow"]:
                    settings["permissions"]["allow"].append(perm)

            # Merge permissions deny list
            if "deny" not in settings["permissions"]:
                settings["permissions"]["deny"] = []

            for perm in default_settings["permissions"]["deny"]:
                if perm not in settings["permissions"]["deny"]:
                    settings["permissions"]["deny"].append(perm)

        # Add company announcements if not present
        if "companyAnnouncements" not in settings:
            settings["companyAnnouncements"] = default_settings["companyAnnouncements"]

        print_success(f"Updated {settings_file}")
    else:
        # Create new settings file
        settings = default_settings
        print_success(f"Created {settings_file}")

    # Write settings
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)


def check_initialization() -> bool:
    """Check if project has been initialized."""
    config_path = Path.cwd() / ".forge" / "config.json"
    if not config_path.exists():
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("initialized", False)
    except:
        return False


def init_project() -> None:
    """Initialize Tool-Forge in current project."""

    cwd = Path.cwd()
    templates_dir = get_templates_dir()

    # Get current project name for display
    project_name = cwd.name

    print_header(f"\nInitializing Tool-Forge in {project_name}...\n")

    # Create .claude directory structure
    claude_dir = cwd / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Copy system prompts
    system_prompts_dest = claude_dir / "system_prompts"
    system_prompts_dest.mkdir(exist_ok=True)
    system_prompts_src = templates_dir / "claude" / "system_prompts"

    if system_prompts_src.exists():
        for file in system_prompts_src.glob("*.md"):
            shutil.copy2(file, system_prompts_dest / file.name)
            print_success(f"Copied system prompt: {file.name}")

    # Copy commands
    commands_dest = claude_dir / "commands"
    commands_dest.mkdir(exist_ok=True)
    commands_src = templates_dir / "claude" / "commands"

    if commands_src.exists():
        for file in commands_src.glob("*.md"):
            shutil.copy2(file, commands_dest / file.name)
            print_success(f"Copied command: {file.name}")

    # Copy agents (optional)
    agents_dest = claude_dir / "agents"
    agents_dest.mkdir(exist_ok=True)
    agents_src = templates_dir / "claude" / "agents"

    if agents_src.exists():
        for file in agents_src.glob("*.md"):
            shutil.copy2(file, agents_dest / file.name)
            print_success(f"Copied agent: {file.name}")

    # Create/update settings.local.json
    create_or_update_settings(claude_dir)

    # Create .forge directory structure
    forge_dir = cwd / ".forge"
    forge_dir.mkdir(exist_ok=True)

    # Create scripts directory
    scripts_dest = forge_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = templates_dir / "forge" / "scripts"

    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            # Make executable
            (scripts_dest / file.name).chmod(0o755)
            print_success(f"Copied script: {file.name}")

    # Copy .gitignore for .forge
    gitignore_src = templates_dir / "forge" / ".gitignore"
    gitignore_dest = forge_dir / ".gitignore"

    if gitignore_src.exists():
        shutil.copy2(gitignore_src, gitignore_dest)
        print_success("Created .forge/.gitignore")

    # Create config.json with initialization flag
    config = {
        "initialized": True,
        "version": "3.0.0"
    }
    config_path = forge_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print_success(f"Created config.json (Version: 3.0.0)")

    print(f"\n{Colors.GREEN}{Colors.BOLD}Initialization complete!{Colors.RESET}\n")

    print_header("Available commands in Claude Code:")
    print(f"  {Colors.CYAN}/create{Colors.RESET}              - Create a new tool")
    print()
    print_info(f"{project_name} is now ready for tool creation:")
    print("  1. 🔍 Requirement Analysis")
    print("  2. 🌐 Solution Discovery")
    print("  3. 📊 Solution Evaluation")
    print("  4. 🎯 Decision (Use/Customize/Build)")
    print("  5. 🔨 Development (if needed)")
    print("  6. ✅ Publication")
    print()


def launch_coch() -> None:
    """Launch Claude Code with tool-forge system prompt."""
    import subprocess

    # Get path to system prompt template
    templates_dir = get_templates_dir()
    system_prompt_path = templates_dir / "claude" / "system_prompts" / "tool-forge.md"

    if not system_prompt_path.exists():
        print_error("Error: System prompt not found")
        print_dim(f"Expected at: {system_prompt_path}")
        sys.exit(1)

    # Read system prompt content (skip frontmatter)
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip frontmatter (between --- lines)
    in_frontmatter = False
    content_lines = []
    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                continue
        if not in_frontmatter:
            content_lines.append(line)

    system_prompt = "".join(content_lines).strip()

    # Launch Claude Code with system prompt
    print_info("Launching Claude Code in tool creation coach mode...")
    print_dim("(Using Tool-Forge framework system prompt)\n")

    cmd = ["claude", "--system-prompt", system_prompt]

    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print_error("Error: 'claude' command not found")
        print_dim("Make sure Claude Code CLI is installed and in your PATH")
        print_dim("Install from: https://claude.ai/download")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    # Check for explicit commands
    if len(sys.argv) >= 2:
        command = sys.argv[1]

        if command == "init":
            init_project()
            return
        elif command == "version":
            from tool_forge import __version__
            print(f"tool-forge version {__version__}")
            return
        elif command in ["help", "--help", "-h"]:
            print("Tool-Forge - Systematic tool creation with AI assistance\n")
            print("Usage:")
            print("  tool-forge           Auto-init and launch Claude Code")
            print("  tool-forge init      Force re-initialization")
            print("  tool-forge version    Show version")
            print()
            print("For more info: https://github.com/MuyaoWorkshop/tool-forge")
            return
        else:
            print_error(f"Unknown command: {command}")
            print_dim("Run 'tool-forge --help' for usage")
            sys.exit(1)

    # Default behavior: check init, then launch
    if not check_initialization():
        print_info("First-time setup detected. Initializing...")
        print()
        init_project()
        print()
        print_header("Launching Claude Code with Tool-Forge framework...")
        print()
        launch_coch()
    else:
        print_info("Launching Claude Code in tool creation coach mode...")
        print_dim("(Use /create to start tool creation)\n")
        launch_coch()


if __name__ == "__main__":
    main()
