"""
TransplantLink Organ Repository
"""

from typing import Dict, List, Optional, Any
from .base import BaseRepository


SYNTHETIC_SHOWCASE_ORGANS = {
    "SYN-ORG-9921": {
        "organ_id": "SYN-ORG-9921",
        "organ_type": "Heart",
        "blood_group": "O+",
        "donor_id": "DON-4081",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "donor_hospital_name": "Harborview Medical Center",
        "donor_hospital_city": "Seattle",
        "donor_hospital_state": "WA",
        "donor_latitude": 13.0827,
        "donor_longitude": 80.2707,
        "donor_age": 28,
        "donor_sex": "M",
        "donor_weight_kg": 76.5,
        "donor_height_cm": 180.0,
        "donor_type": "DCD",
        "donor_screening_status": "CLEARED",
        "quality_grade": "GOOD",
        "preservation_method": "TransMedics OCS Pulsatile Machine Perfusion",
        "preservation_status": "ACTIVE_PERFUSION",
        "current_elapsed_hours": 1.4,
        "simulated_remaining_hours": 2.7,
        "organ_metrics": {
            "lvef": 62,
            "coronary_flow_l_min": 1.10,
            "perfusate_lactate_mmol_l": 2.1,
            "mean_aortic_pressure_mmhg": 82,
            "biopsy_endomyocardial": "No microthrombi, myocyte architecture preserved",
        },
        "donor_medical_history": {
            "cause_of_death": "Severe closed head trauma (motor vehicle accident)",
            "comorbidities": "None",
            "infectious_disease_panel": "HIV non-reactive, HBV non-reactive, HCV non-reactive, CMV IgG positive",
        },
        "simulation_parameters": {"temperature_c": 4.2, "flow_rate": 1.1},
        "donor_hla": {
            "a_1": "A2", "a_2": "A3",
            "b_1": "B8", "b_2": "B44",
            "dr_1": "DR4", "dr_2": "DR11",
        },
    },
    "SYN-ORG-8832": {
        "organ_id": "SYN-ORG-8832",
        "organ_type": "Kidney",
        "blood_group": "A+",
        "donor_id": "DON-4092",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "donor_hospital_name": "Swedish Medical Center",
        "donor_hospital_city": "Seattle",
        "donor_hospital_state": "WA",
        "donor_latitude": 13.0827,
        "donor_longitude": 80.2707,
        "donor_age": 34,
        "donor_sex": "F",
        "donor_weight_kg": 62.0,
        "donor_height_cm": 165.0,
        "donor_type": "DBD",
        "donor_screening_status": "CLEARED",
        "quality_grade": "GOOD",
        "preservation_method": "LifePort Kidney Perfusion",
        "preservation_status": "ACTIVE_PERFUSION",
        "current_elapsed_hours": 3.8,
        "simulated_remaining_hours": 14.3,
        "organ_metrics": {
            "resistance": 0.28,
            "flow_ml_min": 112,
            "terminal_creatinine": 0.8,
            "biopsy": "Glomerulosclerosis < 5%, interstitial fibrosis negative",
        },
        "donor_medical_history": {
            "cause_of_death": "Cerebrovascular accident (subarachnoid hemorrhage)",
            "comorbidities": "Mild essential hypertension",
            "infectious_disease_panel": "HIV non-reactive, HBV non-reactive, HCV non-reactive",
        },
        "simulation_parameters": {"temperature_c": 4.0, "resistance": 0.28},
        "donor_hla": {
            "a_1": "A1", "a_2": "A24",
            "b_1": "B8", "b_2": "B35",
            "dr_1": "DR3", "dr_2": "DR7",
        },
    },
    "SYN-ORG-7714": {
        "organ_id": "SYN-ORG-7714",
        "organ_type": "Liver",
        "blood_group": "B+",
        "donor_id": "DON-4105",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "donor_hospital_name": "OHSU Medical Center",
        "donor_hospital_city": "Portland",
        "donor_hospital_state": "OR",
        "donor_latitude": 13.0827,
        "donor_longitude": 80.2707,
        "donor_age": 42,
        "donor_sex": "M",
        "donor_weight_kg": 80.0,
        "donor_height_cm": 178.0,
        "donor_type": "DBD",
        "donor_screening_status": "CLEARED",
        "quality_grade": "GOOD",
        "preservation_method": "OrganOx Metra Normothermic Machine Perfusion",
        "preservation_status": "ACTIVE_PERFUSION",
        "current_elapsed_hours": 2.1,
        "simulated_remaining_hours": 6.2,
        "organ_metrics": {
            "bile_production_ml_hr": 14.0,
            "perfusate_lactate": 1.4,
            "macrosteatosis_pct": 8,
            "alt_u_l": 28,
            "ast_u_l": 32,
        },
        "donor_medical_history": {
            "cause_of_death": "Anoxic brain injury secondary to cardiac arrest",
            "comorbidities": "None",
            "infectious_disease_panel": "HIV, HBV, HCV non-reactive",
        },
        "simulation_parameters": {"temperature_c": 37.0},
        "donor_hla": {
            "a_1": "A2", "a_2": "A11",
            "b_1": "B15", "b_2": "B44",
            "dr_1": "DR4", "dr_2": "DR13",
        },
    },
    "SYN-ORG-9917": {
        "organ_id": "SYN-ORG-9917",
        "organ_type": "Heart",
        "blood_group": "A+",
        "donor_id": "DON-4112",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "donor_hospital_name": "Providence St. Vincent",
        "donor_hospital_city": "Portland",
        "donor_hospital_state": "OR",
        "donor_latitude": 13.0827,
        "donor_longitude": 80.2707,
        "donor_age": 52,
        "donor_sex": "M",
        "donor_weight_kg": 88.0,
        "donor_height_cm": 175.0,
        "donor_type": "DBD",
        "donor_screening_status": "CLEARED",
        "quality_grade": "FAIR",
        "preservation_method": "Static Cold Storage",
        "preservation_status": "COLD_STORAGE",
        "current_elapsed_hours": 3.2,
        "simulated_remaining_hours": 0.8,
        "organ_metrics": {
            "lvef": 50,
            "inotropic_support": "High dopamine requirement",
        },
        "donor_medical_history": {
            "cause_of_death": "Subarachnoid hemorrhage",
            "comorbidities": "Type 2 diabetes, smoker (15 pack-years)",
            "infectious_disease_panel": "HIV, HBV, HCV non-reactive",
        },
        "simulation_parameters": {"temperature_c": 4.0},
        "donor_hla": {
            "a_1": "A1", "a_2": "A2",
            "b_1": "B*07:02", "b_2": "B18",
            "dr_1": "DR15", "dr_2": "DR4",
        },
    },
}


class OrganRepository(BaseRepository):
    def get_organ(self, organ_id: str) -> Optional[Dict[str, Any]]:
        if organ_id in SYNTHETIC_SHOWCASE_ORGANS:
            return dict(SYNTHETIC_SHOWCASE_ORGANS[organ_id])
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT o.*, 
                       h.name as donor_hospital_name, h.city as donor_hospital_city, h.state as donor_hospital_state,
                       h.latitude as donor_latitude, h.longitude as donor_longitude,
                       d.age as donor_age, d.sex as donor_sex, d.weight_kg as donor_weight_kg, d.height_cm as donor_height_cm,
                       d.donor_type, d.screening_status as donor_screening_status,
                       d.medical_history as donor_medical_history,
                       dh.hla_a_1, dh.hla_a_2, dh.hla_b_1, dh.hla_b_2, dh.hla_dr_1, dh.hla_dr_2,
                       pe.preservation_method, pe.preservation_start, pe.current_elapsed_hours, 
                       pe.simulated_remaining_hours, pe.status as preservation_status, pe.simulation_parameters
                FROM organs o
                LEFT JOIN hospitals h ON o.donor_hospital_id = h.hospital_id
                LEFT JOIN donors d ON o.donor_id = d.donor_id
                LEFT JOIN donor_hla dh ON d.donor_id = dh.donor_id
                LEFT JOIN preservation_events pe ON o.organ_id = pe.organ_id
                WHERE o.organ_id = ?
                """,
                (organ_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["organ_metrics"] = self.parse_json_field(data.get("organ_metrics"))
            data["donor_medical_history"] = self.parse_json_field(data.get("donor_medical_history"))
            data["simulation_parameters"] = self.parse_json_field(data.get("simulation_parameters"))
            data["donor_hla"] = {
                "a_1": data.pop("hla_a_1", None),
                "a_2": data.pop("hla_a_2", None),
                "b_1": data.pop("hla_b_1", None),
                "b_2": data.pop("hla_b_2", None),
                "dr_1": data.pop("hla_dr_1", None),
                "dr_2": data.pop("hla_dr_2", None),
            }
            return data

    def search_available_organs(
        self,
        organ_type: Optional[str] = None,
        blood_group: Optional[str] = None,
        status: Optional[str] = "AVAILABLE",
        preservation_status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        conditions = []
        params = []

        if status and status.upper() != "ALL":
            conditions.append("UPPER(o.status) = UPPER(?)")
            params.append(status)
        if organ_type and organ_type.upper() != "ALL":
            conditions.append("UPPER(o.organ_type) = UPPER(?)")
            params.append(organ_type)
        if blood_group and blood_group.upper() != "ALL":
            conditions.append("o.blood_group = ?")
            params.append(blood_group)
        if preservation_status and preservation_status.upper() != "ALL":
            conditions.append("UPPER(pe.status) = UPPER(?)")
            params.append(preservation_status)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = f"""
                SELECT o.*, 
                       h.name as donor_hospital_name, h.city as donor_hospital_city,
                       pe.current_elapsed_hours, pe.simulated_remaining_hours, pe.status as preservation_status,
                       d.age as donor_age, d.sex as donor_sex, d.weight_kg as donor_weight_kg, d.height_cm as donor_height_cm,
                       dh.hla_a_1, dh.hla_a_2, dh.hla_b_1, dh.hla_b_2, dh.hla_dr_1, dh.hla_dr_2
                FROM organs o
                LEFT JOIN hospitals h ON o.donor_hospital_id = h.hospital_id
                LEFT JOIN donors d ON o.donor_id = d.donor_id
                LEFT JOIN donor_hla dh ON d.donor_id = dh.donor_id
                LEFT JOIN preservation_events pe ON o.organ_id = pe.organ_id
                {where_clause}
                ORDER BY 
                    CASE pe.status
                        WHEN 'CRITICAL' THEN 1
                        WHEN 'APPROACHING_LIMIT' THEN 2
                        WHEN 'WITHIN_WINDOW' THEN 3
                        ELSE 4
                    END,
                    pe.simulated_remaining_hours ASC
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["organ_metrics"] = self.parse_json_field(item.get("organ_metrics"))
                item["donor_hla"] = {
                    "a_1": item.pop("hla_a_1", None),
                    "a_2": item.pop("hla_a_2", None),
                    "b_1": item.pop("hla_b_1", None),
                    "b_2": item.pop("hla_b_2", None),
                    "dr_1": item.pop("hla_dr_1", None),
                    "dr_2": item.pop("hla_dr_2", None),
                }
                results.append(item)
            return results

    def get_preservation_status(self, organ_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT pe.*, o.organ_type, o.blood_group, o.quality_grade,
                       h.name as donor_hospital_name, h.city as donor_hospital_city
                FROM preservation_events pe
                JOIN organs o ON pe.organ_id = o.organ_id
                JOIN hospitals h ON o.donor_hospital_id = h.hospital_id
                WHERE pe.organ_id = ?
                """,
                (organ_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["simulation_parameters"] = self.parse_json_field(data.get("simulation_parameters"))
            return data
