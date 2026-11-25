# Standalone M8 saved-report audit

This helper explains existing in-sample D1/D2 retrieval reports. It does not call a model, change Gold, tune mappings, load contracts or evaluate held-out data.

`m8_audit.audit(report)` validates the saved protocol, source-family identities, case identities, rank bounds and agreement with saved Primary/Oracle metrics. It returns the union of graph-off and graph-on misses with diagnostic flags. Query/citation group counts are descriptive; they are not additional independent source families.

Run the self-contained tests from the directory containing these two Python files, using the project Python environment:

```powershell
& '<project-python.exe>' -m pytest -q test_m8_audit.py
```

All test cases are synthetic fixtures for the audit tool. They are not inference results or legal annotations.
The actual historical source reports remain in the internal evidence packet. Read `N2_M8_ERROR_ANALYSIS.md` for their hashes, reconciled counts, conclusions and limits.

In particular, the historical `primary_missed_cases` list covers graph-off misses only. Looking only at that list loses graph-on-only regressions. Top5 evaluation remains top5 even when the retrieval pool has8 items. Oracle replacement labels may worsen individual rankings and are not an inference configuration.

The helper intentionally rejects protocols/splits it does not support. It is an analysis sidecar, not a replacement for the runtime retriever or the M8 metric implementation.
