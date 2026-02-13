#!/usr/bin/env python3
"""
Run quality checks on a tool project to ensure it meets standards.
"""

import json
import sys
from pathlib import Path
import subprocess


def check_project_structure(project_dir: Path) -> dict:
    """Check basic project structure."""
    checks = {
        "has_readme": (project_dir / "README.md").exists(),
        "has_pyproject": (project_dir / "pyproject.toml").exists(),
        "has_license": (project_dir / "LICENSE").exists(),
        "has_src": (project_dir / "src").exists(),
        "has_tests": (project_dir / "tests").exists() or (project_dir / "test").exists()
    }
    return checks


def check_documentation(project_dir: Path) -> dict:
    """Check documentation quality."""
    readme = project_dir / "README.md"

    if not readme.exists():
        return {"readme_exists": False, "readme_complete": False}

    content = readme.read_text()

    checks = {
        "readme_exists": True,
        "has_installation": "installation" in content.lower(),
        "has_usage": "usage" in content.lower() or "example" in content.lower(),
        "has_features": "feature" in content.lower(),
        "readme_complete": all([
            "installation" in content.lower(),
            ("usage" in content.lower() or "example" in content.lower()),
            "feature" in content.lower()
        ])
    }
    return checks


def check_code_style(project_dir: Path) -> dict:
    """Check code style with pycodestyle if available."""
    src_dir = project_dir / "src"

    if not src_dir.exists():
        return {"style_checkable": False}

    try:
        result = subprocess.run(
            ["pycodestyle", str(src_dir)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "style_checkable": True,
            "style_issues": result.returncode != 0,
            "style_output": result.stdout if result.returncode != 0 else ""
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {"style_checkable": False, "style_check_skipped": True}


def run_quality_check(tool_dir: str) -> dict:
    """
    Run comprehensive quality checks on a tool project.

    Args:
        tool_dir: Path to tool directory (e.g., .forge/my-tool)

    Returns:
        Quality check results
    """
    tool_path = Path(tool_dir)
    project_dir = tool_path / "project"

    if not project_dir.exists():
        return {
            "status": "error",
            "message": f"Project directory not found: {project_dir}"
        }

    # Run all checks
    structure_checks = check_project_structure(project_dir)
    doc_checks = check_documentation(project_dir)
    style_checks = check_code_style(project_dir)

    # Calculate overall score
    all_checks = {
        **structure_checks,
        **doc_checks,
        **style_checks
    }

    critical_checks = [
        structure_checks.get("has_readme", False),
        structure_checks.get("has_pyproject", False),
        structure_checks.get("has_license", False),
    ]

    score = sum(1 for k, v in all_checks.items()
                if isinstance(v, bool) and v) / len(all_checks)

    output = {
        "status": "success",
        "tool_dir": str(tool_dir),
        "project_dir": str(project_dir),
        "score": round(score * 100, 1),
        "checks": all_checks,
        "critical": all(critical_checks),
        "recommendations": [],
        "next_action": "address_issues" if not all(critical_checks) else "proceed_to_publication",
        "llm_directive": (
            f"Quality score: {round(score * 100, 1)}%. "
            f"Review checks and help user address any critical issues. "
            f"Once all critical checks pass, proceed to publication checklist."
        )
    }

    # Add recommendations
    if not structure_checks.get("has_readme"):
        output["recommendations"].append("Add README.md with installation and usage")
    if not structure_checks.get("has_pyproject"):
        output["recommendations"].append("Create pyproject.toml for installability")
    if not structure_checks.get("has_license"):
        output["recommendations"].append("Add LICENSE file (recommend MIT)")
    if not doc_checks.get("readme_complete"):
        output["recommendations"].append("Complete README with installation, usage, features")
    if not structure_checks.get("has_tests"):
        output["recommendations"].append("Add basic tests for core functionality")
    if style_checks.get("style_issues"):
        output["recommendations"].append("Fix code style issues (run: pycodestyle src/)")

    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 quality_check.py <tool_dir>")
        print("\nExample: python3 quality_check.py .forge/my-tool")
        sys.exit(1)

    tool_dir = sys.argv[1]
    run_quality_check(tool_dir)
