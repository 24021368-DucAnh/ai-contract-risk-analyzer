"""Validate and explain saved Dev retrieval reports; never rerun or tune models."""

import math
import re


def audit(report):
    """Reconcile rank-derived counts and retain the union of both modes' errors."""
    try:
        if report["held_out_used"] is not False or report["status"] != "DEV_IN_SAMPLE_CLAUSE_LABEL_PREDICTIONS":
            raise ValueError("Only the declared D1/D2 in-sample Dev protocol is supported")
        k, pool = report["k"], report["final_k"]
        if type(k) is not int or type(pool) is not int or not 1 <= k <= pool:
            raise ValueError("Invalid retrieval thresholds")
        rows = report["dev_case_details"]
        if not rows:
            raise ValueError("No case-level evidence")
        ids, sources, groups = set(), set(), set()
        counts = dict.fromkeys(("total", "primary_off_hits", "primary_on_hits", "oracle_off_hits",
                               "oracle_on_hits", "off_misses", "on_misses", "error_union",
                               "graph_gains", "graph_losses", "oracle_off_rescues", "oracle_on_rescues",
                               "oracle_off_regressions", "oracle_on_regressions"), 0)
        errors = []
        for row in rows:
            case = row["case_id"]
            parts = case.split(":")
            if len(parts) != 3 or parts[0] not in {"D1", "D2"} or not parts[2].isdigit() or case in ids:
                raise ValueError("Invalid or duplicated case identity")
            ids.add(case)
            dataset, document_id, _ = parts
            source = report["original_source_clusters"].get(document_id)
            if not isinstance(source, str) or not re.fullmatch(r"[0-9a-f]{64}", source):
                raise ValueError("Missing source family binding")
            sources.add(source)
            ranks = {}
            for name in ("primary_off", "primary_on", "oracle_off", "oracle_on"):
                rank = row[name + "_rank"]
                if rank is not None and (type(rank) is not int or not 1 <= rank <= pool):
                    raise ValueError("Invalid or out-of-pool rank")
                ranks[name] = rank
            weight = row["gold_label_weight"]
            if type(weight) not in (int, float) or not math.isfinite(weight) or weight < 0:
                raise ValueError("Invalid label weight")
            if type(row["gold_reachable_from_graph_seeds"]) is not bool:
                raise ValueError("Missing graph reachability evidence")
            group = (dataset, document_id, row["gold_clause_ref"], row["gold_citation_id"])
            groups.add(group)
            hit = {name: rank is not None and rank <= k for name, rank in ranks.items()}
            counts["total"] += 1
            for name, value in hit.items():
                counts[name + "_hits"] += int(value)
            off_miss, on_miss = not hit["primary_off"], not hit["primary_on"]
            loss = hit["primary_off"] and on_miss
            gain = off_miss and hit["primary_on"]
            rescue_off = off_miss and hit["oracle_off"]
            rescue_on = on_miss and hit["oracle_on"]
            regress_off = hit["primary_off"] and not hit["oracle_off"]
            regress_on = hit["primary_on"] and not hit["oracle_on"]
            for name, value in (("off_misses", off_miss), ("on_misses", on_miss),
                                ("error_union", off_miss or on_miss), ("graph_losses", loss),
                                ("graph_gains", gain), ("oracle_off_rescues", rescue_off),
                                ("oracle_on_rescues", rescue_on), ("oracle_off_regressions", regress_off),
                                ("oracle_on_regressions", regress_on)):
                counts[name] += int(value)
            if off_miss or on_miss:
                errors.append({
                    "case_id": case, "dataset": dataset, "document_id": document_id,
                    "source_family_sha256": source, "gold_clause_ref": row["gold_clause_ref"],
                    "gold_citation_id": row["gold_citation_id"],
                    "query_citation_group": "|".join(group),
                    **{name + "_rank": rank for name, rank in ranks.items()},
                    "predicted_clause_labels": row["predicted_clause_labels"],
                    "oracle_clause_labels": row["oracle_clause_labels"],
                    "miss_primary_off": off_miss, "miss_primary_on": on_miss,
                    "graph_regression": loss, "oracle_off_rescue": rescue_off,
                    "oracle_on_rescue": rescue_on, "zero_predicted_label_weight": weight == 0,
                    "oracle_off_regression": regress_off, "oracle_on_regression": regress_on,
                    "gold_reachable_from_graph_seeds": row["gold_reachable_from_graph_seeds"],
                    "interpretation": "OBSERVATIONS_AND_COUNTERFACTUAL_DIAGNOSTICS_NOT_PROVEN_CAUSAL_ROOT_CAUSE",
                })
        for metric, prefix in (("m8_primary", "primary"), ("m8_oracle_labels", "oracle")):
            saved = report[metric]
            if saved["total"] != counts["total"]:
                raise ValueError("Aggregate total differs from case inventory")
            for mode in ("off", "on"):
                values = saved["graph_" + mode]
                if values["total"] != counts["total"] or values["hits"] != counts[prefix + "_" + mode + "_hits"]:
                    raise ValueError("Saved metrics differ from case-level ranks")
        return {"counts": counts, "errors": errors,
                "unique_query_citation_groups": len(groups),
                "error_query_citation_groups": len({x["query_citation_group"] for x in errors}),
                "original_source_families": len(sources), "k": k, "final_k": pool,
                "new_inference_run": False, "held_out_used": False}
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError("Incomplete case-level evidence") from exc
