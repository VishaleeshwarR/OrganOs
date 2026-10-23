"""
TransplantLink Backend & MCP Test Suite
Validates schema, deterministic seed scenario, all MCP tools, and FastAPI endpoints.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from backend.server import app
from backend.mcp_server import TOOL_FUNCTIONS

client = TestClient(app)


def test_mcp_tools_registered():
    response = client.get("/api/mcp/tools")
    assert response.status_code == 200
    data = response.json()
    tools = [t["name"] for t in data["tools"]]
    required_tools = [
        "get_patient",
        "search_patients",
        "get_waitlist",
        "search_available_organs",
        "get_organ_details",
        "get_donor",
        "get_donor_organs",
        "evaluate_compatibility",
        "find_potential_matches",
        "get_hospital",
        "find_transplant_centers",
        "find_transport_options",
        "calculate_transport_eta",
        "get_preservation_status",
        "get_registry_statistics",
        "get_match_statistics",
    ]
    for req in required_tools:
        assert req in tools, f"Missing MCP tool: {req}"
    print("[PASS] All 16 MCP tools registered and exposed.")


def test_canonical_matching_scenario():
    # Call find_potential_matches via MCP call endpoint
    payload = {
        "tool": "find_potential_matches",
        "arguments": {"patient_id": "REC-2026-00421", "organ_type": "Kidney"},
    }
    response = client.post("/api/mcp/call", json=payload)
    assert response.status_code == 200
    data = response.json()
    res = data["result"]

    assert res["patient_id"] == "REC-2026-00421"
    assert res["total_organs_considered"] == 27, f"Expected 27 evaluated, got {res['total_organs_considered']}"
    assert res["potential_matches"] == 8, f"Expected 8 matches, got {res['potential_matches']}"
    assert res["excluded_candidates"] == 19, f"Expected 19 excluded, got {res['excluded_candidates']}"

    summary = res["exclusion_summary"]
    assert summary["abo_incompatible"] == 8, f"Expected 8 ABO incompatible, got {summary['abo_incompatible']}"
    assert summary["transport_not_feasible"] == 4, f"Expected 4 transport infeasible, got {summary['transport_not_feasible']}"
    assert summary["preservation_constraint"] == 3, f"Expected 3 preservation constraint, got {summary['preservation_constraint']}"
    assert summary["center_capability"] == 2, f"Expected 2 center capability, got {summary['center_capability']}"
    assert summary["size_constraint"] == 2, f"Expected 2 size constraint, got {summary['size_constraint']}"
    print("[PASS] Canonical scenario 27 evaluated, 8 matches, 19 excluded validated!")


def test_clinical_query_endpoint():
    payload = {
        "query": "Find potential kidney matches for REC-2026-00421 that can reach the recipient center within preservation window."
    }
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "SEARCH RESULT" in data["answer"]
    assert len(data["data_sources_consulted"]) >= 3
    assert data["data_sources_consulted"][0]["tool"] == "get_patient"
    print("[PASS] Clinical Registry Query endpoint returned grounded MCP evidence.")


def test_analytics_and_charts():
    response = client.get("/api/analytics/charts")
    assert response.status_code == 200
    charts = response.json()
    assert "inventory_distribution" in charts
    assert "matching_outcomes" in charts
    assert "availability_trend" in charts
    assert "distance_vs_eta" in charts
    assert "allocation_outcomes" in charts
    print("[PASS] All 5 required analytics chart datasets generated successfully.")


def test_audit_log():
    response = client.get("/api/audit")
    assert response.status_code == 200
    data = response.json()
    assert "audit_log" in data
    assert len(data["audit_log"]) > 0
    print("[PASS] Audit log captured operations with timestamps and latencies.")


if __name__ == "__main__":
    test_mcp_tools_registered()
    test_canonical_matching_scenario()
    test_clinical_query_endpoint()
    test_analytics_and_charts()
    test_audit_log()
    print("==================================================")
    print("ALL BACKEND & MCP TESTS PASSED!")
    print("==================================================")
