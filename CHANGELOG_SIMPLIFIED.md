# Changelog: Simplified to Two Parameters

## What Changed

The specification verifier has been **dramatically simplified** from multiple parameters to just **two**:

### Before (Complex)
```bash
./spec_verifier.py \
  --human-input input1.txt input2.txt input3.txt \
  --requirements req1.txt req2.txt req3.txt \
  --constitution prin1.txt prin2.txt \
  --specification spec.md
```

### After (Simple)
```bash
./spec_verifier.py --input inputs/ --specification spec.md
```

## New Interface

**Two required parameters:**
1. `--input` - Folder containing ALL source documents
2. `--specification` - The specification file to verify

**Two optional parameters:**
3. `--output` - Output file (default: stdout)
4. `--json` - JSON output format

## What Was Removed

- ❌ `--human-input` / `-i` parameter
- ❌ `--requirements` / `-r` parameter
- ❌ `--constitution` / `-c` parameter
- ❌ All backward compatibility code
- ❌ Category separation

## What Was Added

- ✅ `--input` parameter (single folder)
- ✅ Automatic recursive folder scanning
- ✅ Auto-detection of requirements from all files
- ✅ Auto-detection of principles from all files
- ✅ Simplified load_documents() method

## How It Works Now

1. **You provide**: One folder with all your documents
2. **Tool scans**: Finds all `.txt`, `.md`, `.markdown`, `.rst`, `.text` files
3. **Tool extracts**: Requirements and principles from ALL files
4. **Tool verifies**: Your specification against everything found

## Benefits

### 1. Much Simpler
```bash
# Old: 4 parameters, listing every file
./spec_verifier.py -i f1.txt f2.txt -r r1.txt r2.txt -c p1.txt -s spec.md

# New: 2 parameters
./spec_verifier.py --input inputs/ --specification spec.md
```

### 2. No Category Decisions
You don't need to decide "Is this a human input or a requirement or a principle?"

Just put it in the input folder. The tool figures it out.

### 3. Easy to Add Files
```bash
# Old: Edit command line to add new file
./spec_verifier.py -i f1.txt f2.txt NEW_FILE.txt ...

# New: Just add to folder
cp new_requirement.md inputs/
./spec_verifier.py --input inputs/ --specification spec.md  # Same command!
```

### 4. Team-Friendly
Team members can add documents to the shared folder without coordination.

### 5. Clean Commands
No more long lists of files. Just point to a folder.

## Migration

### Step 1: Create Input Folder
```bash
mkdir inputs
```

### Step 2: Move All Files
```bash
# Move everything to inputs/
mv human_inputs/* inputs/
mv requirements/* inputs/
mv principles/* inputs/
```

### Step 3: Update Command
```bash
# Old command
./spec_verifier.py \
  -i human_inputs/*.txt \
  -r requirements/*.txt \
  -c principles/*.txt \
  -s spec.md

# New command
./spec_verifier.py --input inputs/ --specification spec.md
```

## Example Folder Structure

```
project/
├── inputs/                          ← Put everything here
│   ├── user_stories.md
│   ├── technical_requirements.txt
│   ├── security_principles.md
│   ├── architecture_guidelines.txt
│   ├── performance_targets.md
│   └── stakeholder_interviews.txt
├── spec.md                          ← Your specification
└── spec_verifier.py
```

**Usage:**
```bash
./spec_verifier.py --input inputs/ --specification spec.md
```

## What Didn't Change

✅ All verification checks still work
✅ Report format unchanged
✅ Exit codes unchanged (0=pass, 1=fail)
✅ JSON output still available
✅ All violation detection logic unchanged

Only the **interface** changed. The **verification** is the same.

## Updated Files

### Modified
- **`spec_verifier.py`** - Simplified to 2 parameters

### New Documentation
- **`SIMPLE_USAGE.md`** - Simple usage guide
- **`README_VERIFIER.md`** - Quick reference
- **`CHANGELOG_SIMPLIFIED.md`** - This file

### Removed
- All backward compatibility code
- Complex parameter handling
- Category separation logic

## Examples

### Example 1: Basic
```bash
./spec_verifier.py --input requirements/ --specification spec.md
```

### Example 2: With Output
```bash
./spec_verifier.py \
  --input docs/inputs/ \
  --specification docs/spec.md \
  --output report.txt
```

### Example 3: JSON for CI/CD
```bash
./spec_verifier.py \
  --input requirements/ \
  --specification spec.md \
  --json > violations.json
```

### Example 4: CI/CD Pipeline
```yaml
- name: Verify Specification
  run: |
    ./spec_verifier.py \
      --input requirements/ \
      --specification spec.md \
      --json
```

## Breaking Changes

⚠️ **This is a breaking change!**

Old commands will not work:
```bash
# This no longer works:
./spec_verifier.py -i input.txt -r req.txt -c const.txt -s spec.md
```

Must use new format:
```bash
# Must do this:
./spec_verifier.py --input inputs/ --specification spec.md
```

## Rationale

**Why simplify?**

1. **Easier to use**: Two parameters vs many
2. **Less cognitive load**: Don't categorize documents
3. **More flexible**: Tool figures out what's what
4. **Scalable**: Add files without changing commands
5. **Cleaner**: No parameter soup
6. **Maintainable**: Less code, fewer bugs

**Why remove backward compatibility?**

1. **Simpler code**: No legacy baggage
2. **Clearer documentation**: One way to do things
3. **Better UX**: New users aren't confused by old options
4. **Easier maintenance**: Less code to maintain

The simplification makes the tool **10x easier to use** at the cost of breaking existing scripts (which are easy to update).

## Help Output

```
$ ./spec_verifier.py --help

usage: spec_verifier.py [-h] --input INPUT --specification SPECIFICATION
                        [--output OUTPUT] [--json]

Adversarial Specification Verification Tool

options:
  --input INPUT         Input folder containing all source documents
  --specification SPECIFICATION
                        Specification document to verify (file)
  --output OUTPUT       Output report file (default: stdout)
  --json                Output violations in JSON format
```

Clean and simple!

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| Required parameters | 4 | 2 |
| File organization | Manual categorization | Single folder |
| Adding files | Edit command | Drop in folder |
| Complexity | High | Low |
| Backward compatible | N/A | No |
| Ease of use | Medium | High |

**Bottom line:** The tool does the same thorough verification, but with a **much simpler interface**.

---

**Get started:**
```bash
./spec_verifier.py --input inputs/ --specification spec.md
```

