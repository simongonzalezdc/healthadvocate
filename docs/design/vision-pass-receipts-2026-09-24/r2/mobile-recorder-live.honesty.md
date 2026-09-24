judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/mobile-recorder-live.png)

**NO-IMAGE.** I cannot see the attached image, so I'm refusing to issue a verdict, per your protocol.

What I found when resolving the attachment path:

- `/tmp/ha-ds-shots/judge-img/r2` is a **13,499-byte JPG file, not a directory**. So the attached path `r2/mobile-recorder-live.jpg` cannot exist — any stat or read of it fails with `ENOTDIR`. The attachment never materialized.
- There are two plausible candidates for what was meant, and they are **different images**, so guessing would risk auditing the wrong screenshot:
  1. `/tmp/ha-ds-shots/judge-img/r1/mobile-recorder-live.jpg` — exact filename match, but in the r1 (round-1) directory.
  2. `/tmp/ha-ds-shots/judge-img/r2` itself — exact directory-prefix match, but it is byte-identical (md5 `731d0d0b...`) to `r2-view.jpg`, i.e. it's the round-2 "view" screenshot, not a recorder-live shot.

I won't substitute either one and present a verdict as if it were the attached image — that would be exactly the failure mode this audit exists to catch: a fallback dressed up as a confident answer. There is no HONESTY-VERDICT line because no image was judged.

Tell me which file to audit (the `r1/mobile-recorder-live.jpg`, the `r2`/`r2-view.jpg` file, or a corrected path) and I'll run the six-question audit against it.
