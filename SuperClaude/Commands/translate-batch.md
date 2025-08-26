---
name: translate-batch
description: "Translates all target files in the project in a batch operation."
category: workflow
complexity: advanced
personas: [translation-agent-jp]
---

# /sc:translate-batch - Batch Translate Project Files

> **Context Framework Note**: This command systematically translates all designated documentation and configuration files to Japanese.

## Context Trigger Pattern
```
/sc:translate-batch [--dry-run]
```
**Usage**: Run without arguments to translate all target files. Use `--dry-run` to list the files that would be translated without actually performing the translation.

## Behavioral Flow
1.  **Discover Files**: Use `find_by_name` to identify all files matching the target patterns.
    -   **Targets**: `README.md`, `Docs/**/*.md`, `SuperClaude/Commands/**/*.md`
    -   **Exclusions**: `scripts/`, `bin/`, `.github/`, `*.py`, `*.js`
2.  **Handle Dry Run**: If `--dry-run` is specified, list the discovered files and stop.
3.  **Activate Persona**: Invoke the `translation-agent-jp` persona.
4.  **Execute in Parallel**: Instruct the agent to translate all discovered files. This process should be parallelized for efficiency.
5.  **Summarize**: Report the total number of files translated, any errors, and the location of the translation log.

## Examples

### Perform a dry run to see what will be translated
```
/sc:translate-batch --dry-run
```

### Execute the full batch translation
```
/sc:translate-batch
```