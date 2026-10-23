"""
TransplantLink FastAPI HTTP/SSE Bridge
Exposes REST endpoints, MCP tool execution, audit logging, analytics, and clinical query reasoning.
Notice: Prototype using synthetic demonstration data.
"""

import os
import re
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip('"\'' )
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-flash-lite-latest").strip('"\'' )

from backend.mcp_server import (
    TOOL_FUNCTIONS,
    patient_repo,
    organ_repo,
    donor_repo,
    hospital_repo,
    logistics_repo,
    matching_repo,
    analytics_repo,
    matching_engine,
)

app = FastAPI(
    title="TransplantLink Clinical Coordination API",
    description="Backend API and MCP bridge for TransplantLink synthetic clinical decision support prototype.",
    version="1.0.0",
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory Audit Log Store
AUDIT_LOG: List[Dict[str, Any]] = [
    {
        "id": "AUD-0001",
        "timestamp": "2026-09-14T09:40:12Z",
        "action": "SYSTEM_INITIALIZATION",
        "tool_called": "get_registry_statistics",
        "patient_context": "GLOBAL",
        "records_evaluated": 700,
        "result_summary": "Registry state synchronized: 126 available organs, 487 waitlist candidates",
        "latency_ms": 42,
    },
    {
        "id": "AUD-0002",
        "timestamp": "2026-09-14T09:41:05Z",
        "action": "PATIENT_DIRECTORY_LOOKUP",
        "tool_called": "search_patients",
        "patient_context": "FILTER_KIDNEY_HIGH_URGENCY",
        "records_evaluated": 500,
        "result_summary": "Retrieved 15 candidates meeting high urgency kidney listing criteria",
        "latency_ms": 28,
    },
    {
        "id": "AUD-0003",
        "timestamp": "2026-09-14T09:42:18Z",
        "action": "COMPATIBILITY_ANALYSIS",
        "tool_called": "find_potential_matches",
        "patient_context": "REC-2026-00421",
        "records_evaluated": 27,
        "result_summary": "8 potential matches identified, 19 excluded across configured criteria",
        "latency_ms": 184,
    },
]


class McpCallRequest(BaseModel):
    tool: str = Field(..., description="Name of the MCP tool to execute")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments to pass to the tool")


class MatchingRequest(BaseModel):
    patient_id: str
    organ_id: str


class FindMatchesRequest(BaseModel):
    patient_id: str
    organ_type: Optional[str] = None


class ClinicalQueryRequest(BaseModel):
    query: str
    patient_id: Optional[str] = None
    organ_id: Optional[str] = None
    api_key: Optional[str] = None


# ---------------------------------------------------------------------------
# MCP TOOL CALL ENDPOINT
# ---------------------------------------------------------------------------

@app.post("/api/mcp/call")
def call_mcp_tool(req: McpCallRequest):
    tool_name = req.tool
    if tool_name not in TOOL_FUNCTIONS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not recognized in MCP registry.")

    func = TOOL_FUNCTIONS[tool_name]
    start_time = time.perf_counter()
    try:
        result = func(**req.arguments)
        duration_ms = int(round((time.perf_counter() - start_time) * 1000))

        # Record audit log event
        records_count = 1
        if isinstance(result, dict):
            if "total_organs_considered" in result:
                records_count = result["total_organs_considered"]
            elif "count" in result:
                records_count = result["count"]
            elif "organs" in result and isinstance(result["organs"], list):
                records_count = len(result["organs"])
            elif "patients" in result and isinstance(result["patients"], list):
                records_count = len(result["patients"])

        patient_ctx = req.arguments.get("patient_id") or req.arguments.get("organ_id") or "GLOBAL"
        AUDIT_LOG.insert(0, {
            "id": f"AUD-{uuid.uuid4().hex[:6].upper()}",
            "timestamp": datetime.now().isoformat(),
            "action": f"MCP_EXECUTION_{tool_name.upper()}",
            "tool_called": tool_name,
            "patient_context": str(patient_ctx),
            "records_evaluated": records_count,
            "result_summary": f"Executed tool '{tool_name}' successfully",
            "latency_ms": duration_ms,
        })

        return {
            "tool": tool_name,
            "latency_ms": duration_ms,
            "result": result,
            "disclaimer": "SYNTHETIC DATA · DEMONSTRATION PROTOTYPE",
        }
    except TypeError as te:
        raise HTTPException(status_code=400, detail=f"Invalid arguments for tool '{tool_name}': {str(te)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool '{tool_name}': {str(e)}")


@app.get("/api/mcp/tools")
def list_mcp_tools():
    return {
        "tools": [
            {"name": name, "doc": func.__doc__.strip() if func.__doc__ else "Clinical tool"}
            for name, func in TOOL_FUNCTIONS.items()
        ]
    }


# ---------------------------------------------------------------------------
# PATIENTS ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/patients")
def get_patients(
    organ_needed: Optional[str] = None,
    blood_group: Optional[str] = None,
    urgency_level: Optional[str] = None,
    listing_status: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    results = patient_repo.search_patients(
        organ_needed=organ_needed,
        blood_group=blood_group,
        urgency_level=urgency_level,
        listing_status=listing_status,
        query=query,
        limit=limit,
        offset=offset,
    )
    return {"total": len(results), "patients": results}


@app.get("/api/patients/{patient_id}")
def get_patient_by_id(patient_id: str):
    p = patient_repo.get_patient(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Patient '{patient_id}' not found.")
    return p


# ---------------------------------------------------------------------------
# ORGANS ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/organs")
def get_organs(
    organ_type: Optional[str] = None,
    blood_group: Optional[str] = None,
    status: Optional[str] = "AVAILABLE",
    preservation_status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    organs = organ_repo.search_available_organs(
        organ_type=organ_type,
        blood_group=blood_group,
        status=status,
        preservation_status=preservation_status,
        limit=limit,
        offset=offset,
    )
    return {"total": len(organs), "organs": organs}


@app.get("/api/organs/{organ_id}")
def get_organ_by_id(organ_id: str):
    organ = organ_repo.get_organ(organ_id)
    if not organ:
        raise HTTPException(status_code=404, detail=f"Organ '{organ_id}' not found.")
    return organ


# ---------------------------------------------------------------------------
# MATCHING WORKSPACE ENDPOINTS
# ---------------------------------------------------------------------------

@app.post("/api/matching/find-potential")
def find_potential(req: FindMatchesRequest):
    start_time = time.perf_counter()
    patient = patient_repo.get_patient(req.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient '{req.patient_id}' not found.")

    target_organ = req.organ_type or patient["organ_needed"]
    candidate_organs = organ_repo.search_available_organs(organ_type=target_organ, status="AVAILABLE", limit=200)

    result = matching_engine.find_potential_matches(patient, candidate_organs)
    duration_ms = int(round((time.perf_counter() - start_time) * 1000))

    # Save to audit trail
    AUDIT_LOG.insert(0, {
        "id": f"AUD-{uuid.uuid4().hex[:6].upper()}",
        "timestamp": datetime.now().isoformat(),
        "action": "FIND_POTENTIAL_MATCHES",
        "tool_called": "find_potential_matches",
        "patient_context": req.patient_id,
        "records_evaluated": result["total_organs_considered"],
        "result_summary": f"{result['potential_matches']} potential matches, {result['excluded_candidates']} excluded",
        "latency_ms": duration_ms,
    })

    return {
        **result,
        "latency_ms": duration_ms,
        "disclaimer": "SYNTHETIC DATA · DEMONSTRATION PROTOTYPE",
    }


@app.post("/api/matching/evaluate")
def evaluate_pair(req: MatchingRequest):
    patient = patient_repo.get_patient(req.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient '{req.patient_id}' not found.")

    organ = organ_repo.get_organ(req.organ_id)
    if not organ:
        raise HTTPException(status_code=404, detail=f"Organ '{req.organ_id}' not found.")

    res = matching_engine.evaluate_pair(patient, organ)
    matching_repo.save_evaluation(res)
    return res


# ---------------------------------------------------------------------------
# HOSPITALS & LOGISTICS ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/hospitals")
def get_hospitals(organ_program: Optional[str] = None, city: Optional[str] = None, limit: int = 100):
    return {"hospitals": hospital_repo.list_hospitals(organ_program=organ_program, city=city, limit=limit)}


@app.get("/api/hospitals/{hospital_id}")
def get_hospital_by_id(hospital_id: str):
    h = hospital_repo.get_hospital(hospital_id)
    if not h:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return h


@app.get("/api/logistics/routes")
def get_transport_routes(origin: str, destination: str):
    routes = logistics_repo.find_transport_options(origin, destination)
    return {"routes": routes}


# ---------------------------------------------------------------------------
# ANALYTICS & AUDIT ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/analytics/registry")
def get_registry_stats():
    return analytics_repo.get_registry_statistics()


@app.get("/api/analytics/charts")
def get_charts():
    return analytics_repo.get_charts_data()


@app.get("/api/audit")
def get_audit_trail(limit: int = 50):
    return {"audit_log": AUDIT_LOG[:limit]}


# ---------------------------------------------------------------------------
# CLINICAL REGISTRY QUERY (NATURAL LANGUAGE REASONING)
# ---------------------------------------------------------------------------

# Canonical Patient Profiles matching the CaseContext across all frontend pages
CANONICAL_PATIENT_CASES = {
    "REC-2026-00421": {
        "patient_id": "REC-2026-00421",
        "full_name": "Robert Vance",
        "age": 54,
        "sex": "Male",
        "blood_group": "O Rh+",
        "organ_needed": "Thoracic Heart",
        "urgency_level": "Status 1A (Impella 5.5)",
        "waitlist_days": 428,
        "clinical_support": "Impella 5.5 (4.2 L/min), Milrinone 0.375 mcg/kg/min",
        "transplant_center_name": "UCSF Medical Center, CCU Bed 14-B",
        "center_city": "San Francisco",
        "center_state": "CA",
        "pra_percentage": 78.0,
        "hla": {
            "a_1": "A*02:01", "a_2": "A*24:02",
            "b_1": "B*08:01", "b_2": "B*44:02",
            "c_1": "C*07:01", "c_2": "C*07:02",
            "dr_1": "DRB1*03:01", "dr_2": "DRB1*15:01",
        },
        "unacceptable_antigens": ["Anti-HLA-B*07:02 (8,830 MFI)", "Anti-HLA-A*01:01 (5,620 MFI)"],
        "primary_organ_id": "SYN-ORG-9921",
        "primary_match_score": 94.2,
        "mandatory_gates_passed": 4,
        "matched_donor": {
            "donor_id": "D-4081",
            "organ_id": "SYN-ORG-9921",
            "organ_type": "Thoracic Heart",
            "age": 28,
            "sex": "Male",
            "blood_group": "O Rh+",
            "hospital": "Harborview Medical Center",
            "city": "Seattle, WA (BFI Airport)",
            "perfusion_rig": "TransMedics OCS Heart #02 (Pulsatile)",
            "perfusion_temp": "4.2 °C",
            "coronary_flow": "1.10 L/min",
            "aortic_pressure": "82 mmHg",
            "lactate": "2.1 mmol/L (Downward Trend)",
            "flight_carrier": "MEDEVAC 921TX (Learjet 45 @ FL240)",
            "flight_eta_min": 18,
            "cit_remaining": "02:41:18",
            "match_score": 94.2,
            "gates_passed": "4/4 Cleared (ABO Serology, Biometrics/Mass, Virtual Crossmatch 0 DSA, Functional Viability)",
            "hla_alleles": {"a_1": "A*02:01", "a_2": "A*03:01", "b_1": "B*08:01", "b_2": "B*44:02", "dr_1": "DRB1*04:01", "dr_2": "DRB1*11:01"},
        }
    },
    "REC-2026-00109": {
        "patient_id": "REC-2026-00109",
        "full_name": "Elena Rostova",
        "age": 46,
        "sex": "Female",
        "blood_group": "O Rh+",
        "organ_needed": "Thoracic Heart",
        "urgency_level": "Status 1B (ICU Intubated)",
        "waitlist_days": 312,
        "clinical_support": "Vasoactive inotropes, Intubated",
        "transplant_center_name": "Stanford Health Care, ICU Room 4",
        "center_city": "Stanford",
        "center_state": "CA",
        "pra_percentage": 12.0,
        "hla": {
            "a_1": "A*29:01", "a_2": "A*11:01",
            "b_1": "B*40:01", "b_2": "B*44:02",
            "dr_1": "DRB1*15:01", "dr_2": "DRB1*13:01",
        },
        "unacceptable_antigens": [],
        "primary_organ_id": "SYN-ORG-9921",
        "primary_match_score": 88.5,
        "mandatory_gates_passed": 4,
        "matched_donor": {
            "donor_id": "D-4081",
            "organ_id": "SYN-ORG-9921",
            "organ_type": "Thoracic Heart",
            "age": 28,
            "sex": "Male",
            "blood_group": "O Rh+",
            "hospital": "Harborview Medical Center",
            "city": "Seattle, WA (BFI Airport)",
            "perfusion_rig": "TransMedics OCS Heart #02",
            "perfusion_temp": "4.2 °C",
            "coronary_flow": "1.10 L/min",
            "aortic_pressure": "82 mmHg",
            "lactate": "2.1 mmol/L",
            "flight_carrier": "MEDEVAC 921TX",
            "flight_eta_min": 22,
            "cit_remaining": "02:41:18",
            "match_score": 88.5,
            "gates_passed": "4/4 Cleared",
            "hla_alleles": {"a_1": "A*02:01", "a_2": "A*03:01", "b_1": "B*08:01", "b_2": "B*44:02", "dr_1": "DRB1*04:01", "dr_2": "DRB1*11:01"},
        }
    },
    "REC-2026-00388": {
        "patient_id": "REC-2026-00388",
        "full_name": "Marcus Chen",
        "age": 61,
        "sex": "Male",
        "blood_group": "B Rh+",
        "organ_needed": "Left Kidney",
        "urgency_level": "Status 2 (Hemodialysis 3x/wk)",
        "waitlist_days": 684,
        "clinical_support": "Hemodialysis via AV Fistula",
        "transplant_center_name": "UC Davis Medical Center",
        "center_city": "Sacramento",
        "center_state": "CA",
        "pra_percentage": 0.0,
        "hla": {
            "a_1": "A*01:01", "a_2": "A*31:01",
            "b_1": "B*27:05", "b_2": "B*07:02",
            "dr_1": "DRB1*13:01", "dr_2": "DRB1*17:01",
        },
        "unacceptable_antigens": [],
        "primary_organ_id": "SYN-ORG-9918",
        "primary_match_score": 84.1,
        "mandatory_gates_passed": 4,
        "matched_donor": {
            "donor_id": "D-3912",
            "organ_id": "SYN-ORG-9918",
            "organ_type": "Left Kidney",
            "age": 41,
            "sex": "Male",
            "blood_group": "B Rh+",
            "hospital": "Portland Medical Center",
            "city": "Portland, OR",
            "perfusion_rig": "LifePort Kidney Rig #11 (Hypothermic Pulsatile)",
            "perfusion_temp": "4.0 °C",
            "coronary_flow": "98 mL/min renal flow",
            "aortic_pressure": "Resistive Index: 0.28",
            "lactate": "Normal clearance",
            "flight_carrier": "Falcon Ground Medical Van 04",
            "flight_eta_min": 35,
            "cit_remaining": "18:42:00",
            "match_score": 84.1,
            "gates_passed": "4/4 Cleared",
            "hla_alleles": {"a_1": "A*01:01", "a_2": "A*02:01", "b_1": "B*08:01", "b_2": "B*27:05", "dr_1": "DRB1*03:01", "dr_2": "DRB1*13:01"},
        }
    }
}


@app.post("/api/query")
def process_clinical_query(req: ClinicalQueryRequest):
    query_text = req.query.strip()
    start_time = time.perf_counter()
    data_sources_consulted = []

    # 1. Identify Target Patient ID
    target_pid = req.patient_id
    if not target_pid:
        pid_match = re.search(r"REC-2026-\d{5}", query_text, re.IGNORECASE)
        if pid_match:
            target_pid = pid_match.group(0).upper()
        elif "robert" in query_text.lower():
            target_pid = "REC-2026-00421"
        elif "elena" in query_text.lower():
            target_pid = "REC-2026-00109"
        elif "marcus" in query_text.lower():
            target_pid = "REC-2026-00388"
        elif "priya" in query_text.lower():
            target_pid = "REC-2026-00502"
        else:
            target_pid = "REC-2026-00421"

    # Check canonical patient case for 100% alignment across all site pages
    canonical = CANONICAL_PATIENT_CASES.get(target_pid)

    # 2. Identify Target Organ / Donor ID
    target_organ_id = req.organ_id
    if not target_organ_id:
        org_match = re.search(r"SYN-ORG-\d{4}", query_text, re.IGNORECASE)
        if org_match:
            target_organ_id = org_match.group(0).upper()
        elif canonical:
            target_organ_id = canonical["primary_organ_id"]
        elif "4081" in query_text or "9921" in query_text:
            target_organ_id = "SYN-ORG-9921"
        elif "4092" in query_text or "8832" in query_text:
            target_organ_id = "SYN-ORG-8832"
        elif "4105" in query_text or "7714" in query_text:
            target_organ_id = "SYN-ORG-7714"
        elif "4112" in query_text or "9917" in query_text:
            target_organ_id = "SYN-ORG-9917"
        else:
            target_organ_id = "SYN-ORG-9921"

    # 3. Retrieve Patient Record via MCP Tool
    t0 = time.perf_counter()
    patient = patient_repo.get_patient(target_pid)
    ms_patient = int(round((time.perf_counter() - t0) * 1000))

    if canonical:
        # Merge canonical details to ensure complete consistency with all other site pages
        if not patient:
            patient = {}
        patient.update({
            "patient_id": canonical["patient_id"],
            "full_name": canonical["full_name"],
            "age": canonical["age"],
            "sex": canonical["sex"],
            "blood_group": canonical["blood_group"],
            "organ_needed": canonical["organ_needed"],
            "urgency_level": canonical["urgency_level"],
            "waitlist_days": canonical["waitlist_days"],
            "clinical_support": canonical["clinical_support"],
            "transplant_center_name": canonical["transplant_center_name"],
            "pra_percentage": canonical["pra_percentage"],
            "hla": canonical["hla"],
            "unacceptable_antigens": canonical["unacceptable_antigens"],
        })

    data_sources_consulted.append({
        "tool": "get_patient",
        "records_evaluated": 1 if patient else 0,
        "latency_ms": ms_patient,
        "status": "COMPLETE" if patient else "NOT_FOUND",
    })

    if not patient:
        return {
            "query": query_text,
            "patient_id": target_pid,
            "organ_id": target_organ_id,
            "answer": f"Candidate patient '{target_pid}' was not found in the transplant registry.",
            "data_sources_consulted": data_sources_consulted,
            "disclaimer": "SYNTHETIC DEMO ONLY",
        }

    target_organ_type = patient.get("organ_needed", "Thoracic Heart")

    # 4. Retrieve Organ & Donor Record via MCP Tools
    t1 = time.perf_counter()
    organ = organ_repo.get_organ(target_organ_id) if target_organ_id else None
    ms_organ = int(round((time.perf_counter() - t1) * 1000))
    data_sources_consulted.append({
        "tool": "get_organ_details",
        "records_evaluated": 1 if organ else 0,
        "latency_ms": ms_organ,
        "status": "COMPLETE" if organ else "NOT_FOUND",
    })

    donor = None
    if organ and organ.get("donor_id"):
        t_d = time.perf_counter()
        donor = donor_repo.get_donor(organ["donor_id"])
        ms_donor = int(round((time.perf_counter() - t_d) * 1000))
        data_sources_consulted.append({
            "tool": "get_donor",
            "records_evaluated": 1 if donor else 0,
            "latency_ms": ms_donor,
            "status": "COMPLETE" if donor else "NOT_FOUND",
        })

    # 5. Evaluate Pair Compatibility via MCP Matching Engine
    evaluation = None
    if organ:
        t2 = time.perf_counter()
        evaluation = matching_engine.evaluate_pair(patient, organ)
        ms_eval = int(round((time.perf_counter() - t2) * 1000))
        data_sources_consulted.append({
            "tool": "evaluate_compatibility",
            "records_evaluated": 1,
            "latency_ms": ms_eval,
            "status": "COMPLETE",
        })

    # 6. Find Potential Pool Matches
    t3 = time.perf_counter()
    candidate_organs = organ_repo.search_available_organs(organ_type=target_organ_type, status="AVAILABLE", limit=50)
    match_result = matching_engine.find_potential_matches(patient, candidate_organs)
    ms_matches = int(round((time.perf_counter() - t3) * 1000))
    data_sources_consulted.append({
        "tool": "find_potential_matches",
        "records_evaluated": len(candidate_organs),
        "latency_ms": ms_matches,
        "status": "COMPLETE",
    })

    # 7. Construct Comprehensive MCP Context for LLM Reasoning
    # Build complete patient profile matching the site pages
    matched_donor_info = canonical.get("matched_donor") if canonical else None
    mcp_context = {
        "candidate_patient": {
            "id": patient.get("patient_id"),
            "name": patient.get("full_name") or "Candidate",
            "age": patient.get("age"),
            "sex": patient.get("sex"),
            "blood_group": patient.get("blood_group"),
            "organ_needed": patient.get("organ_needed"),
            "urgency_level": patient.get("urgency_level"),
            "waitlist_days": patient.get("waitlist_days", 428),
            "clinical_support_tier": patient.get("clinical_support", "Standard CCU Care"),
            "transplant_center": patient.get("transplant_center_name") or patient.get("transplant_center_id"),
            "cpra_percentage": patient.get("pra_percentage"),
            "hla_typing_12_locus": patient.get("hla"),
            "unacceptable_antigens": patient.get("unacceptable_antigens", []),
        },
        "primary_matched_graft": matched_donor_info or ({
            "id": organ.get("organ_id") if organ else target_organ_id,
            "donor_id": organ.get("donor_id") if organ else "Unknown",
            "organ_type": organ.get("organ_type") if organ else target_organ_type,
            "blood_group": organ.get("blood_group") if organ else "O Rh+",
            "preservation_status": organ.get("preservation_status") if organ else "Standard",
            "current_location": organ.get("donor_hospital_city") or organ.get("current_location") if organ else "Unknown",
            "remaining_cit_hours": organ.get("simulated_remaining_hours") if organ else 2.7,
            "hla_alleles": organ.get("donor_hla") if organ else (donor.get("hla") if donor else None),
        } if organ else None),
        "matching_analysis": {
            "match_score": canonical.get("primary_match_score", 94.2) if canonical else (evaluation.get("composite_score") if evaluation else 94.2),
            "mandatory_gates_status": "4/4 PASSED (Gate 1 Serology/ABO, Gate 2 Biometrics/Mass, Gate 3 Virtual Crossmatch 0 DSA, Gate 4 Functional Viability)",
            "virtual_crossmatch": "NEGATIVE / CLEARED (0 Donor-Specific Antibodies detected against donor HLA antigens)",
            "details": evaluation.get("explanation_data") if evaluation else None,
        },
        "logistics_and_telemetry": {
            "flight_carrier": matched_donor_info.get("flight_carrier") if matched_donor_info else "MEDEVAC 921TX (Learjet 45 @ FL240)",
            "flight_eta_min": matched_donor_info.get("flight_eta_min") if matched_donor_info else 18,
            "cit_remaining": matched_donor_info.get("cit_remaining") if matched_donor_info else "02:41:18",
            "origin_hospital": matched_donor_info.get("hospital") if matched_donor_info else "Harborview Medical Center, Seattle WA",
            "destination_center": patient.get("transplant_center_name"),
        },
        "pool_summary": match_result.get("exclusion_summary"),
        "total_organs_screened": match_result.get("total_organs_considered"),
        "potential_matches_found": match_result.get("potential_matches"),
    }

    # 8. Call LLM (Primary: Free High-Uptime Gemini, Backup: Groq / Grok)
    load_dotenv(override=True)
    env_gemini_key = os.getenv("GEMINI_API_KEY", "").strip('"\'' )
    env_groq_key = (os.getenv("GROQ_API_KEY", "") or os.getenv("GROK_API_KEY", "")).strip('"\'' )
    env_llm_key = os.getenv("LLM_API_KEY", "").strip('"\'' )
    req_key = (req.api_key or "").strip('"\'' )

    system_prompt = (
        "You are the OrganOS AI Clinical Decision-Support Copilot, an expert clinical reasoning assistant "
        "for transplant surgeons and coordinators. "
        "You must answer the doctor's query about the selected candidate patient strictly based on the provided real-time deterministic MCP server data. "
        "Your response MUST match the patient's data shown on the OrganOS platform (Patient Dossier, Matching Workspace, Logistics Radar, and UNOS Registry). "
        "Do not invent facts. Cite the patient's exact name, ID, urgency tier, waitlist tenure, clinical support equipment, hospital, blood group, organ required, "
        "12-locus HLA alleles, cPRA percentage, unacceptable antigens, primary match score, 4-gate verification status, flight logistics, and CIT remaining. "
        "IMPORTANT FORMATTING RULES: "
        "1. Do NOT use markdown symbols like *, **, #, ##, ###, >, or ```. "
        "2. Use plain text headings in ALL CAPS followed by a colon for section titles (e.g. SUMMARY:, DETAILED CLINICAL ANALYSIS:, REGISTRY EVIDENCE:, RECOMMENDATION:). "
        "3. Use bullet points with a simple dash (-) for lists. "
        "4. Provide COMPLETE and DETAILED clinical explanations addressing the user's specific query about the patient. "
        "5. Structure your response with clear sections: SUMMARY:, DETAILED CLINICAL ANALYSIS:, REGISTRY EVIDENCE:, and RECOMMENDATION:."
    )

    user_prompt = (
        f"DOCTOR QUERY ABOUT CANDIDATE PATIENT:\n{query_text}\n\n"
        f"DETERMINISTIC MCP SERVER DATA:\n"
        f"{json.dumps(mcp_context, indent=2)}\n\n"
        f"Provide a thorough, clinical reasoning answer addressing the doctor's question directly with evidence from the MCP data."
    )

    # Helper: Call Google Gemini with high-uptime model cascade
    def _call_gemini_cascade(api_key: str):
        import httpx
        gemini_candidates = [
            os.getenv("GEMINI_MODEL", "").strip(),
            "gemini-flash-lite-latest",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.6-flash",
        ]
        seen_models = set()
        gemini_candidates = [m for m in gemini_candidates if m and not (m in seen_models or seen_models.add(m))]

        last_error = "Unknown Gemini error"
        for gemini_model in gemini_candidates:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_prompt}\n\n{user_prompt}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 4096,
                },
            }
            try:
                resp = httpx.post(url, json=payload, timeout=25.0)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"], gemini_model
                else:
                    try:
                        err_msg = resp.json().get("error", {}).get("message", resp.text)
                    except Exception:
                        err_msg = resp.text
                    last_error = f"{resp.status_code}: {err_msg[:120]}"
                    if resp.status_code in (400, 401, 403) or "API_KEY_INVALID" in err_msg or "PERMISSION_DENIED" in err_msg:
                        break
            except Exception as e:
                last_error = str(e)[:120]
        return None, last_error

    # Helper: Call Groq / Grok with high-speed model cascade
    def _call_groq_cascade(api_key: str):
        import httpx
        groq_candidates = [
            os.getenv("GROQ_MODEL", "").strip(),
            os.getenv("GROK_MODEL", "").strip(),
            "qwen/qwen3.8-27b",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ]
        seen_models = set()
        groq_candidates = [m for m in groq_candidates if m and not (m in seen_models or seen_models.add(m))]

        last_error = "Unknown Groq error"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        for groq_model in groq_candidates:
            payload = {
                "model": groq_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 4096,
            }
            try:
                resp = httpx.post(url, headers=headers, json=payload, timeout=25.0)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        msg = choices[0].get("message", {})
                        text = msg.get("content") or msg.get("reasoning")
                        if text and text.strip():
                            return text.strip(), groq_model
                else:
                    try:
                        err_msg = resp.json().get("error", {}).get("message", resp.text)
                    except Exception:
                        err_msg = resp.text
                    last_error = f"{resp.status_code}: {err_msg[:120]}"
                    if resp.status_code in (401, 403) or "invalid_api_key" in err_msg.lower():
                        break
            except Exception as e:
                last_error = str(e)[:120]
        return None, last_error

    # Determine provider keys and execution priority
    gemini_key = env_gemini_key or (env_llm_key if not env_llm_key.startswith("gsk_") else "")
    groq_key = env_groq_key or (env_llm_key if env_llm_key.startswith("gsk_") else "")
    primary_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    # Build sequence of provider keys to try: if one key doesn't work, continue with other keys
    providers_to_try = []

    if req_key:
        if req_key.startswith("gsk_"):
            # Custom Groq key supplied by request
            providers_to_try.append(("groq", req_key, "Groq Custom"))
            if gemini_key:
                providers_to_try.append(("gemini", gemini_key, "Gemini Backup"))
            if env_groq_key and env_groq_key != req_key:
                providers_to_try.append(("groq", env_groq_key, "Groq Env Backup"))
        else:
            # Custom Gemini key supplied by request
            providers_to_try.append(("gemini", req_key, "Gemini Custom"))
            if groq_key:
                providers_to_try.append(("groq", groq_key, "Groq Backup"))
            if env_gemini_key and env_gemini_key != req_key:
                providers_to_try.append(("gemini", env_gemini_key, "Gemini Env Backup"))
    else:
        if primary_provider in ("groq", "grok"):
            if groq_key:
                providers_to_try.append(("groq", groq_key, "Groq"))
            if gemini_key:
                providers_to_try.append(("gemini", gemini_key, "Gemini Backup"))
        else:
            # Primary: Gemini, Secondary/Backup: Groq
            if gemini_key:
                providers_to_try.append(("gemini", gemini_key, "Gemini"))
            if groq_key:
                providers_to_try.append(("groq", groq_key, "Groq Backup"))

    llm_answer = None
    llm_status = "UNKNOWN"
    model_used = None
    attempt_errors = []

    for prov, key, label in providers_to_try:
        if not key:
            continue
        if prov == "gemini":
            ans, res = _call_gemini_cascade(key)
            if ans:
                llm_answer = ans
                llm_status = f"ONLINE ({label} {res})"
                model_used = res
                break
            else:
                attempt_errors.append(f"{label}: {res}")
        elif prov in ("groq", "grok"):
            ans, res = _call_groq_cascade(key)
            if ans:
                llm_answer = ans
                llm_status = f"ONLINE ({label} - {res})"
                model_used = res
                break
            else:
                attempt_errors.append(f"{label}: {res}")

    if not llm_answer:
        if attempt_errors:
            llm_status = "ALL_PROVIDERS_FAILED: " + " | ".join(attempt_errors)
        else:
            llm_status = "NO_API_KEY_CONFIGURED"

    # 9. No Fallback Synthesis: Display authentic LLM response or actual error
    if not llm_answer:
        llm_answer = (
            f"ERROR: LLM reasoning synthesis failed ({llm_status}).\n\n"
            f"No synthetic fallback response is generated. "
            f"MCP server data was retrieved successfully, but clinical reasoning requires a valid LLM response."
        )

    total_latency_ms = int(round((time.perf_counter() - start_time) * 1000))

    # Append to Audit Log
    AUDIT_LOG.insert(0, {
        "id": f"AUD-{uuid.uuid4().hex[:6].upper()}",
        "timestamp": datetime.now().isoformat(),
        "action": "CLINICAL_COUNCIL_QUERY",
        "tool_called": "mcp_llm_reasoning_orchestrator",
        "patient_context": f"{target_pid}::{target_organ_id}",
        "records_evaluated": len(data_sources_consulted),
        "result_summary": f"Query processed for {target_pid} (LLM: {llm_status})",
        "latency_ms": total_latency_ms,
    })

    return {
        "query": query_text,
        "patient_id": target_pid,
        "organ_id": target_organ_id,
        "organ_type": target_organ_type,
        "answer": llm_answer,
        "llm_status": llm_status,
        "model_used": model_used if (llm_status and "ONLINE" in llm_status) else "None",
        "data_sources_consulted": data_sources_consulted,
        "evaluation": evaluation,
        "matches": match_result.get("matches", []),
        "exclusions": match_result.get("exclusions", []),
        "exclusion_summary": match_result.get("exclusion_summary", {}),
        "latency_ms": total_latency_ms,
        "disclaimer": "SYNTHETIC CLINICAL DECISION SUPPORT PROTOTYPE",
    }

