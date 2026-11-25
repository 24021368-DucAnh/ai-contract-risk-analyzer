# Pipeline source-only review handoff — do not merge into Data code

This branch carries a review artifact for sosadsonar/ai-contract-risk-analyzer-pipeline. It is stored here because the connected GitHub integration returned HTTP 403 (Resource not accessible by integration) for the Pipeline Git tree write. It is not an implementation change to this Data repository. Review it here; apply it in the Pipeline repository on a new branch and open its actual integration PR there.

## Application

Required Pipeline base: d930e0092fa27f92cabf2ef8161d9fab86c60272. Verify the patch SHA256 against MANIFEST.json, create an isolated branch at that base, run `git apply --check pipeline_code_only.patch`, then apply the patch. Do not apply this patch at the Data repository root. Do not merge this review-only PR as a substitute for a Pipeline PR.

The patch contains exactly 24 allowlisted Pipeline source/test/plan files. No source contracts, Gold datasets, corpus law text, private metadata, runtime DB, credentials, submodule gitlink or runtime-default changes are included. The reviewer guide is provided alongside the patch.

## Validation scope

Fresh checks: current remote main equals the patch base; the full public base tree was verified against GitHub blob hashes; all 24 patched file hashes match the previously verified code-only patch manifest; full Pipeline Ruff passes. Comparison with the historical frozen Pipeline portion found 53 exact files and 497 files differing only in LF/CRLF, with zero other content differences across its 516 source and 34 resource pins.

Fresh full pytest collected 1216 tests (4 optional live tests deselected, 1212 selected) but did not complete: the first contract test blocked in Windows socketpair accept while asyncio.run created its self-pipe. A faulthandler trace located this boundary. The run was interrupted; it is neither a test failure count nor a successful regression. The same test collection without execution completed. No actual model/cloud call was made. The maintainer must run full offline regression in a host where socketpair works, and attach the result before merging the actual Pipeline PR.

Historical frozen-candidate regression was 1214 passed, 2 skipped, 4 optional live tests deselected. That larger source/fixture environment is not identical to the current public-only checkout and is not a new result for this branch. Do not replace the incomplete fresh run with that result.

Data converter validation is tracked separately in Data PR #25: 22 fresh tests passed. Neither PR completes WP2 legal/source-rights review, Risk taxonomy migration compatibility, teammate handover, frozen Dev predictions or final system acceptance. M10 stays NOT_MEASURED; T1/T2 stay closed.

Review ownership: sosadsonar is the Pipeline repository owner and has write permission in this Data repository. Review request is separate from actual approval. No merge has been performed.
