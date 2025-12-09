# GitHub Issues from Docs Agent

Create GitHub issues for all tasks defined in the `docs/bookstore-r-us-TASKS.md` file. **Skip any tasks where an issue with the same title already exists.**

## Instructions

### 1. Fetch Existing Issues

Before creating any issues, fetch all existing issue titles to avoid duplicates:

```bash
# Get all existing issue titles (open and closed)
gh issue list --state all --limit 1000 --json title --jq '.[].title'
```

Store these titles in a set/list for quick lookup.

### 2. Read the Tasks File

Read the file at `docs/bookstore-r-us-TASKS.md` to extract all tasks.

### 3. Task Format

Tasks follow this format:
```
- [ ] TNNN [optional flags] Description with file paths
```

Where:
- `TNNN` is the task ID (e.g., T001, T025, T230)
- `[P]` indicates the task can run in parallel (optional)
- `[US#]` indicates which user story the task belongs to (optional)
- The description follows after the flags

### 4. Phase Detection

Tasks are organized under Phase headers like:
```
## Phase 1: Setup (Shared Infrastructure)
## Phase 2: Foundational (Blocking Prerequisites)
## Phase 3: User Story 1 - Product Catalog Display (Priority: P1)
```

Extract the phase number from each section header and apply it to all tasks under that section.

### 5. Create Labels

Before creating issues, ensure required labels exist:

```bash
# Create issue_ingestion label if it doesn't exist
gh label create "issue_ingestion" --description "Issues ingested for processing" --color "2ea44f" 2>/dev/null || true

# Create Phase labels (Phase 01 through Phase 20)
for i in $(seq -w 1 20); do
  gh label create "Phase $i" --description "Phase $i tasks" --color "c5def5" 2>/dev/null || true
done
```

### 6. Create Issues (Skip Duplicates)

For each task found:

1. Extract the task ID (TNNN)
2. Extract the description (everything after the task ID and optional flags)
3. Build the issue title: `TNNN: Description`
4. **Check if title already exists** in the existing issues list
   - If it exists: **SKIP** this task and log it as skipped
   - If it doesn't exist: proceed to create the issue
5. Determine the current Phase from the section header
6. Create the GitHub issue:

```bash
gh issue create \
  --title "TNNN: Description" \
  --body "Task from docs/bookstore-r-us-TASKS.md

**Task ID**: TNNN
**Phase**: Phase XX
**Parallel**: Yes/No
**User Story**: USXX (if applicable)

## Description
Full task description here

## File Path
Extracted file path if mentioned in task
" \
  --label "Phase XX" \
  --label "issue_ingestion"
```

### 7. Parsing and Duplicate Check Logic

```python
# Pseudocode for parsing with duplicate detection

# Step 1: Get existing issue titles
existing_titles = set(get_all_issue_titles())  # From gh issue list

current_phase = None
tasks = []
skipped = []

for line in file:
    # Check for phase header
    if line.startswith("## Phase"):
        # Extract phase number (e.g., "Phase 1" from "## Phase 1: Setup...")
        match = re.search(r'Phase (\d+)', line)
        if match:
            current_phase = int(match.group(1))

    # Check for task
    if line.strip().startswith("- [ ] T"):
        # Extract task ID and description
        match = re.match(r'- \[ \] (T\d+)\s*(.+)', line.strip())
        if match:
            task_id = match.group(1)
            rest = match.group(2)

            # Check for [P] flag
            is_parallel = "[P]" in rest
            rest = rest.replace("[P]", "").strip()

            # Check for [US#] flag
            us_match = re.search(r'\[US(\d+)\]', rest)
            user_story = us_match.group(1) if us_match else None
            rest = re.sub(r'\[US\d+\]', '', rest).strip()

            # Remaining text is the description
            description = rest

            # Build the issue title
            issue_title = f"{task_id}: {description}"

            # CHECK FOR DUPLICATE
            if issue_title in existing_titles:
                skipped.append({
                    'id': task_id,
                    'title': issue_title,
                    'reason': 'Already exists'
                })
                continue  # Skip this task

            tasks.append({
                'id': task_id,
                'description': description,
                'title': issue_title,
                'phase': current_phase,
                'parallel': is_parallel,
                'user_story': user_story
            })
```

### 8. Progress Reporting

Report progress as issues are created:
- Show current task being created
- Show running total (e.g., "Created 45/230 issues")
- Show skipped duplicates (e.g., "Skipped 5 existing issues")
- Report any errors

### 9. Final Summary

After completion, report:
- Total tasks found in file
- Total issues created (new)
- Total issues skipped (already exist)
- Issues by phase
- Any tasks that failed to create

## Example Output

```
Creating GitHub issues from docs/bookstore-r-us-TASKS.md...

Fetching existing issues to check for duplicates...
- Found 28 existing issues

Creating labels...
- Created label: issue_ingestion
- Created labels: Phase 01 through Phase 20

Processing 230 tasks...
[1/230] SKIPPED: T001 - Create Next.js 14 project structure... (already exists)
[2/230] SKIPPED: T002 - Configure Tailwind CSS... (already exists)
[3/230] Created: T003 - Setup Python FastAPI project structure... (Phase 01)
[4/230] Created: T004 - Configure Docker Compose... (Phase 01)
...
[230/230] Created: T230 - Create runbook for production operations (Phase 20)

Summary:
- Total tasks in file: 230
- Issues created: 202
- Issues skipped (already exist): 28
- By phase:
  - Phase 01: 5 created, 2 skipped
  - Phase 02: 11 created, 0 skipped
  - Phase 03: 20 created, 2 skipped
  ...
```

## Notes

- **Duplicate Detection**: Issues are checked by exact title match. If an issue with the title `TNNN: Description` already exists (open or closed), skip creating it.
- The agent should handle rate limiting from GitHub API
- Batch operations where possible to reduce API calls
- Include the original task ID in the issue title for traceability (enables duplicate detection)
