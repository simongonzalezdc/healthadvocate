judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/mobile-library.png)

NO-IMAGE

I cannot see the attached image, so per your instruction I'm refusing the audit rather than substituting a guess.

**What's wrong:** the attachment path `/tmp/ha-ds-shots/judge-img/r2/mobile-library.jpg` does not exist. Under `judge-img/`, `r2` is a single JPEG file (620×436), not a directory, so the path fails with ENOTDIR. There is no `mobile-library.jpg` anywhere under an `r2` path.

**Likely intended file:** `mobile-library.jpg` exists only under the **r1** directory (`/tmp/ha-ds-shots/judge-img/r1/mobile-library.jpg`). The `judge-img/r2/` area contains differently named shots (`r2-form.jpg`, `r2-head.jpg`, `r2-title.jpg`, `r2-top.jpg`, `r2-view*.jpg`) — none named for the library screen. Since this audit's whole point is honesty about what is actually being judged, I won't audit the r1 file (a different round's capture) or any other shot and present it as the attached one.

Re-attach with the corrected path — either `/tmp/ha-ds-shots/judge-img/r1/mobile-library.jpg` or the specific r2 file you meant — and I'll run the six-question audit verbatim.
