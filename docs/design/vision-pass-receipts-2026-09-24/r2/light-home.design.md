judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-home.png)

NO-IMAGE — refusing to audit.

The attached path `/tmp/ha-ds-shots/judge-img/r2/light-home.jpg` does not exist: `judge-img/r2` is a stray 13 KB file, not a directory. What I found while verifying:

- `judge-img/r2`, `judge-img/r2-view.jpg`, and `judge-img/r2-attached-dark-insurance.jpg` are byte-identical copies of one 599×880 **crop** — no full r2 light-home render exists.
- The only full-page light-home shots on disk are `judge-img/r1/light-home.jpg` (620×910) and older top-level `j-`/`t-` copies, all checksum-distinct — i.e., a **different round** of the build.

The brief says judge ONLY the attached image, and an r1 verdict stamped as r2 would be a dishonest audit. Fix the attachment path (or point me at the real r2 full-page capture) and I'll run the full describe-and-defect pass.
