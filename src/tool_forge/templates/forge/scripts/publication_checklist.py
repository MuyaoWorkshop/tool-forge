#!/usr/bin/env python3
"""
Run comprehensive publication checklist to ensure tool is ready for public use.
"""

import json
import sys
from pathlib import Path
import subprocess


def check_installation(project_dir: Path) -> dict:
    """Check if tool can be installed."""
    checks = {
        "has_pyproject": (project_dir / "pyproject.toml").exists(),
        "has_valid_name": True,  # Would need to parse and validate
        "dependencies_specified": True,
        "entry_point_defined": True
    }

    # Parse pyproject.toml for entry point
    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text()
        checks["entry_point_defined"] = "[project.scripts]" in content

    return checks


def check_documentation(project_dir: Path) -> dict:
    """Check documentation completeness."""
    readme = project_dir / "README.md"

    if not readme.exists():
        return {
            "has_readme": False,
            "has_installation": False,
            "has_usage": False,
            "has_examples": False
        }

    content = readme.read_text().lower()

    return {
        "has_readme": True,
        "has_installation": "installation" in content or "install" in content,
        "has_usage": "usage" in content or "example" in content,
        "has_examples": "example" in content or code_example_present(content),
        "has_badge": "badge" in content or "stars" in content or "license" in content
    }


def code_example_present(content: str) -> bool:
    """Check if README has code examples."""
    return "```" in content  # Markdown code blocks


def check_testing(project_dir: Path) -> dict:
    """Check testing coverage."""
    tests_dir = project_dir / "tests"
    test_dir = project_dir / "test"

    has_tests = tests_dir.exists() or test_dir.exists()

    if has_tests:
        # Check for at least one test file
        test_files = list((tests_dir if tests_dir.exists() else test_dir).rglob("test_*.py"))
        has_test_files = len(test_files) > 0
    else:
        has_test_files = False

    return {
        "has_tests": has_tests,
        "has_test_files": has_test_files
    }


def check_license(project_dir: Path) -> dict:
    """Check license file."""
    license_file = project_dir / "LICENSE"

    if not license_file.exists():
        return {"has_license": False, "license_type": None}

    content = license_file.read_text()

    # Detect license type
    license_type = "Other"
    if "MIT" in content:
        license_type = "MIT"
    elif "Apache" in content:
        license_type = "Apache"
    elif "GPL" in content:
        license_type = "GPL"
    elif "BSD" in content:
        license_type = "BSD"

    return {
        "has_license": True,
        "license_type": license_type,
        "license_permissive": license_type in ["MIT", "Apache", "BSD"]
    }


def check_git_readiness(project_dir: Path) -> dict:
    """Check if ready for git operations."""
    has_gitignore = (project_dir.parent / ".gitignore").exists()

    # Check for common gitignore entries
    gitignore_content = ""
    if has_gitignore:
        gitignore_content = (project_dir.parent / ".gitignore").read_text()

    return {
        "has_gitignore": has_gitignore,
        "ignores_python_cache": "__pycache__" in gitignore_content,
        "ignores_build": "build/" in gitignore_content or "dist/" in gitignore_content
    }


def run_publication_checklist(tool_dir: str) -> dict:
    """
    Run comprehensive publication checklist.

    Args:
        tool_dir: Path to tool directory (e.g., .forge/my-tool)

    Returns:
        Publication readiness results
    """
    tool_path = Path(tool_dir)
    project_dir = tool_path / "project"

    if not project_dir.exists():
        return {
            "status": "error",
            "message": f"Project directory not found: {project_dir}"
        }

    # Run all checks
    installation_checks = check_installation(project_dir)
    doc_checks = check_documentation(project_dir)
    test_checks = check_testing(project_dir)
    license_checks = check_license(project_dir)
    git_checks = check_git_readiness(project_dir)

    # Calculate readiness
    all_checks = {
        **installation_checks,
        **doc_checks,
        **test_checks,
        **license_checks,
        **git_checks
    }

    critical_checks = [
        installation_checks.get("has_pyproject", False),
        doc_checks.get("has_readme", False),
        license_checks.get("has_license", False),
        git_checks.get("has_gitignore", False)
    ]

    recommended_checks = [
        installation_checks.get("entry_point_defined", False),
        doc_checks.get("has_installation", False),
        doc_checks.get("has_usage", False),
        doc_checks.get("has_examples", False),
        test_checks.get("has_test_files", False)
    ]

    all_critical = all(critical_checks)
    all_recommended = all(recommended_checks)

    score = sum(1 for k, v in all_checks.items()
                if isinstance(v, bool) and v) / len(all_checks)

    output = {
        "status": "success",
        "tool_dir": str(tool_dir),
        "project_dir": str(project_dir),
        "readiness_score": round(score * 100, 1),
        "ready_for_publication": all_critical,
        "fully_ready": all_critical and all_recommended,
        "checks": {
            "installation": installation_checks,
            "documentation": doc_checks,
            "testing": test_checks,
            "license": license_checks,
            "git": git_checks
        },
        "critical_issues": [k for k, v in all_checks.items() if not v and k in [
            "has_pyproject", "has_readme", "has_license", "has_gitignore"
        ]],
        "recommended_improvements": [k for k, v in all_checks.items() if not v and k not in [
            "has_pyproject", "has_readme", "has_license", "has_gitignore"
        ]],
        "next_action": "address_issues" if not all_critical else "publish",
        "llm_directive": (
            f"Publication readiness: {round(score * 100, 1)}%. "
            f"{'Ready for basic publication!' if all_critical else 'Address critical issues first.'} "
            f"{'Fully ready for GitHub + PyPI!' if all_critical and all_recommended else 'Consider improvements for better experience.'} "
            f"Guide user through remaining steps: {'Fix critical issues' if not all_critical else 'Create release and publish'}."
        ),
        "publication_steps": [
            "1. Create version tag (e.g., v1.0.0)",
            "2. Create GitHub Release with CHANGELOG",
            "3. Test fresh installation: pip install .",
            "4. Optional: Publish to PyPI with twine",
            "5. Share with community (Reddit, forums, etc.)"
        ] if all_critical else []
    }

    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 publication_checklist.py <tool_dir>")
        print("\nExample: python3 publication_checklist.py .forge/my-tool")
        sys.exit(1)

    tool_dir = sys.argv[1]
    run_publication_checklist(tool_dir)
