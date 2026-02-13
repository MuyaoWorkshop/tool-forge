# Tool-Forge v3.0 - CLI Tool System

## 🎯 Three Core Principles

### 1️⃣ Prioritize Existing Excellent Solutions

**Why**: Avoid reinventing the wheel, use industry best practices

**Implementation**:
- ✅ Complete solution discovery process (GitHub, PyPI, Awesome lists)
- ✅ Multi-dimensional assessment standards (5 dimensions, 5-star scale)
- ✅ Clear decision matrix
- ✅ Real example comparisons

### 2️⃣ Build Complete When Necessary

**Why**: Ensure tool quality and meet specific needs

**Implementation**:
- ✅ Polished prompt engineering
- ✅ AI collaboration best practices
- ✅ Quality assurance checklist
- ✅ Iterative improvement process

### 3️⃣ Ensure Others Can Use

**Why**: Tool value lies in shareability and reusability

**Implementation**:
- ✅ Complete publication checklist (50+ items)
- ✅ Multi-platform compatibility
- ✅ Clear documentation
- ✅ Easy installation
- ✅ Open source license

---

## 📂 Directory Structure

```
tool-forge/
├── src/tool_forge/              # Source code (CLI tool)
│   ├── cli/
│   │   └── main.py              # CLI entry point
│   └── templates/               # Template files
│       ├── claude/              # Claude config
│       │   ├── system_prompts/
│       │   │   └── tool-forge.md
│       │   ├── commands/
│       │   │   └── create.md
│       │   └── agents/
│       └── forge/              # Tool-Forge scripts
│           └── scripts/
│               ├── discover_solutions.py
│               ├── init_tool_project.py
│               ├── quality_check.py
│               └── publication_checklist.py
├── prompts/                      # Reference library
│   └── data-processing/
│       └── json-formatter.md
├── guides/                       # Usage guides
│   ├── requirement-analysis.md
│   ├── ai-collaboration.md
│   ├── solution-evaluation.md
│   └── publication-checklist.md
├── examples/                     # Complete examples
│   ├── pdf-split/
│   │   └── creation-story.md
│   └── photo-rename/
│       └── complete-story.md
├── CLAUDE.md                    # This file (system spec)
├── README.md                     # User documentation
└── pyproject.toml                # Package config
```

---

## 🚀 Quick Start

### Installation

```bash
# Install using uv (recommended)
uv tool install tool-forge

# Or use pip
pip install -e .
```

### Usage

**Start Tool-Forge system**:
```bash
tool-forge
```

This will:
1. Initialize Tool-Forge in current project
2. Launch Claude Code with Tool-Forge system prompt
3. Enable `/create` command for tool creation

**Available commands**:
```bash
tool-forge              # Launch Claude Code + Tool-Forge system
tool-forge init         # Force re-initialization
tool-forge --help       # Show help
tool-forge version      # Show version
```

---

## 🔄 Complete Workflow

```
User Request
   ↓
[Phase 1: Solution Discovery]
  Multi-strategy search
  Identify candidates
  Initial screening
   ↓
[Phase 2: Solution Evaluation]
  Multi-dimensional assessment
  Decision matrix
  Trial if promising
   ↓
[Phase 3: Decision]
  → Use existing: Integrate and document
  → Customize existing: Modify and extend
  → Build new: Enter Tool-Forge development flow
   ↓
[Phase 4: Development (if building)]
  Project initialization
  Requirement analysis
  Prompt template selection
  AI collaboration
  Quality checks
   ↓
[Phase 5: Publication]
  Publication checklist
  Release preparation
  Share with community
```

---

## 💡 Core Principles

### Principle 1: Solution Discovery First

> "Don't rush to code - systematic discovery saves time"

**Traditional**:
- Have idea → build immediately
- Might miss better solutions

**Tool-Forge**:
- Multi-strategy automated search
- Standardized evaluation process
- Evidence-based decision framework

### Principle 2: Evidence-Based Development

> "Quality comes from systematic approach, not speed"

**Traditional**:
- Unclear prompts
- AI understanding偏差
- Unstable code quality

**Tool-Forge**:
- Optimized prompt templates
- Collaboration best practices
- Quality checklists

### Principle 3: Publication Ready

> "Tools should be convenient for others to use"

**Traditional**:
- Only creator can use
- Difficult for others
- Incomplete documentation

**Tool-Forge**:
- Complete publication checklist (50+ items)
- Multi-platform compatible
- Easy for others to use

---

## 🎯 Success Criteria

Using Tool-Forge, you should be able to:

### 1️⃣ Find Best Solutions ✅
- Don't miss excellent tools
- Objective and rational evaluation
- Evidence-based decisions

### 2️⃣ Develop High-Quality Tools ✅
- Clear and effective prompts
- Stable code quality
- Efficient AI collaboration

### 3️⃣ Publish Professional Tools ✅
- Others can use conveniently
- Clear and complete documentation
- Multi-platform compatible

### 4️⃣ Continuous Improvement ✅
- Accumulate evaluation experience
- Summarize collaboration patterns
- Create your own templates

---

## 📝 Version History

**v3.0.0** - CLI Tool System (current version)
- ✅ Complete restructure as executable CLI tool
- ✅ Installable via `uv tool install`
- ✅ Three core principles
- ✅ Automated solution discovery and evaluation
- ✅ Python scripts supporting complete workflow
- ✅ Quality and publication checklists
- ✅ Reference: learn-faster-kit architecture

**v2.0.0** - Solution Evaluation System
- ✅ Solution discovery and evaluation system
- ✅ Publication checklist
- ✅ Complete examples

**v1.0.0** - Prompt Engineering Library
- ✅ Prompt template library
- ✅ Usage guides
- ✅ Real examples

---

## 🔗 Reference Resources

- [learn-faster-kit](https://github.com/hluaguo/learn-faster-kit) - System architecture reference
- [PDF-Split Tool](https://github.com/MuyaoWorkshop/pdf-split) - Complete example
- [Python CLI Development Flow](../knowledge_vault/10_Knowledge/Practices/Python_CLI项目完整开发流程.md)
