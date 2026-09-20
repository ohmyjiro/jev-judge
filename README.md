# jev-judge

A small, dependency-free CLI for delegating bounded judgments to [TypeSafe Jev](https://docs.typesafe.ai/api). Give it a JSON `state` and named Noul, Choice, or Score questions. It returns typed answers, usage, and elapsed time without echoing the state.

The useful pattern for coding agents is to construct the request from a local file or tool output **before that material enters the agent's context**. The agent then reads the small answer instead of the full evidence. This can reduce context sent to the agent; it does not make the TypeSafe API call free or prove that a workflow is faster.

## Install

Requires Python 3 and a TypeSafe API key. No Python packages are required.

```sh
git clone https://github.com/ohmyjiro/jev-judge.git
cd jev-judge
install -m 755 bin/jev-judge "$HOME/.local/bin/jev-judge"
```

Provide `TYPESAFE_API_KEY` through your existing secret manager or environment. Do not put the key in a request file or commit it. The CLI sends the supplied state and questions to TypeSafe's API; do not submit confidential material unless that transfer is appropriate for your task.

## Use

```sh
jev-judge examples/triage.json
cat examples/triage.json | jev-judge
```

The [example request](examples/triage.json) asks three questions about one saved link: a yes/no judgment, a topic choice with an `other` option, and an actionability score. Output contains `answers`, `model`, `usage`, and `elapsedMs`; it never includes the input `state`. Pipe through `jq '.answers'` if only the decisions are needed.

For an agent workflow, generate the request from files in code, call `jev-judge request.json`, and show the agent only the answer or uncertain cases. For many independent records, call once per record from code. Put related questions about the *same* state in one request. Jev does not write summaries or code; leave open-ended writing and final verification to the agent.

The CLI accepts 1–16 named questions and enforces a 50 KB request guardrail. It reports API failures without printing the state or key. It does not choose a confidence threshold or take an action for you.

## Codex skill

Copy [`skills/jev-judge/SKILL.md`](skills/jev-judge/SKILL.md) into your Codex skills directory if you want Codex to recognize the workflow. The CLI also works without Codex or MCP.

## Check

```sh
python3 -m unittest discover -s tests -v
```

This project is an independent community tool, not affiliated with TypeSafe AI.
