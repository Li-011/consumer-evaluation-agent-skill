# Consumer Evaluation Agent Skill

Use this repository when evaluating an e-commerce poster from a locked target-consumer perspective.

## Activation

Activate for consumer scoring, poster iteration comparison, PASS versus ITERATE decisions, consumer-facing failure diagnosis, or structured revision routing.

## Required behavior

- Read `SKILL.md` for the full protocol.
- Preserve the upstream macro segment and purchase motivation.
- Score Attention, Relevance, Clarity, Value, and Desire with equal weights.
- Choose a 1–5 rubric anchor before converting to 20/40/60/80/100.
- Use only registered failure codes.
- Return schema-valid JSON.
- Route pure aesthetics to the Aesthetic Agent.
- Never invent product evidence.

## Gotchas

- The 48 consumer states are contexts, not separate rubrics.
- Purchase motivation changes the lens, not the weights.
- PASS requires CES at least 80 and no dimension below 65.
- Keep taxonomy, rubric, thresholds, and product truth fixed across iterations.

