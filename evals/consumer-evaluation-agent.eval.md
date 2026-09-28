# Consumer Evaluation Agent 1.0 Eval

## Binary checks

1. Valid taxonomy labels are accepted and unknown labels are rejected.
2. A 1–5 anchor is deterministically converted to 20–100.
3. CES is the equal-weight mean of A–E.
4. PASS requires CES at least 80 and no dimension below 65.
5. Unknown Failure Codes are rejected.
6. Version comparison fails when the locked consumer profile changes.

## Golden cases

- `nori-input-valid`: the bundled NORI input validates.
- `nori-v1-iterate`: scores 80/80/60/60/60 produce CES 68 and ITERATE.
- `nori-v2-pass`: scores 80/80/80/80/80 produce CES 80 and PASS.
- `profile-drift-holdout`: changing the profile between versions must fail. Split: test.

