#!/usr/bin/env python3
"""
Discover existing solutions for a given requirement using multiple search strategies.
Outputs structured JSON for LLM evaluation.
"""

import json
import subprocess
from pathlib import Path
from typing import List, Dict
import re


def search_github(keywords: str) -> List[Dict]:
    """
    Search GitHub for repositories matching keywords.

    Args:
        keywords: Search keywords

    Returns:
        List of repositories with metadata
    """
    try:
        # Use gh CLI if available
        result = subprocess.run(
            ["gh", "search", "repos", keywords, "--limit", "10", "--json", "name,description,stargazerCount,url,primaryLanguage"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            repos = json.loads(result.stdout)
            return [
                {
                    "name": repo["name"],
                    "description": repo.get("description", "No description"),
                    "stars": repo.get("stargazerCount", 0),
                    "url": repo["url"],
                    "language": repo.get("primaryLanguage", "Unknown"),
                    "source": "GitHub"
                }
                for repo in repos[:5]  # Top 5
            ]
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    return []


def search_pypi(keywords: str) -> List[Dict]:
    """
    Search PyPI for packages matching keywords.

    Args:
        keywords: Search keywords

    Returns:
        List of packages with metadata
    """
    try:
        # Use pip search if available (note: pip search is deprecated, may need alternative)
        result = subprocess.run(
            ["pip", "search", keywords],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            packages = []
            for line in result.stdout.split('\n')[:5]:
                # Parse pip search output format: "package-name (version) : description"
                match = re.match(r'(\S+)\s+\(([^)]+)\)\s*:\s*(.*)', line)
                if match:
                    packages.append({
                        "name": match.group(1),
                        "version": match.group(2),
                        "description": match.group(3),
                        "url": f"https://pypi.org/project/{match.group(1)}/",
                        "source": "PyPI"
                    })
            return packages
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return []


def suggest_manual_search_strategies(requirement: str, category: str) -> List[str]:
    """
    Suggest manual search strategies for the user.

    Args:
        requirement: User's requirement
        category: Tool category

    Returns:
        List of search strategies with example queries
    """
    strategies = [
        f"Google: '{requirement} open source tool'",
        f"Google: '{requirement} github'",
        f"Google: 'best {category.lower()} tools {requirement}'",
        f"GitHub: Search with '{requirement.split()[0]}'",
        f"Awesome lists: 'awesome-{category.lower()}' on GitHub"
    ]

    if category == "Data processing":
        strategies.extend([
            "PyPI: Search for data processing libraries",
            "Check: pandas, polars, dask documentation"
        ])
    elif category == "File operations":
        strategies.extend([
            "Check: pathlib, shutil documentation",
            "Search: 'file automation' on GitHub"
        ])
    elif category == "Text processing":
        strategies.extend([
            "Check: regex, nltk, spacy documentation",
            "Search: 'text processing' on PyPI"
        ])

    return strategies


def discover_solutions(requirement: str, category: str) -> Dict:
    """
    Discover existing solutions using multiple strategies.

    Args:
        requirement: User's requirement description
        category: Tool category

    Returns:
        Structured output with discovered solutions
    """
    # Extract keywords from requirement
    keywords = requirement.split()[0] if requirement else "tool"

    # Search different sources
    github_repos = search_github(requirement)
    pypi_packages = search_pypi(keywords)

    # Combine results
    all_solutions = []

    for repo in github_repos:
        all_solutions.append({
            "type": "GitHub Repository",
            "name": repo["name"],
            "description": repo["description"],
            "metrics": {
                "stars": repo["stars"],
                "language": repo["language"]
            },
            "url": repo["url"],
            "source": "GitHub"
        })

    for pkg in pypi_packages:
        all_solutions.append({
            "type": "Python Package",
            "name": pkg["name"],
            "description": pkg["description"],
            "metrics": {
                "version": pkg["version"]
            },
            "url": pkg["url"],
            "source": "PyPI"
        })

    # If automated search found nothing, suggest manual strategies
    manual_strategies = suggest_manual_search_strategies(requirement, category) if not all_solutions else []

    # Output structured JSON
    output = {
        "status": "success",
        "requirement": requirement,
        "category": category,
        "solutions_found": len(all_solutions),
        "solutions": all_solutions,
        "manual_search_strategies": manual_strategies,
        "next_action": "evaluate_solutions",
        "llm_directive": (
            f"Found {len(all_solutions)} potential solutions. "
            f"Present these to user and guide systematic evaluation using 5-dimensional assessment. "
            f"If no automated results, show manual search strategies and help user search. "
            f"After evaluation, ask user to decide: use existing / customize / build new."
        ),
        "evaluation_criteria": {
            "functionality": "How well does it match requirements?",
            "quality": "Is it mature and well-maintained?",
            "usability": "How easy is it to use?",
            "customization": "Can it be customized if needed?",
            "license": "Is the license suitable for your use case?"
        }
    }

    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 discover_solutions.py <requirement> <category>")
        print("\nExample: python3 discover_solutions.py 'batch rename photos' 'File operations'")
        sys.exit(1)

    requirement = sys.argv[1]
    category = sys.argv[2]

    discover_solutions(requirement, category)
