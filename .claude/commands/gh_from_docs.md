Create GitHub issues from the task list in `docs/bookstore-r-us-TASKS.md`.

Follow the instructions in `.claude/agents/gh-from-docs.md` to:

1. **Read the tasks file** at `docs/bookstore-r-us-TASKS.md`
2. **Fetch existing issues** to avoid creating duplicates
3. **Parse all tasks** that match the format `- [ ] TNNN` where NNN is a number
4. **Identify the Phase** for each task (e.g., "Phase 1", "Phase 2", etc.)
5. **Skip tasks** where an issue with the same title already exists
6. **Create GitHub issues** for new tasks only with:
   - **Title**: The task description text (everything after `- [ ] TNNN`)
   - **Labels**:
     - `Phase XX` (where XX is the phase number)
     - `issue_ingestion`

Create labels if they don't exist. Report progress, skipped duplicates, and the total number of issues created.
