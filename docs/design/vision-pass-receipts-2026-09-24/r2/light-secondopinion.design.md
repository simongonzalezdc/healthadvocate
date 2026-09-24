judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-secondopinion.png)

NO-IMAGE — refusing per instruction.

The attachment path `/tmp/ha-ds-shots/judge-img/r2/light-secondopinion.jpg` does not exist. What's actually on disk at that location: `judge-img/r2` is a **JPEG file** (620×436), not a directory, so the `r2/…` path fails with ENOTDIR. That file is byte-identical to `r2-attached-dark-insurance.jpg` — i.e., it is a *dark insurance* shot, not the light second-opinion screen I was asked to judge. The only `light-secondopinion.jpg` on disk is under `judge-img/r1/` (a different round).

Since the named image cannot be seen and the only candidate at the attachment path is provably a different screen, I will not substitute or guess. To fix the pipeline: either the attachment should point at `/tmp/ha-ds-shots/judge-img/r1/light-secondopinion.jpg`, or the r2 capture of the second-opinion view was never rendered/renamed correctly (it collides with the dark-insurance JPEG).
