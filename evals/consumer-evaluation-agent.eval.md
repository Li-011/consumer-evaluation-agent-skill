# Consumer Agent 1.1 Eval

## Interface checks

1. Input contains only `poster_image` and `product_input` at the top level.
2. `scene_tags` contains exactly one P, one M, and one S label in that order.
3. Unknown or misordered frozen tags are rejected.
4. Output contains exactly the seven A-D fields.
5. `meta` contains only `judge_dimensions` and `confidence`.

## Scoring checks

1. Five fixed dimensions accept only integer anchors 0, 1, or 2.
2. Overall score is their sum and remains an integer from 0 to 10.
3. Score 7 or above passes only when no critical issue exists.
4. A critical factual issue blocks pass even when the score is high.
5. Problems and suggestions are paired by index and limited to three.

## Failure checks

1. Image parse failure returns the same seven-field JSON with score 0.
2. Missing required input never produces fabricated dimension scores.
3. Invalid, incorrect, or uncertain content is never included in `protected_content`.
