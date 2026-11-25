# N1 review — Ngô Hoàng Nhật

Scope: Clause AI / provider / Clause Graph. See OWNERSHIP.md and the role issue. Display-only preview; apply the original decoded patch, not this Markdown.

## backend/app/ai/dev_local_client.py

````diff
diff --git a/backend/app/ai/dev_local_client.py b/backend/app/ai/dev_local_client.py
--- a/backend/app/ai/dev_local_client.py
+++ b/backend/app/ai/dev_local_client.py
@@ -28,6 +28,19 @@
         return r.status_code, r.json()
     except ValueError:
         return r.status_code, None
+
+
+
+def _reported_token_count(payload, key):
+    if not isinstance(payload, dict):
+        return None
+
+    value = payload.get(key)
+
+    if type(value) is int and value >= 0:
+        return value
+
+    return None


 class DevLocalClient:
@@ -67,9 +80,25 @@
         try:
             data = json.loads(payload["message"]["content"])
         except (KeyError, TypeError, json.JSONDecodeError):
-            raise ProviderFailure("invalid_json") from None
+            raise ProviderFailure(
+                "invalid_json",
+                in_tokens=_reported_token_count(
+                    payload, "prompt_eval_count"
+                ),
+                out_tokens=_reported_token_count(
+                    payload, "eval_count"
+                ),
+            ) from None
         if not isinstance(data, dict):
-            raise ProviderFailure("invalid_json")
+            raise ProviderFailure(
+                "invalid_json",
+                in_tokens=_reported_token_count(
+                    payload, "prompt_eval_count"
+                ),
+                out_tokens=_reported_token_count(
+                    payload, "eval_count"
+                ),
+            )
         return LLMResponse(
             data=data,
             model_id=model_id,
````

## backend/app/clause/dev_tfidf_baseline.py

````diff
diff --git a/backend/app/clause/dev_tfidf_baseline.py b/backend/app/clause/dev_tfidf_baseline.py
--- a/backend/app/clause/dev_tfidf_baseline.py
+++ b/backend/app/clause/dev_tfidf_baseline.py
@@ -37,7 +37,8 @@
     for text, labels in zip(texts, predictions):
         if not labels:
             raise ValueError("Dev clause prediction must contain a label")
-        if _SECURITY_WORKING_CONDITIONS.search(_normalize(text)):
+        # OTHER is exclusive in the frozen taxonomy; preserve it before secondary signals.
+        if "OTHER" not in labels and _SECURITY_WORKING_CONDITIONS.search(_normalize(text)):
             retained = tuple(dict.fromkeys(labels[:2]))
             result.append(retained if "WORKING_CONDITIONS" in retained
                           else (labels[0], "WORKING_CONDITIONS"))
````

## tests/unit/test_dev_local_client_oi05.py

````diff
diff --git a/tests/unit/test_dev_local_client_oi05.py b/tests/unit/test_dev_local_client_oi05.py
new file mode 100644
--- /dev/null
+++ b/tests/unit/test_dev_local_client_oi05.py
@@ -0,0 +1,188 @@
+
+"""OI-05: preserve reported usage on invalid local JSON."""
+
+import asyncio
+
+import pytest
+from app.ai.dev_local_client import DevLocalClient
+from app.ai.provider import (
+    AiOutputInvalid,
+    InMemoryLedger,
+    ProviderFailure,
+    call_with_retry,
+)
+
+
+def response(content, in_tokens=120, out_tokens=40):
+    return {
+        "message": {"content": content},
+        "prompt_eval_count": in_tokens,
+        "eval_count": out_tokens,
+    }
+
+
+CASES = [
+    (
+        "valid_json",
+        [response('{"ok": true}')],
+        0,
+        (1, 120, 40, [], "SUCCESS"),
+    ),
+    (
+        "invalid_json_known_usage",
+        [response('{"broken":')],
+        0,
+        (1, 120, 40, ["invalid_json"], "AiOutputInvalid"),
+    ),
+    (
+        "non_object_json_known_usage",
+        [response("[]")],
+        0,
+        (1, 120, 40, ["invalid_json"], "AiOutputInvalid"),
+    ),
+    (
+        "invalid_json_retry_success",
+        [
+            response('{"broken":', 120, 40),
+            response('{"ok": true}', 130, 50),
+        ],
+        1,
+        (2, 250, 90, ["invalid_json"], "SUCCESS"),
+    ),
+    (
+        "invalid_json_retry_exhausted",
+        [
+            response('{"broken":', 120, 40),
+            response('{"broken":', 130, 50),
+        ],
+        1,
+        (
+            2, 250, 90,
+            ["invalid_json", "invalid_json"],
+            "AiOutputInvalid",
+        ),
+    ),
+    (
+        "missing_usage",
+        [{"message": {"content": "broken"}}],
+        0,
+        (1, 0, 0, ["invalid_json"], "AiOutputInvalid"),
+    ),
+    (
+        "partial_usage",
+        [{
+            "message": {"content": "broken"},
+            "prompt_eval_count": 120,
+        }],
+        0,
+        (1, 120, 0, ["invalid_json"], "AiOutputInvalid"),
+    ),
+    (
+        "malformed_usage",
+        [response("broken", True, -1)],
+        0,
+        (1, 0, 0, ["invalid_json"], "AiOutputInvalid"),
+    ),
+]
+
+
+@pytest.mark.parametrize(
+    "name,payloads,retry,expected",
+    CASES,
+    ids=[case[0] for case in CASES],
+)
+def test_ledger(name, payloads, retry, expected):
+    iterator = iter(payloads)
+    transport_calls = 0
+
+    def fake_transport(url, body, timeout):
+        nonlocal transport_calls
+        transport_calls += 1
+        return 200, next(iterator)
+
+    client = DevLocalClient(
+        app_env="dev",
+        transport=fake_transport,
+    )
+
+    ledger = InMemoryLedger(max_calls=2)
+
+    async def execute():
+        outcome = "SUCCESS"
+
+        try:
+            result, _ = await call_with_retry(
+                client,
+                ledger,
+                model_id="offline-test",
+                messages=[
+                    {
+                        "role": "user",
+                        "content": "Synthetic test",
+                    }
+                ],
+                response_schema={"type": "object"},
+                timeout_s=5,
+                max_retries=retry,
+            )
+            assert result.data == {"ok": True}
+
+        except AiOutputInvalid:
+            outcome = "AiOutputInvalid"
+
+        assert transport_calls == ledger.calls
+
+        assert (
+            ledger.calls,
+            ledger.in_tokens,
+            ledger.out_tokens,
+            ledger.errors,
+            outcome,
+        ) == expected
+
+    asyncio.run(execute())
+
+
+@pytest.mark.parametrize(
+    "payload,expected",
+    [
+        (response("broken", 120, 40), (120, 40, True)),
+        (
+            {"message": {"content": "broken"}},
+            (None, None, False),
+        ),
+        (response("broken", 0, 0), (0, 0, True)),
+        (response("broken", True, -1), (None, None, False)),
+    ],
+    ids=[
+        "known_usage",
+        "unknown_usage",
+        "zero_usage",
+        "malformed_usage",
+    ],
+)
+def test_failure_metadata(payload, expected):
+    client = DevLocalClient(
+        app_env="dev",
+        transport=lambda *args: (200, payload),
+    )
+
+    with pytest.raises(ProviderFailure) as captured:
+        asyncio.run(
+            client.generate_structured(
+                model_id="offline-test",
+                messages=[],
+                response_schema={"type": "object"},
+                timeout_s=5,
+            )
+        )
+
+    exc = captured.value
+
+    assert exc.kind == "invalid_json"
+
+    assert (
+        exc.in_tokens,
+        exc.out_tokens,
+        exc.usage_known,
+    ) == expected
````

## tests/unit/test_dev_tfidf_baseline.py

````diff
diff --git a/tests/unit/test_dev_tfidf_baseline.py b/tests/unit/test_dev_tfidf_baseline.py
--- a/tests/unit/test_dev_tfidf_baseline.py
+++ b/tests/unit/test_dev_tfidf_baseline.py
@@ -13,6 +13,10 @@
 def test_fit_requires_aligned_dev_examples():
     with pytest.raises(ValueError):
         DevTfidfBaseline.fit(["A"], [])
+
+
+def test_source_signal_preserves_other_exclusivity():
+    assert add_source_working_conditions(["Người lao động đặt cọc."], [("OTHER",)]) == (("OTHER",),)


 def test_source_security_signal_adds_second_clause_label_without_gold_lookup():
````
