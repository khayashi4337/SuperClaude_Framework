---
name: translate-file
description: "Translates a single specified file using the Japanese translation agent."
category: workflow
complexity: standard
personas: [translation-agent-jp]
---

# /sc:translate-file - Translate Single File

> **Context Framework Note**: This command activates the Japanese translation agent to process a single file.

## Context Trigger Pattern
```
/sc:translate-file [file_path]
```
**Usage**: Provide the full path to the file you want to translate.

## Behavioral Flow
1.  **Validate**: Check if the file at `[file_path]` exists and is a supported format (.md, .json).
2.  **Activate Persona**: Invoke the `translation-agent-jp` persona.
3.  **Execute**: Instruct the agent to translate the specified file.
4.  **Report**: Announce that the translation is complete or report any errors encountered.

## Examples

### Translate a README file
```
/sc:translate-file Docs/Reference/README.md
```