"""
TransplantLink Donor Repository
"""

from typing import Dict, List, Optional, Any
from .base import BaseRepository


SYNTHETIC_SHOWCASE_DONORS = {
    "DON-4081": {
        "donor_id": "DON-4081",
        "donor_code": "Donor D-4081",
        "age": 28,
        "sex": "M",
        "blood_group": "O+",
        "donor_hospital_name": "Harborview Medical Center",
        "donor_hospital_city": "Seattle",
        "donor_hospital_state": "WA",
        "donor_type": "DCD",
        "cause_of_death": "Severe closed head trauma",
        "medical_history": {"infectious_panel": "HIV non-reactive, HBV non-reactive, HCV non-reactive"},
        "hla": {"a_1": "A2", "a_2": "A3", "b_1": "B8", "b_2": "B44", "dr_1": "DR4", "dr_2": "DR11"},
    },
    "DON-4092": {
        "donor_id": "DON-4092",
        "donor_code": "Donor D-4092",
        "age": 34,
        "sex": "F",
        "blood_group": "A+",
        "donor_hospital_name": "Swedish Medical Center",
        "donor_hospital_city": "Seattle",
        "donor_hospital_state": "WA",
        "donor_type": "DBD",
        "cause_of_death": "Cerebrovascular accident",
        "medical_history": {"infectious_panel": "HIV non-reactive, HBV non-reactive, HCV non-reactive"},
        "hla": {"a_1": "A1", "a_2": "A24", "b_1": "B8", "b_2": "B35", "dr_1": "DR3", "dr_2": "DR7"},
    },
    "DON-4105": {
        "donor_id": "DON-4105",
        "donor_code": "Donor D-4105",
        "age": 42,
        "sex": "M",
        "blood_group": "B+",
        "donor_hospital_name": "OHSU Medical Center",
        "donor_hospital_city": "Portland",
        "donor_hospital_state": "OR",
        "donor_type": "DBD",
        "cause_of_death": "Anoxic brain injury",
        "medical_history": {"infectious_panel": "HIV, HBV, HCV non-reactive"},
        "hla": {"a_1": "A2", "a_2": "A11", "b_1": "B15", "b_2": "B44", "dr_1": "DR4", "dr_2": "DR13"},
    },
    "DON-4112": {
        "donor_id": "DON-4112",
        "donor_code": "Donor D-4112",
        "age": 52,
        "sex": "M",
        "blood_group": "A+",
        "donor_hospital_name": "Providence St. Vincent",
        "donor_hospital_city": "Portland",
        "donor_hospital_state": "OR",
        "donor_type": "DBD",
        "cause_of_death": "Subarachnoid hemorrhage",
        "medical_history": {"infectious_panel": "HIV, HBV, HCV non-reactive"},
        "hla": {"a_1": "A1", "a_2": "A2", "b_1": "B*07:02", "b_2": "B18", "dr_1": "DR15", "dr_2": "DR4"},
    },
}


class DonorRepository(BaseRepository):
    def get_donor(self, donor_id: str) -> Optional[Dict[str, Any]]:
        if donor_id in SYNTHETIC_SHOWCASE_DONORS:
            return dict(SYNTHETIC_SHOWCASE_DONORS[donor_id])
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT d.*, 
                       h.name as donor_hospital_name, h.city as donor_hospital_city, h.state as donor_hospital_state,
                       dh.hla_a_1, dh.hla_a_2, dh.hla_b_1, dh.hla_b_2, dh.hla_dr_1, dh.hla_dr_2
                FROM donors d
                LEFT JOIN hospitals h ON d.donor_hospital_id = h.hospital_id
                LEFT JOIN donor_hla dh ON d.donor_id = dh.donor_id
                WHERE d.donor_id = ?
                """,
                (donor_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["medical_history"] = self.parse_json_field(data.get("medical_history"))
            data["hla"] = {
                "a_1": data.pop("hla_a_1", None),
                "a_2": data.pop("hla_a_2", None),
                "b_1": data.pop("hla_b_1", None),
                "b_2": data.pop("hla_b_2", None),
                "dr_1": data.pop("hla_dr_1", None),
                "dr_2": data.pop("hla_dr_2", None),
            }
            return data

    def get_donor_organs(self, donor_id: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT o.*, pe.status as preservation_status, pe.simulated_remaining_hours, pe.current_elapsed_hours
                FROM organs o
                LEFT JOIN preservation_events pe ON o.organ_id = pe.organ_id
                WHERE o.donor_id = ?
                ORDER BY o.organ_type ASC
                """,
                (donor_id,),
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["organ_metrics"] = self.parse_json_field(item.get("organ_metrics"))
                results.append(item)
            return results
