---
name: translate-check
description: "Checks the status and history of file translations."
category: utility
complexity: simple
---

# /sc:translate-check - Check Translation Status

> **Context Framework Note**: This command provides a summary of translation activities by reading the log file.

## Context Trigger Pattern
```
/sc:translate-check
```
**Usage**: Run this command to get a report on translation progress.

## Behavioral Flow
1.  **Read Log**: Read the `SuperClaude/Translations/translation_log.json` file.
2.  **Analyze Data**: Process the log data to calculate key metrics:
    -   Total number of translated files.
    -   Timestamp of the most recent translation.
    -   List of files with translation errors.
3.  **Generate Report**: Present the analyzed data to the user in a clear, readable format.

## Example

### Check the current translation status
```
/sc:translate-check
```