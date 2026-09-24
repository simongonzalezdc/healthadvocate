judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-drugs.png)

NO-IMAGE — refusing to judge.

The attached path does not resolve: `/tmp/ha-ds-shots/judge-img/r2/light-drugs.jpg` fails because `judge-img/r2` is a **file** (a 620×436 JPEG, 13,499 bytes), not a directory, so no `light-drugs.jpg` exists under it. I have therefore seen nothing to audit.

For whoever is feeding the judge, the likely intended artifacts are:
- `/tmp/ha-ds-shots/judge-img/r1/light-drugs.jpg` — the previous round's version of this view
- `/tmp/ha-ds-shots/judge-img/r2-view.jpg` (byte-identical to the stray `judge-img/r2` file and to `r2-attached-dark-insurance.jpg`) — but its name suggests a dark insurance view, not light drugs

I deliberately did not substitute either one, since auditing the wrong screenshot would produce a dishonest verdict. Re-attach the correct r2 light-drugs capture and I'll run the full describe-then-defects pass.
