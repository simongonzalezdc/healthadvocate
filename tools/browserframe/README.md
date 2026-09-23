# Browser-frame verification harness

`playground_matrix.mjs` (playwright) verifies the champion playground page in
REAL browser engines (chromium + webkit) — the consumer frame. Run from a dir
with playwright installed (`npm i playwright; npx playwright install chromium
webkit`), playground live on :8936, tunnel agent loaded:

    node playground_matrix.mjs

Scenarios: page render + LIVE badge, real chat round-trip, tunnel-down UX
(explicit DOWN + warning), self-heal restore. Exit 0 = all green.

Origin lesson (2026-09-23): the page shipped with a top-level `return` JS
syntax error that curl smoke-tests could not see — the chat UI never worked
in ANY browser while the server API tested green. Producer-frame verification
(curl) must never gate consumer-frame surfaces (pages). This harness is the
standing cure; run it after any playground change.
