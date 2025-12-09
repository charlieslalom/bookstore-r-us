# Specification Verifier

**Adversarial verification tool for specification documents**

## ⚡ Ultra-Simple Usage

```bash
./spec_verifier.py --input inputs/ --specification spec.md
```

Two parameters:
1. `--input` - Folder with all your requirements, principles, design docs
2. `--specification` - The spec file to verify

## 🚀 Quick Start

```bash
# 1. Organize your source documents
mkdir inputs
cp requirements.txt principles.txt design_notes.md inputs/

# 2. Run verification
./spec_verifier.py --input inputs/ --specification my_spec.md

# 3. Fix violations and re-run
```

## 📋 What It Checks

- ❌ **Missing Requirements** - Requirements not covered in spec
- ❌ **Principle Violations** - Spec violates mandatory principles
- ❌ **Contradictions** - Conflicting specifications
- ⚠️ **Scope Creep** - Specs not traced to requirements
- ⚠️ **Ambiguity** - Vague language ("reasonable", "TBD")
- ⚠️ **Testability** - No measurable criteria
- ℹ️ **Consistency** - Inconsistent terminology

## 🎯 Example

**Input folder:**
```
inputs/
├── user_stories.md
├── security_requirements.txt
├── architecture_principles.md
└── performance_targets.txt
```

**Run:**
```bash
./spec_verifier.py --input inputs/ --specification system_spec.md
```

**Output:**
```
Scanning input folder: inputs/
Found 4 file(s)
Specification: system_spec.md

Loaded: 23 requirements, 15 principles, 45 specification items

[CRITICAL] COVERAGE: 3 requirements have NO coverage
  - Password reset functionality not addressed
  - Two-factor authentication missing
  - Session timeout not specified

[HIGH] PRINCIPLE_VIOLATION: Spec logs passwords
  Line 67: Violates "Never log sensitive data" principle

❌ FAILED - 2 CRITICAL issues must be resolved
```

## 📄 Supported File Types

- `.txt`
- `.md` (Markdown)
- `.markdown`
- `.rst`
- `.text`
- Files with no extension

## 🔍 What Gets Extracted

**Requirements:**
- `REQ-001: System must...`
- `The system shall...`
- `- Users need to...`
- Numbered lists

**Principles:**
- `PRINCIPLE: Never...`
- `RULE: All data must...`
- `Must/shall` statements

## 📊 Options

| Option | Description |
|--------|-------------|
| `--input FOLDER` | Input folder (required) |
| `--specification FILE` | Spec file (required) |
| `--output FILE` | Save report to file |
| `--json` | JSON output format |

## 💡 Examples

### Save to File
```bash
./spec_verifier.py \
  --input requirements/ \
  --specification spec.md \
  --output report.txt
```

### JSON for CI/CD
```bash
./spec_verifier.py \
  --input requirements/ \
  --specification spec.md \
  --json > violations.json
```

### In CI/CD Pipeline
```bash
./spec_verifier.py --input reqs/ --specification spec.md || exit 1
```

## 🎓 Full Documentation

- **Quick Start**: [`SIMPLE_USAGE.md`](SIMPLE_USAGE.md)
- **Detailed Guide**: [`SPEC_VERIFIER_README.md`](SPEC_VERIFIER_README.md)
- **Examples**: [`examples/README.md`](examples/README.md)

## 🧪 Try the Demo

```bash
cd examples
./run_demo.sh
```

## ✅ Features

- ✅ **Simple**: Just two parameters
- ✅ **Automatic**: Scans folders recursively
- ✅ **Smart**: Extracts requirements and principles automatically
- ✅ **Adversarial**: Skeptical and thorough
- ✅ **Fast**: Runs in seconds
- ✅ **CI/CD Ready**: Exit codes, JSON output
- ✅ **Zero Dependencies**: Pure Python 3

## 🎯 Use Cases

1. **Pre-implementation**: Verify specs before coding
2. **Stakeholder review**: Check completeness before approval
3. **Requirements change**: Re-verify after updates
4. **CI/CD gate**: Automatic verification on commits
5. **Quality assurance**: Regular specification audits

## 📝 Help

```bash
./spec_verifier.py --help
```

---

**Get Started:** `./spec_verifier.py --input inputs/ --specification spec.md`

