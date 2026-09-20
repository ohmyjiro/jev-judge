---
name: jev-judge
description: Delegate repeated bounded yes-no, option-choice, or rubric judgments to Jev before Codex reads all candidate evidence, including when an MCP server is unavailable.
---

# Jev Judge

Use `jev-judge request.json` or pipe a JSON request to `jev-judge`. The request has `state` plus 1–16 named `questions`; each question uses TypeSafe `noul`, `choice`, or `score`. Prepare the state in code or a local file so large source material does not first enter Codex context. The command prints only typed answers, usage, and elapsed time. Batch related questions about one state; for many independent records, call once per record from code and return only selected or uncertain results.

Choose explicit criteria and include an `other` or escalation option when candidates might all be wrong. Never send credentials or sensitive records without authorization for sending them to TypeSafe. Treat probabilities as routing evidence, not proof. Codex writes text or code and verifies consequential outcomes.
