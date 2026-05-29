---
description: "Add new context or facts to the repo's copilot-instructions.md. Use when: discovered something about the codebase worth recording, want to document a convention, add architectural context, or capture tribal knowledge for future developers."
agent: "agent"
tools: ["search", "editFiles"]
argument-hint: "Describe the context to add..."
---

The user wants to add new context or facts to the repository's Copilot instructions file at `.github/copilot-instructions.md`.

## Your task

1. Read the user's input — they will describe a fact, convention, architectural detail, or piece of tribal knowledge they want recorded.
2. Read the current `.github/copilot-instructions.md` to understand the existing structure and sections.
3. Determine where the new information best fits:
   - If it extends an existing section, add it there
   - If it's a new topic, create a new section in a logical position
   - If it corrects existing information, update in place
4. Make the edit — keep the same tone and formatting as the rest of the file (concise, factual, bullet points or tables where appropriate).
5. Confirm what was added and where.

## Rules

- Do NOT duplicate information already present in the file.
- Do NOT restructure or reformat existing sections — only touch what's needed.
- Keep additions concise. This file is loaded into Copilot's context on every interaction, so brevity matters.
- If the user's input is vague, search the codebase to verify facts before adding them.
- If the information seems incorrect or contradicts the codebase, flag it to the user before adding.
