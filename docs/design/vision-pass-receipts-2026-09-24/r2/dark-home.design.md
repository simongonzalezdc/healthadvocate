judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-home.png)

NO-IMAGE — the attached screenshot does not exist on disk, so I cannot audit it and I refuse to substitute a different file.

Evidence: `/tmp/ha-ds-shots/judge-img/r2` is a **file** (a 62-byte-header JPEG, 620×436, 13,499 bytes), not a directory, so the path `/tmp/ha-ds-shots/judge-img/r2/dark-home.jpg` fails with `ENOTDIR` — there is no `dark-home.jpg` anywhere under `judge-img/`. Siblings that do exist are `r2-form.jpg`, `r2-head.jpg`, `r2-title.jpg`, `r2-top.jpg`, `r2-view.jpg` (byte-identical to the stray `r2` file) and several `z-*.png` crops; none is named or verifiably the dark-theme home screen.

I will not guess which of those crops matches "dark-home" — auditing the wrong pixels would be a dishonest verdict. Re-attach the correct image (or fix the export path in the shoot script) and I'll run the full audit.
