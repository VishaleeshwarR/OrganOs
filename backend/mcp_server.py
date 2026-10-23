"""
TransplantLink MCP Server (Model Context Protocol)
Standardized tool and resource access layer for clinical transplant coordination.
Notice: Prototype operates entirely on synthetic demonstration data.
"""

from typing import Dict, List, Optional, Any
from mcp.server.mcpserver import MCPServer
from backend.repository.patients import PatientRepository
from backend.repository.donors import DonorRepository
from backend.repository.organs import OrganRepository
from backend.repository.hospitals import HospitalRepository
from backend.repository.logistics import LogisticsRepository
from backend.repository.matching import MatchingRepository
from backend.repository.analytics import AnalyticsRepository
from backend.matching_engine import MatchingEngine

# Initialize repositories and engine
patient_repo = PatientRepository()
donor_repo = DonorRepository()
organ_repo = OrganRepository()
hospital_repo = HospitalRepository()
logistics_repo = LogisticsRepository()
matching_repo = MatchingRepository()
analytics_repo = AnalyticsRepository()
matching_engine = MatchingEngine(hospital_repo, logistics_repo)

mcp_server = MCPServer("transplantlink-mcp")

DISCLAIMER = "SYNTHETIC DATA · DEMONSTRATION PROTOTYPE ONLY"


# ---------------------------------------------------------------------------
# PATIENT TOOLS
# ---------------------------------------------------------------------------

@mcp_server.tool()
def get_patient(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve clinical profile, HLA alleles, PRA%, urgency, and waitlist record for a patient.
    """
    patient = patient_repo.get_patient(patient_id)
    if not patient:
        return {"error": f"Patient '{patient_id}' not found in registry", "status": "NOT_FOUND"}
    return {
        "patient": patient,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def search_patients(
    organ_needed: Optional[str] = None,
    blood_group: Optional[str] = None,
    urgency_level: Optional[str] = None,
    listing_status: Optional[str] = "ACTIVE",
    query: Optional[str] = None,
    limit: int = 25,
) -> Dict[str, Any]:
    """
    Search and filter patients in the transplant registry.
    """
    results = patient_repo.search_patients(
        organ_needed=organ_needed,
        blood_group=blood_group,
        urgency_level=urgency_level,
        listing_status=listing_status,
        query=query,
        limit=limit,
    )
    return {
        "count": len(results),
        "patients": results,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def get_waitlist() -> Dict[str, Any]:
    """
    Retrieve current waitlist summary broken down by organ and urgency level.
    """
    summary = patient_repo.get_waitlist_summary()
    return {
        "waitlist_summary": summary,
        "disclaimer": DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# ORGAN & DONOR TOOLS
# ---------------------------------------------------------------------------

@mcp_server.tool()
def search_available_organs(
    organ_type: Optional[str] = None,
    blood_group: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    """
    Search available procured organs with preservation metrics and donor details.
    """
    organs = organ_repo.search_available_organs(
        organ_type=organ_type,
        blood_group=blood_group,
        status="AVAILABLE",
        limit=limit,
    )
    if location:
        organs = [o for o in organs if location.upper() in (o.get("current_location") or "").upper() or location.upper() in (o.get("donor_hospital_city") or "").upper()]
    return {
        "count": len(organs),
        "organs": organs,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def get_organ_details(organ_id: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive physiological metrics, preservation timeline, and donor information for an organ.
    """
    organ = organ_repo.get_organ(organ_id)
    if not organ:
        return {"error": f"Organ '{organ_id}' not found in registry", "status": "NOT_FOUND"}
    return {
        "organ": organ,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def get_donor(donor_id: str) -> Dict[str, Any]:
    """
    Retrieve donor demographics, medical screening history, and HLA profile.
    """
    donor = donor_repo.get_donor(donor_id)
    if not donor:
        return {"error": f"Donor '{donor_id}' not found in registry", "status": "NOT_FOUND"}
    return {
        "donor": donor,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def get_donor_organs(donor_id: str) -> Dict[str, Any]:
    """
    Retrieve all organs procured from a specific donor with preservation states.
    """
    organs = donor_repo.get_donor_organs(donor_id)
    return {
        "donor_id": donor_id,
        "count": len(organs),
        "organs": organs,
        "disclaimer": DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# MATCHING TOOLS
# ---------------------------------------------------------------------------

@mcp_server.tool()
def evaluate_compatibility(patient_id: str, organ_id: str) -> Dict[str, Any]:
    """
    Perform deterministic clinical multi-factor evaluation between a recipient and a procured organ.
    Produces structured evidence, positive factors, limiting factors, and classification.
    """
    patient = patient_repo.get_patient(patient_id)
    if not patient:
        return {"error": f"Patient '{patient_id}' not found", "status": "NOT_FOUND"}

    organ = organ_repo.get_organ(organ_id)
    if not organ:
        return {"error": f"Organ '{organ_id}' not found", "status": "NOT_FOUND"}

    evaluation = matching_engine.evaluate_pair(patient, organ)
    # Persist evaluation for audit trail
    matching_repo.save_evaluation(evaluation)

    return {
        "evaluation": evaluation,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def find_potential_matches(patient_id: str, organ_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Star matching tool: Evaluates all available candidate organs for a patient.
    Returns matched candidates, excluded candidates, and full categorized exclusion summary.
    """
    patient = patient_repo.get_patient(patient_id)
    if not patient:
        return {"error": f"Patient '{patient_id}' not found", "status": "NOT_FOUND"}

    target_organ = organ_type or patient["organ_needed"]
    candidate_organs = organ_repo.search_available_organs(organ_type=target_organ, status="AVAILABLE", limit=200)

    result = matching_engine.find_potential_matches(patient, candidate_organs)

    # Persist evaluations for audit history
    for item in result["matches"] + result["exclusions"]:
        matching_repo.save_evaluation(item)

    result["disclaimer"] = DISCLAIMER
    return result


# ---------------------------------------------------------------------------
# HOSPITAL & LOGISTICS TOOLS
# ---------------------------------------------------------------------------

@mcp_server.tool()
def get_hospital(hospital_id: str) -> Dict[str, Any]:
    """
    Retrieve transplant center profile, certified programs, ICU capacity, and HLA lab readiness.
    """
    hospital = hospital_repo.get_hospital(hospital_id)
    if not hospital:
        return {"error": f"Hospital '{hospital_id}' not found", "status": "NOT_FOUND"}
    return {
        "hospital": hospital,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def find_transplant_centers(organ_type: Optional[str] = None, location: Optional[str] = None) -> Dict[str, Any]:
    """
    Find transplant centers authorized for a specific organ program in a given region.
    """
    centers = hospital_repo.find_transplant_centers(organ_type=organ_type, location=location)
    return {
        "count": len(centers),
        "centers": centers,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def find_transport_options(organ_id: str, destination_hospital_id: str) -> Dict[str, Any]:
    """
    Calculate and retrieve available transport routes, transit modes, distance, and ETAs between donor and recipient centers.
    """
    organ = organ_repo.get_organ(organ_id)
    if not organ:
        return {"error": f"Organ '{organ_id}' not found", "status": "NOT_FOUND"}

    origin_id = organ.get("donor_hospital_id")
    routes = logistics_repo.find_transport_options(origin_id, destination_hospital_id)

    return {
        "organ_id": organ_id,
        "origin_hospital_id": origin_id,
        "destination_hospital_id": destination_hospital_id,
        "routes_count": len(routes),
        "routes": routes,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def calculate_transport_eta(transport_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed transit route timing and arrival projections for a given transport ID.
    """
    details = logistics_repo.calculate_transport_eta(transport_id)
    if not details:
        return {"error": f"Transport route '{transport_id}' not found", "status": "NOT_FOUND"}
    return {
        "transport_route": details,
        "disclaimer": DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# PRESERVATION & ANALYTICS TOOLS
# ---------------------------------------------------------------------------

@mcp_server.tool()
def get_preservation_status(organ_id: str) -> Dict[str, Any]:
    """
    Retrieve preservation technique, cold ischemia elapsed time, and simulated remaining window.
    """
    preservation = organ_repo.get_preservation_status(organ_id)
    if not preservation:
        return {"error": f"Preservation record for '{organ_id}' not found", "status": "NOT_FOUND"}
    return {
        "preservation": preservation,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def get_registry_statistics() -> Dict[str, Any]:
    """
    Retrieve executive registry metrics, organ inventory tally, preservation urgency breakdown, and recent events.
    """
    stats = analytics_repo.get_registry_statistics()
    return {
        "statistics": stats,
        "disclaimer": DISCLAIMER,
    }


@mcp_server.tool()
def get_match_statistics(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve matching counts and candidate ratios for a specific listed recipient.
    """
    stats = analytics_repo.get_match_statistics(patient_id)
    return {
        "match_statistics": stats,
        "disclaimer": DISCLAIMER,
    }


# Tool Dispatcher dictionary for direct Python execution and FastAPI bridge
TOOL_FUNCTIONS = {
    "get_patient": get_patient,
    "search_patients": search_patients,
    "get_waitlist": get_waitlist,
    "search_available_organs": search_available_organs,
    "get_organ_details": get_organ_details,
    "get_donor": get_donor,
    "get_donor_organs": get_donor_organs,
    "evaluate_compatibility": evaluate_compatibility,
    "find_potential_matches": find_potential_matches,
    "get_hospital": get_hospital,
    "find_transplant_centers": find_transplant_centers,
    "find_transport_options": find_transport_options,
    "calculate_transport_eta": calculate_transport_eta,
    "get_preservation_status": get_preservation_status,
    "get_registry_statistics": get_registry_statistics,
    "get_match_statistics": get_match_statistics,
}
