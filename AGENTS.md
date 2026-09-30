# 02消费者Agent-skill

Use this repository to evaluate one e-commerce poster from upstream-locked P population, M purchase-motivation, and S usage-scene tags.

## Contract

- Accept only the fixed A-to-D input: `poster_image` plus `product_input`.
- Treat `scene_tags` as exactly `[P population, M motivation, S usage scene]`.
- Return exactly the seven D-to-A fields defined in `assets/schemas/output.schema.json`.
- Return JSON only. Errors keep the same structure with score 0.

## Evaluation

- Observe the poster before using product facts to fill gaps.
- Score the five fixed dimensions from 0 to 2 and sum them to 0–10.
- Pass only at score 7 or above with no critical factual issue.
- Pair each problem with the suggestion at the same array index; keep at most three.
- Protect only content verified as correct against the supplied product input.

## Boundaries

- Never reclassify P-M-S tags.
- Never invent product claims or campaign requirements.
- Do not generate posters, control retries, compare versions, call the aesthetic agent, or grade pure aesthetics.
- A owns compliance, iteration, logging, regeneration, and protected-content merging.
