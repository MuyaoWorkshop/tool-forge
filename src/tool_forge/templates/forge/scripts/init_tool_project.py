#!/usr/bin/env python3
"""
Initialize a new tool project with standard structure and metadata.
"""

import os
import json
from datetime import datetime
from pathlib import Path


def init_tool_project(tool_name: str, requirement: str, category: str, base_dir: str = ".forge"):
    """
    Initialize a new tool project with directory structure and tracking files.

    Args:
        tool_name: Name of the tool
        requirement: Requirement description
        category: Tool category
        base_dir: Base directory for tool projects (default: .forge)
    """
    # Create base directory if it doesn't exist
    forge_dir = Path(base_dir)
    forge_dir.mkdir(exist_ok=True)

    # Create tool-specific directory
    tool_slug = tool_name.lower().replace(" ", "-").replace("_", "-")
    tool_dir = forge_dir / tool_slug

    if tool_dir.exists():
        print(json.dumps({
            "status": "error",
            "message": f"Tool '{tool_name}' already exists at {tool_dir}"
        }, indent=2))
        return str(tool_dir)

    tool_dir.mkdir(parents=True, exist_ok=True)

    # Create metadata
    metadata = {
        "tool_name": tool_name,
        "requirement": requirement,
        "category": category,
        "created_at": datetime.now().isoformat(),
        "status": "in_development",
        "publication_ready": False,
        "total_sessions": 0,
        "decisions": []
    }

    with open(tool_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Create requirement analysis
    with open(tool_dir / "requirement_analysis.md", "w") as f:
        f.write(f"# {tool_name} - Requirement Analysis\n\n")
        f.write("## Requirement\n\n")
        f.write(f"{requirement}\n\n")
        f.write("## Category\n\n")
        f.write(f"{category}\n\n")
        f.write("## Problem Statement\n\n")
        f.write("<!-- What problem does this tool solve? -->\n\n")
        f.write("## Input\n\n")
        f.write("<!-- What does the tool take as input? -->\n\n")
        f.write("## Output\n\n")
        f.write("<!-- What does the tool produce? -->\n\n")
        f.write("## Constraints\n\n")
        f.write("- <!-- Constraint 1 -->\n")
        f.write("- <!-- Constraint 2 -->\n\n")
        f.write("## Special Requirements\n\n")
        f.write("<!-- Any special requirements or edge cases -->\n\n")

    # Create development log
    with open(tool_dir / "development_log.md", "w") as f:
        f.write(f"# {tool_name} - Development Log\n\n")
        f.write("## Session Notes\n\n")
        f.write("<!-- Development progress will be logged here -->\n\n")

    # Create evaluation record (even if we're building, record why)
    with open(tool_dir / "evaluation.md", "w") as f:
        f.write(f"# {tool_name} - Solution Evaluation\n\n")
        f.write("## Existing Solutions Considered\n\n")
        f.write("### Solution A\n")
        f.write("- **Functionality**: ⭐⭐⭐\n")
        f.write("- **Quality**: ⭐⭐⭐\n")
        f.write("- **Usability**: ⭐⭐\n")
        f.write("- **Customization**: ⭐⭐\n")
        f.write("- **License**: ⭐⭐⭐\n")
        f.write("- **Decision**: <!-- Why not use this? -->\n\n")
        f.write("## Decision to Build\n\n")
        f.write("### Why Build?\n")
        f.write("<!-- Explain why existing solutions didn't meet needs -->\n\n")
        f.write("### Key Features Needed\n")
        f.write("- <!-- Feature 1 -->\n")
        f.write("- <!-- Feature 2 -->\n\n")

    # Create project structure template
    project_dir = tool_dir / "project"
    project_dir.mkdir()

    # Create basic README
    with open(project_dir / "README.md", "w") as f:
        f.write(f"# {tool_name}\n\n")
        f.write(f"{requirement}\n\n")
        f.write("## Installation\n\n")
        f.write("<!-- Installation instructions -->\n\n")
        f.write("## Usage\n\n")
        f.write("<!-- Usage examples -->\n\n")
        f.write("## Features\n\n")
        f.write("- <!-- Feature 1 -->\n")
        f.write("- <!-- Feature 2 -->\n\n")

    # Create pyproject.toml template
    with open(project_dir / "pyproject.toml", "w") as f:
        f.write('[build-system]\n')
        f.write('requires = ["setuptools>=61.0"]\n')
        f.write('build-backend = "setuptools.build_meta"\n\n')
        f.write('[project]\n')
        f.write(f'name = "{tool_slug}"\n')
        f.write('version = "0.1.0"\n')
        f.write(f'description = "{requirement}"\n')
        f.write('readme = "README.md"\n')
        f.write('requires-python = ">=3.8"\n')
        f.write('license = {text = "MIT"}\n\n')
        f.write('# Add your dependencies here\n')
        f.write('dependencies = [\n')
        f.write('    # "package>=version",\n')
        f.write(']\n\n')
        f.write('[project.scripts]\n')
        f.write(f'# {tool_slug} = "package.module:main_function"\n')

    # Create basic src structure
    src_dir = project_dir / "src" / tool_slug.replace("-", "_")
    src_dir.mkdir(parents=True)

    with open(src_dir / "__init__.py", "w") as f:
        f.write(f'"""\"\"\"{tool_name}\"\"\"\n\n')
        f.write('__version__ = "0.1.0"\n')
        f.write('"""')

    with open(src_dir / "main.py", "w") as f:
        f.write('"""Main module."""\n\n')
        f.write('def main():\n')
        f.write('    """Main entry point."""\n')
        f.write('    print("Hello from ' + tool_name + '!")\n\n')
        f.write('\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    main()\n')

    # Output structured JSON for LLM parsing
    output = {
        "status": "success",
        "tool_name": tool_name,
        "tool_slug": tool_slug,
        "directory": str(tool_dir),
        "project_directory": str(project_dir),
        "files_created": [
            "metadata.json",
            "requirement_analysis.md",
            "development_log.md",
            "evaluation.md",
            "project/README.md",
            "project/pyproject.toml",
            f"project/src/{tool_slug.replace('-', '_')}/__init__.py",
            f"project/src/{tool_slug.replace('-', '_')}/main.py"
        ],
        "next_action": "select_prompt_template",
        "llm_directive": (
            f"Tool project initialized at {project_dir}. "
            f"Now help user complete requirement_analysis.md, then select appropriate prompt template "
            f"from /home/wanps/Projects/tool-forge/prompts/{category.lower()}/ "
            f"to guide AI collaboration for development. "
            f"Ask user to explain their requirement clearly first, then match to best template."
        ),
        "suggested_response": (
            f"✅ Tool project '{tool_name}' initialized!\n\n"
            f"Location: {tool_dir}\n\n"
            f"Next steps:\n"
            f"1. Complete requirement analysis\n"
            f"2. Select prompt template\n"
            f"3. Start AI collaboration for development\n"
        )
    }

    print(json.dumps(output, indent=2))
    return str(tool_dir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python3 init_tool_project.py <tool_name> <requirement> <category> [base_dir]")
        print("\nExample: python3 init_tool_project.py 'photo-renamer' 'batch rename photos' 'File operations'")
        sys.exit(1)

    tool_name = sys.argv[1]
    requirement = sys.argv[2]
    category = sys.argv[3]
    base_dir = sys.argv[4] if len(sys.argv) > 4 else ".forge"

    init_tool_project(tool_name, requirement, category, base_dir)
