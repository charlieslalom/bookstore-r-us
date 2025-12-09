# Specification Verifier - Simple Usage

## Two Parameters Only

The tool has been simplified to just **two required parameters**:

1. `--input` - Folder containing all your source documents
2. `--specification` - The specification file to verify

## Basic Usage

```bash
./spec_verifier.py --input docs/inputs/ --specification docs/spec.md
```

That's it!

## What It Does

The tool:
1. **Scans** the input folder recursively for all documents (`.txt`, `.md`, `.markdown`, `.rst`, `.text`)
2. **Extracts** requirements and principles from ALL files found
3. **Verifies** the specification against everything it found
4. **Reports** violations, gaps, and issues

## Examples

### Example 1: Basic Verification
```bash
./spec_verifier.py \
  --input requirements/ \
  --specification spec.md
```

### Example 2: With Output File
```bash
./spec_verifier.py \
  --input docs/requirements/ \
  --specification docs/specification.md \
  --output verification_report.txt
```

### Example 3: JSON Output
```bash
./spec_verifier.py \
  --input inputs/ \
  --specification spec.md \
  --json > violations.json
```

## Folder Organization

Organize your input folder however you want:

```
inputs/
├── requirements/
│   ├── functional.md
│   └── non-functional.md
├── principles/
│   ├── security.txt
│   └── architecture.txt
├── interviews/
│   └── stakeholder_meeting_notes.md
└── design_docs/
    └── system_design.md
```

Just point to the root:
```bash
./spec_verifier.py --input inputs/ --specification spec.md
```

The tool finds everything automatically!

## Supported File Types

Automatically detects:
- `.txt`
- `.md` (Markdown)
- `.markdown`
- `.rst` (reStructuredText)
- `.text`
- Files with no extension

## What Gets Extracted

From each file, the tool extracts:

**Requirements** - Patterns like:
- `REQ-001: ...`
- `REQUIREMENT: ...`
- `The system must ...`
- `Users shall ...`
- Numbered/bulleted lists with requirements

**Principles** - Patterns like:
- `PRINCIPLE: ...`
- `RULE: ...`
- `GUIDELINE: ...`
- Must/shall statements

## Output

### Console Output
```
Scanning input folder: inputs/
Found 12 file(s)
Specification: spec.md

Loaded: 45 requirements, 23 principles, 67 specification items

================================================================================
RUNNING ADVERSARIAL VERIFICATION
================================================================================

[CHECK] Requirement Coverage Analysis...
  ✓ Uncovered requirements: 3
  ✓ Partially covered requirements: 7

[CRITICAL] COVERAGE: 3 requirements have NO coverage
  The following requirements are completely missing:
  Evidence:
    - REQ_abc123 [INPUT:user_story.md]: Password reset functionality...
    - REQ_def456 [INPUT:security.txt]: Two-factor authentication...
```

### JSON Output (with `--json`)
```json
[
  {
    "severity": "CRITICAL",
    "category": "COVERAGE",
    "title": "3 requirements have NO coverage",
    "description": "...",
    "evidence": [...],
    "line_numbers": [...]
  }
]
```

## Command-Line Options

| Option | Required | Description |
|--------|----------|-------------|
| `--input` | Yes | Input folder with all source documents |
| `--specification` | Yes | Specification file to verify |
| `--output` | No | Output file (default: stdout) |
| `--json` | No | JSON output format |

## Exit Codes

- `0` - ✅ Passed (no critical violations)
- `1` - ❌ Failed (critical violations found)

Use in CI/CD:
```bash
./spec_verifier.py --input inputs/ --specification spec.md || exit 1
```

## Quick Start

### 1. Organize Your Files
```bash
mkdir -p inputs
# Copy all your requirements, principles, etc. into inputs/
```

### 2. Run Verification
```bash
./spec_verifier.py --input inputs/ --specification your_spec.md
```

### 3. Review Report
Read the output and fix any CRITICAL or HIGH severity issues.

### 4. Re-run Until Clean
```bash
# Fix issues in your specification
# Re-run verification
./spec_verifier.py --input inputs/ --specification your_spec.md
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Verify Specification
  run: |
    ./spec_verifier.py \
      --input requirements/ \
      --specification docs/spec.md \
      --json > violations.json
```

### Makefile
```makefile
verify:
	./spec_verifier.py \
		--input requirements/ \
		--specification specification.md \
		--output report_$(shell date +%Y%m%d).txt
```

### Pre-commit Hook
```bash
#!/bin/bash
./spec_verifier.py --input requirements/ --specification spec.md || exit 1
```

## Troubleshooting

### "No supported files found"
- Check that your input folder contains `.txt`, `.md`, or other supported files
- Files must not be hidden (starting with `.`)
- Try: `ls -la inputs/` to see what's there

### "Specification file not found"
- Check the path to your specification file
- Specification must be a file, not a folder

### "Too many/few requirements found"
- Check that your files use clear requirement patterns
- Requirements should start with "REQ", "MUST", "SHALL", or be in numbered lists

## Tips

1. **Clear Markers**: Use explicit markers like `REQ-001:` for requirements
2. **Organize Logically**: Group related documents in subfolders
3. **Be Explicit**: Use "MUST", "SHALL" for mandatory requirements
4. **Separate Concerns**: Keep principles separate from requirements
5. **Version Control**: Keep your input folder in git

## What's Different from Before?

**Old way** (complicated):
```bash
./spec_verifier.py \
  --human-input input1.txt input2.txt input3.txt \
  --requirements req1.txt req2.txt \
  --constitution prin1.txt prin2.txt \
  --specification spec.md
```

**New way** (simple):
```bash
./spec_verifier.py \
  --input inputs/ \
  --specification spec.md
```

All files go in one folder. The tool figures out what's what.

## Summary

| Feature | Status |
|---------|--------|
| Single input folder | ✅ |
| Recursive scanning | ✅ |
| Auto-detects requirements | ✅ |
| Auto-detects principles | ✅ |
| Simple interface | ✅ |
| No backward compatibility baggage | ✅ |

---

**Get Started:**
```bash
./spec_verifier.py --input your_inputs/ --specification your_spec.md
```

