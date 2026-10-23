"""
TransplantLink Deterministic Clinical Matching Engine
Performs multi-factor clinical matching evaluation and produces structured evidence.
NOTICE: Simulated demonstration criteria only. Decision support prototype.
"""

from typing import Dict, List, Optional, Any, Tuple
import uuid

# Configured simulation preservation limits (hours)
MAX_PRESERVATION_HOURS = {
    "KIDNEY": 30.0,
    "LIVER": 14.0,
    "HEART": 5.0,
    "LUNG": 7.0,
    "PANCREAS": 15.0,
}

# ABO Compatibility matrix (Donor Blood Group -> Compatible Recipient Blood Groups)
ABO_COMPATIBILITY = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"],
}


def check_abo_compatibility(donor_abo: str, recipient_abo: str) -> Tuple[bool, str]:
    donor = donor_abo.strip().upper()
    recipient = recipient_abo.strip().upper()
    compatible_recipients = ABO_COMPATIBILITY.get(donor, [])
    if recipient in compatible_recipients:
        return True, "COMPATIBLE"
    return False, "INCOMPATIBLE"


def evaluate_hla_compatibility(patient_hla: Dict[str, Any], donor_hla: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates 6-loci HLA compatibility (A1, A2, B1, B2, DR1, DR2).
    Returns matched loci count and clinical classification.
    """
    if not patient_hla or not donor_hla:
        return {
            "matched_loci": 0,
            "total_loci": 6,
            "classification": "UNKNOWN",
            "matched_alleles": [],
            "patient_alleles": [],
            "donor_alleles": [],
        }

    p_a = {str(patient_hla.get("a_1") or ""), str(patient_hla.get("a_2") or "")} - {""}
    d_a = {str(donor_hla.get("a_1") or ""), str(donor_hla.get("a_2") or "")} - {""}
    match_a = len(p_a.intersection(d_a))

    p_b = {str(patient_hla.get("b_1") or ""), str(patient_hla.get("b_2") or "")} - {""}
    d_b = {str(donor_hla.get("b_1") or ""), str(donor_hla.get("b_2") or "")} - {""}
    match_b = len(p_b.intersection(d_b))

    p_dr = {str(patient_hla.get("dr_1") or ""), str(patient_hla.get("dr_2") or "")} - {""}
    d_dr = {str(donor_hla.get("dr_1") or ""), str(donor_hla.get("dr_2") or "")} - {""}
    match_dr = len(p_dr.intersection(d_dr))

    total_matched = match_a + match_b + match_dr
    matched_alleles = list(p_a.intersection(d_a)) + list(p_b.intersection(d_b)) + list(p_dr.intersection(d_dr))

    if total_matched >= 4:
        classification = "FAVORABLE_DEMO"
    elif total_matched >= 2:
        classification = "MODERATE_DEMO"
    else:
        classification = "UNFAVORABLE_DEMO"

    return {
        "matched_loci": total_matched,
        "total_loci": 6,
        "classification": classification,
        "matched_alleles": matched_alleles,
        "patient_alleles": [
            f"A: {patient_hla.get('a_1')}/{patient_hla.get('a_2')}",
            f"B: {patient_hla.get('b_1')}/{patient_hla.get('b_2')}",
            f"DR: {patient_hla.get('dr_1')}/{patient_hla.get('dr_2')}",
        ],
        "donor_alleles": [
            f"A: {donor_hla.get('a_1')}/{donor_hla.get('a_2')}",
            f"B: {donor_hla.get('b_1')}/{donor_hla.get('b_2')}",
            f"DR: {donor_hla.get('dr_1')}/{donor_hla.get('dr_2')}",
        ],
    }


class MatchingEngine:
    def __init__(self, hospital_repo, logistics_repo):
        self.hospital_repo = hospital_repo
        self.logistics_repo = logistics_repo

    def evaluate_pair(self, patient: Dict[str, Any], organ: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a single patient-organ pair across 10 deterministic factors.
        Returns structured MatchEvaluation object with evidence.
        """
        evaluation_id = f"EVAL-{uuid.uuid4().hex[:10].upper()}"
        patient_id = patient["patient_id"]
        organ_id = organ["organ_id"]
        organ_type = organ["organ_type"].upper()

        positive_factors: List[str] = []
        limiting_factors: List[str] = []
        primary_limiting_factor: Optional[str] = None
        is_excluded = False

        # 1. Organ Type Validation
        if organ_type != patient["organ_needed"].upper():
            return {
                "evaluation_id": evaluation_id,
                "patient_id": patient_id,
                "organ_id": organ_id,
                "overall_result": "EXCLUDED",
                "match_level": "NONE",
                "abo_result": "N/A",
                "hla_result": "N/A",
                "size_result": "N/A",
                "organ_quality_result": "N/A",
                "preservation_result": "N/A",
                "transport_result": "N/A",
                "center_capability_result": "N/A",
                "primary_limiting_factor": "ORGAN_TYPE_MISMATCH",
                "positive_factors": [],
                "limiting_factors": [f"Organ type mismatch: requires {patient['organ_needed']}, found {organ['organ_type']}"],
                "explanation_data": {"reason": "ORGAN_TYPE_MISMATCH"},
            }

        # 2. Organ Status Check
        if organ.get("status") != "AVAILABLE":
            is_excluded = True
            primary_limiting_factor = primary_limiting_factor or "ORGAN_UNAVAILABLE"
            limiting_factors.append(f"Organ status is {organ.get('status')}")

        # 3. ABO Compatibility Check
        abo_compat, abo_status = check_abo_compatibility(organ["blood_group"], patient["blood_group"])
        if abo_compat:
            positive_factors.append(f"ABO criteria satisfied: donor {organ['blood_group']} → recipient {patient['blood_group']}")
            abo_result = "COMPATIBLE"
        else:
            is_excluded = True
            primary_limiting_factor = primary_limiting_factor or "ABO_INCOMPATIBLE"
            limiting_factors.append(f"ABO incompatibility: donor {organ['blood_group']} cannot donate to recipient {patient['blood_group']}")
            abo_result = "INCOMPATIBLE"

        # 4. HLA Loci Evaluation
        hla_data = evaluate_hla_compatibility(patient.get("hla", {}), organ.get("donor_hla", {}))
        matched_loci = hla_data["matched_loci"]
        if matched_loci >= 4:
            positive_factors.append(f"Favorable HLA profile: {matched_loci}/6 evaluated loci aligned ({hla_data['classification']})")
            hla_result = "FAVORABLE"
        elif matched_loci >= 2:
            positive_factors.append(f"Moderate HLA alignment: {matched_loci}/6 loci aligned")
            limiting_factors.append("Moderate HLA mismatch (crossmatch test required)")
            hla_result = "MODERATE"
        else:
            hla_result = "UNFAVORABLE"
            limiting_factors.append(f"Low HLA compatibility: only {matched_loci}/6 loci aligned")
            # If patient has high PRA (>50%), unfavorable HLA becomes an exclusion
            if float(patient.get("pra_percentage") or 0) > 50:
                is_excluded = True
                primary_limiting_factor = primary_limiting_factor or "HLA_LOW_COMPATIBILITY"

        # 5. Organ Quality
        quality = organ.get("quality_grade", "GOOD")
        if quality == "GOOD":
            positive_factors.append("Organ quality grade: GOOD with favorable physiological indicators")
            quality_result = "SATISFACTORY"
        elif quality == "FAIR":
            limiting_factors.append("Organ quality grade: FAIR (extended donor criteria)")
            quality_result = "MARGINAL_ACCEPTABLE"
        else:
            limiting_factors.append("Organ quality grade: MARGINAL (higher risk profile)")
            quality_result = "MARGINAL"
            if patient.get("urgency_level") in ["STATUS_1A", "CRITICAL"]:
                is_excluded = True
                primary_limiting_factor = primary_limiting_factor or "ORGAN_QUALITY"

        # 6. Center Capability Check
        center = self.hospital_repo.get_hospital(patient["transplant_center_id"])
        origin_hosp_id = organ.get("donor_hospital_id")
        donor_center = self.hospital_repo.get_hospital(origin_hosp_id)

        center_programs = [p.upper() for p in (center.get("transplant_programs") or [])] if center else []
        donor_programs = [p.upper() for p in (donor_center.get("transplant_programs") or [])] if donor_center else []

        if organ_type not in center_programs:
            is_excluded = True
            primary_limiting_factor = primary_limiting_factor or "CENTER_CAPABILITY_MISSING"
            limiting_factors.append(f"Receiving center lacks active authorization for {organ_type} transplantation")
            center_capability_result = "MISSING_PROGRAM"
        elif organ_type not in donor_programs:
            is_excluded = True
            primary_limiting_factor = primary_limiting_factor or "CENTER_CAPABILITY_MISSING"
            limiting_factors.append(f"Donor retrieval center lacks certified {organ_type} program")
            center_capability_result = "MISSING_PROGRAM"
        else:
            positive_factors.append(f"Receiving center ({center.get('name', 'Transplant Center')}) supports {organ_type} program")
            center_capability_result = "AUTHORIZED"

        # 7. Logistics & Transport Feasibility
        dest_hosp_id = patient.get("transplant_center_id")
        routes = self.logistics_repo.find_transport_options(origin_hosp_id, dest_hosp_id)

        best_route = routes[0] if routes else None
        if not best_route:
            is_excluded = True
            primary_limiting_factor = primary_limiting_factor or "TRANSPORT_NOT_FEASIBLE"
            limiting_factors.append("No active road or air transport route available between centers")
            transport_result = "NO_ROUTE"
            transit_minutes = 9999
            distance_km = 0
        else:
            transit_minutes = best_route["estimated_minutes"]
            distance_km = best_route["distance_km"]
            transit_hours = transit_minutes / 60.0
            hrs = transit_minutes // 60
            mins = transit_minutes % 60
            formatted_eta = f"{hrs}h {mins:02d}m" if hrs > 0 else f"{mins}m"
            positive_factors.append(f"Transport feasible: {distance_km} km ({best_route['transport_mode']}), ETA {formatted_eta}")
            transport_result = "FEASIBLE"

        # 8. Preservation Calculation & Cold Ischemia Constraint
        max_window = MAX_PRESERVATION_HOURS.get(organ_type, 24.0)
        elapsed_hours = float(organ.get("current_elapsed_hours") or 6.0)
        transit_hours = transit_minutes / 60.0
        projected_ischemia = elapsed_hours + transit_hours
        simulated_remaining_after_transit = max_window - projected_ischemia

        if projected_ischemia >= max_window or simulated_remaining_after_transit <= 1.0:
            is_excluded = True
            primary_limiting_factor = primary_limiting_factor or "PRESERVATION_EXCEEDED"
            limiting_factors.append(
                f"Preservation limit exceeded: {elapsed_hours:.1f}h elapsed + {transit_hours:.1f}h transit exceeds {max_window:.1f}h simulated limit"
            )
            preservation_result = "EXCEEDED"
        elif simulated_remaining_after_transit <= 4.0:
            limiting_factors.append(f"Preservation approaching limit: projected remaining {simulated_remaining_after_transit:.1f}h")
            preservation_result = "APPROACHING_LIMIT"
        else:
            positive_factors.append(f"Preservation within window: projected remaining {simulated_remaining_after_transit:.1f}h")
            preservation_result = "WITHIN_WINDOW"

        # 9. Size Compatibility (Height & Weight ratio)
        pat_wt = float(patient.get("weight_kg") or 70.0)
        donor_wt = float(organ.get("donor_weight_kg") or organ.get("weight_kg") or 70.0)
        size_ratio = donor_wt / pat_wt if pat_wt > 0 else 1.0
        if 0.75 <= size_ratio <= 1.35:
            size_result = "COMPATIBLE"
            positive_factors.append(f"Donor/recipient size ratio appropriate ({size_ratio:.2f})")
        else:
            size_result = "DISCREPANCY"
            limiting_factors.append(f"Donor/recipient body mass variance (donor: {donor_wt:.1f}kg, recipient: {pat_wt:.1f}kg)")
            if size_ratio < 0.6 or size_ratio > 1.6:
                is_excluded = True
                primary_limiting_factor = primary_limiting_factor or "SIZE_CONSTRAINT"

        # 10. Classification Outcome
        if is_excluded:
            overall_result = "EXCLUDED"
            classification = "NOT_POTENTIAL_MATCH"
            match_level = "EXCLUDED"
        else:
            overall_result = "POTENTIAL_MATCH"
            classification = "POTENTIAL_MATCH"
            if matched_loci >= 4 and quality == "GOOD" and preservation_result == "WITHIN_WINDOW":
                match_level = "HIGH"
            elif matched_loci >= 2 and preservation_result in ["WITHIN_WINDOW", "APPROACHING_LIMIT"]:
                match_level = "MODERATE"
            else:
                match_level = "REVIEW"

        # Safety limitation note
        limiting_factors.append("Crossmatch confirmation required prior to final clinical decision")

        explanation_data = {
            "result": overall_result,
            "match_level": match_level,
            "classification": classification,
            "primary_limiting_factor": primary_limiting_factor,
            "evidence": {
                "recipient_id": patient_id,
                "recipient_blood_group": patient["blood_group"],
                "organ_id": organ_id,
                "organ_blood_group": organ["blood_group"],
                "organ_type": organ_type,
                "hla_matched_loci": matched_loci,
                "hla_total_loci": 6,
                "hla_classification": hla_data["classification"],
                "quality_grade": quality,
                "distance_km": distance_km if best_route else 0,
                "transport_eta_minutes": transit_minutes if best_route else 0,
                "transport_mode": best_route["transport_mode"] if best_route else "NONE",
                "preservation_elapsed_hours": elapsed_hours,
                "preservation_max_window_hours": max_window,
                "projected_remaining_hours": round(max(0.0, simulated_remaining_after_transit), 1),
                "preservation_status": preservation_result,
                "donor_center": organ.get("donor_hospital_name") or organ.get("donor_hospital_id"),
                "recipient_center": center.get("name") if center else patient.get("transplant_center_id"),
            },
        }

        return {
            "evaluation_id": evaluation_id,
            "patient_id": patient_id,
            "organ_id": organ_id,
            "overall_result": overall_result,
            "match_level": match_level,
            "classification": classification,
            "abo_result": abo_result,
            "hla_result": hla_result,
            "size_result": size_result,
            "organ_quality_result": quality_result,
            "preservation_result": preservation_result,
            "transport_result": transport_result,
            "center_capability_result": center_capability_result,
            "primary_limiting_factor": primary_limiting_factor,
            "positive_factors": positive_factors,
            "limiting_factors": limiting_factors,
            "explanation_data": explanation_data,
            "transport": best_route,
            "hla_details": hla_data,
        }

    def find_potential_matches(self, patient: Dict[str, Any], candidate_organs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Star tool: Evaluates all available organs for a given patient.
        Returns matches, exclusions, and categorized exclusion summary.
        """
        matches = []
        exclusions = []
        exclusion_summary = {
            "abo_incompatible": 0,
            "transport_not_feasible": 0,
            "preservation_constraint": 0,
            "hla_low_compatibility": 0,
            "center_capability": 0,
            "size_constraint": 0,
            "organ_quality": 0,
            "other_configured_rules": 0,
        }

        for organ in candidate_organs:
            evaluation = self.evaluate_pair(patient, organ)
            if evaluation["overall_result"] == "POTENTIAL_MATCH":
                matches.append(evaluation)
            else:
                exclusions.append(evaluation)
                factor = evaluation.get("primary_limiting_factor")
                if factor == "ABO_INCOMPATIBLE":
                    exclusion_summary["abo_incompatible"] += 1
                elif factor == "TRANSPORT_NOT_FEASIBLE":
                    exclusion_summary["transport_not_feasible"] += 1
                elif factor == "PRESERVATION_EXCEEDED":
                    exclusion_summary["preservation_constraint"] += 1
                elif factor == "HLA_LOW_COMPATIBILITY":
                    exclusion_summary["hla_low_compatibility"] += 1
                elif factor == "CENTER_CAPABILITY_MISSING":
                    exclusion_summary["center_capability"] += 1
                elif factor == "SIZE_CONSTRAINT":
                    exclusion_summary["size_constraint"] += 1
                elif factor == "ORGAN_QUALITY":
                    exclusion_summary["organ_quality"] += 1
                else:
                    exclusion_summary["other_configured_rules"] += 1

        # Sort matches by high quality: HIGH -> MODERATE -> REVIEW, then lowest ETA
        def sort_key(item):
            rank_map = {"HIGH": 1, "MODERATE": 2, "REVIEW": 3}
            eta = item.get("transport", {}).get("estimated_minutes", 9999) if item.get("transport") else 9999
            return (rank_map.get(item["match_level"], 4), eta)

        matches.sort(key=sort_key)

        return {
            "patient_id": patient["patient_id"],
            "organ_type": patient["organ_needed"],
            "total_organs_considered": len(candidate_organs),
            "potential_matches": len(matches),
            "excluded_candidates": len(exclusions),
            "exclusion_summary": exclusion_summary,
            "matches": matches,
            "exclusions": exclusions,
        }
