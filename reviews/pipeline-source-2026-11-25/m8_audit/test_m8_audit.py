"""Hand-derived rank fixtures catch threshold, graph-loss and validation mistakes."""

from copy import deepcopy

import pytest

from m8_audit import audit


def report():
    rows = [
        {"case_id": "D2:HDLD001:0", "gold_clause_ref": "cl1", "gold_citation_id": "law:a",
         "primary_off_rank": 5, "primary_on_rank": 7, "oracle_off_rank": 6, "oracle_on_rank": None,
         "predicted_clause_labels": ["X"], "oracle_clause_labels": ["Y"],
         "gold_label_weight": 0.0, "gold_reachable_from_graph_seeds": False},
        {"case_id": "D2:HDLD001:1", "gold_clause_ref": "cl2", "gold_citation_id": "law:b",
         "primary_off_rank": 8, "primary_on_rank": None, "oracle_off_rank": 2, "oracle_on_rank": 2,
         "predicted_clause_labels": ["X"], "oracle_clause_labels": ["Y"],
         "gold_label_weight": 0.0, "gold_reachable_from_graph_seeds": False},
    ]
    return {"held_out_used": False, "status": "DEV_IN_SAMPLE_CLAUSE_LABEL_PREDICTIONS",
            "k": 5, "final_k": 8, "original_source_clusters": {"HDLD001": "a" * 64},
            "dev_case_details": rows,
            "m8_primary": {"total": 2, "graph_off": {"hits": 1, "total": 2},
                           "graph_on": {"hits": 0, "total": 2}},
            "m8_oracle_labels": {"total": 2, "graph_off": {"hits": 1, "total": 2},
                                 "graph_on": {"hits": 1, "total": 2}}}


def test_graph_on_only_loss_is_not_dropped_from_error_union():
    # Break caught: consuming only legacy graph-off misses hides the lost rank5 item.
    result = audit(report())
    assert result["counts"] == {"total": 2, "primary_off_hits": 1, "primary_on_hits": 0,
                                "oracle_off_hits": 1, "oracle_on_hits": 1,
                                "off_misses": 1, "on_misses": 2, "error_union": 2,
                                "graph_gains": 0, "graph_losses": 1,
                                "oracle_off_rescues": 1, "oracle_on_rescues": 1,
                                "oracle_off_regressions": 1, "oracle_on_regressions": 0}
    loss = next(x for x in result["errors"] if x["case_id"].endswith(":0"))
    assert loss["graph_regression"] is True
    assert loss["miss_primary_off"] is False
    assert loss["miss_primary_on"] is True
    assert loss["oracle_off_regression"] is True


def test_shared_role_query_is_counted_once_in_query_groups():
    # Break caught: treating role copies as independent source/query evidence.
    data = report()
    duplicate = deepcopy(data["dev_case_details"][1])
    duplicate["case_id"] = "D2:HDLD001:2"
    data["dev_case_details"].append(duplicate)
    for metric in ("m8_primary", "m8_oracle_labels"):
        data[metric]["total"] = 3
        for mode in ("graph_off", "graph_on"):
            data[metric][mode]["total"] = 3
    data["m8_oracle_labels"]["graph_off"]["hits"] = 2
    data["m8_oracle_labels"]["graph_on"]["hits"] = 2
    result = audit(data)
    assert result["counts"]["error_union"] == 3
    assert result["unique_query_citation_groups"] == 2
    assert result["original_source_families"] == 1


@pytest.mark.parametrize("change", ["metric", "duplicate_id", "missing_oracle", "boolean_rank", "out_of_pool", "heldout", "wrong_dataset", "missing_cluster"])
def test_invalid_or_incomplete_evidence_is_rejected(change):
    # Breaks caught: accepting fabricated aggregates, ambiguous cases or an unsupported evaluation split.
    data = report()
    if change == "metric":
        data["m8_primary"]["graph_on"]["hits"] = 2
    elif change == "duplicate_id":
        data["dev_case_details"][1]["case_id"] = "D2:HDLD001:0"
    elif change == "missing_oracle":
        del data["dev_case_details"][1]["oracle_on_rank"]
    elif change == "boolean_rank":
        data["dev_case_details"][1]["primary_off_rank"] = True
    elif change == "out_of_pool":
        data["dev_case_details"][1]["primary_off_rank"] = 9
    elif change == "heldout":
        data["held_out_used"] = True
    elif change == "wrong_dataset":
        data["dev_case_details"][1]["case_id"] = "T1:HDLD001:1"
    elif change == "missing_cluster":
        data["original_source_clusters"] = {}
    with pytest.raises(ValueError):
        audit(data)
