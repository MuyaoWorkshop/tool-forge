---
description: Create a new tool by discovering solutions or building custom with Tool-Forge framework
---

## Context

- Current tool projects: !`ls .forge/ 2>/dev/null | grep -v scripts`

**Note:** The `.forge/` directory stores tool creation projects.

## Your Task

Guide user through complete tool creation workflow using Tool-Forge framework.

**Step 1: Requirement Analysis**

If this is a new requirement, gather details with `AskUserQuestion`:

```json
[
  {
    "question": "What category of tool do you need?",
    "header": "Category",
    "multiSelect": false,
    "options": [
      {
        "label": "Data processing",
        "description": "Transform, analyze, format data (JSON, CSV, etc.)"
      },
      {
        "label": "File operations",
        "description": "Manipulate files and directories (rename, organize, etc.)"
      },
      {
        "label": "Text processing",
        "description": "Parse, transform, analyze text content"
      },
      {
        "label": "Automation",
        "description": "Automate repetitive tasks or workflows"
      },
      {
        "label": "Other",
        "description": "Custom or specialized requirement"
      }
    ]
  },
  {
    "question": "Describe your requirement in detail:",
    "header": "Requirement",
    "multiSelect": false,
    "options": [
      {
        "label": "Simple",
        "description": "Single straightforward task, well-defined scope"
      },
      {
        "label": "Moderate",
        "description": "Multiple features or some complexity"
      },
      {
        "label": "Complex",
        "description": "Many features, requires careful design"
      }
    ]
  }
]
```

Then ask: "Please describe your requirement in 1-2 sentences: What problem does it solve? What's the input/output?"

**Step 2: Solution Discovery**

After requirement is clear:

1. Run: `python3 .forge/scripts/discover_solutions.py "<requirement>" "<category>"`
2. Parse JSON output to see discovered solutions
3. Present solutions to user in structured format

**Step 3: Solution Evaluation**

Guide user through systematic evaluation:

1. For each top solution, show 5-dimensional assessment
2. Create comparison table
3. Ask user to decide with `AskUserQuestion`:

```json
{
  "question": "Based on evaluation, what's your decision?",
  "header": "Decision",
  "multiSelect": false,
  "options": [
    {
      "label": "Use existing",
      "description": "Solution matches needs, will use directly"
    },
    {
      "label": "Customize existing",
      "description": "Good base but needs customization"
    },
    {
      "label": "Build new tool",
      "description": "No suitable solution found"
    }
  ]
}
```

**If choosing "Use existing" or "Customize existing":**
- Help user integrate/ customize
- Document usage
- Save to `.forge/<tool-name>/evaluation.md`
- Offer to create wrapper script for convenience

**If choosing "Build new tool":**
- Proceed to Step 4

**Step 4: Tool Development (if building)**

1. Run: `python3 .forge/scripts/init_tool_project.py "<tool-name>" "<requirement>" "<category>"`
2. Parse JSON output
3. Follow `llm_directive` to:
   - Select appropriate prompt template from `prompts/`
   - Guide user through AI collaboration
   - Implement with best practices

4. During development, use `AskUserQuestion` to check understanding:

```json
{
  "question": "How confident are you with this implementation?",
  "header": "Check-in",
  "multiSelect": false,
  "options": [
    {
      "label": "Confident",
      "description": "I understand how it works"
    },
    {
      "label": "It works but unsure",
      "description": "Need to understand better"
    },
    {
      "label": "Need help",
      "description": "Stuck or confused"
    }
  ]
}
```

5. Run quality checks: `python3 .forge/scripts/quality_check.py .forge/<tool-slug>`

**Step 5: Publication Preparation**

When tool is complete:

1. Run: `python3 .forge/scripts/publication_checklist.py .forge/<tool-slug>`
2. Guide user through checklist items
3. Ensure all checks pass
4. Help with:
   - GitHub release
   - Documentation
   - Installation testing
   - Community sharing

**Important:**

- Always start with solution discovery (never jump to coding)
- Use systematic evaluation for all solutions
- Build only when necessary
- Ensure publication readiness before sharing
- Document entire process for future reference

**Follow framework:**

- Three core principles (see system_prompts/tool-forge.md)
- Multi-dimensional evaluation
- Quality standards from guides/
- Publication checklist

**Success criteria:**
- Either: Best existing solution found and integrated
- Or: High-quality custom tool built and published that others can use conveniently
- Or: Customized existing solution documented and shared
