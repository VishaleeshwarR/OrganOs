"""
TransplantLink Patient Repository
"""

from typing import Dict, List, Optional, Any
from .base import BaseRepository


class PatientRepository(BaseRepository):
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT p.*, 
                       h.name as transplant_center_name, h.city as center_city, h.state as center_state,
                       hla.hla_a_1, hla.hla_a_2, hla.hla_b_1, hla.hla_b_2, hla.hla_dr_1, hla.hla_dr_2
                FROM patients p
                LEFT JOIN hospitals h ON p.transplant_center_id = h.hospital_id
                LEFT JOIN patient_hla hla ON p.patient_id = hla.patient_id
                WHERE p.patient_id = ?
                """,
                (patient_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["hla"] = {
                "a_1": data.pop("hla_a_1", None),
                "a_2": data.pop("hla_a_2", None),
                "b_1": data.pop("hla_b_1", None),
                "b_2": data.pop("hla_b_2", None),
                "dr_1": data.pop("hla_dr_1", None),
                "dr_2": data.pop("hla_dr_2", None),
            }
            return data

    def search_patients(
        self,
        organ_needed: Optional[str] = None,
        blood_group: Optional[str] = None,
        urgency_level: Optional[str] = None,
        listing_status: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        conditions = []
        params = []

        if organ_needed and organ_needed.upper() != "ALL":
            conditions.append("UPPER(p.organ_needed) = UPPER(?)")
            params.append(organ_needed)
        if blood_group and blood_group.upper() != "ALL":
            conditions.append("p.blood_group = ?")
            params.append(blood_group)
        if urgency_level and urgency_level.upper() != "ALL":
            conditions.append("UPPER(p.urgency_level) = UPPER(?)")
            params.append(urgency_level)
        if listing_status and listing_status.upper() != "ALL":
            conditions.append("UPPER(p.listing_status) = UPPER(?)")
            params.append(listing_status)
        if query:
            conditions.append("(p.patient_id LIKE ? OR h.name LIKE ? OR h.city LIKE ?)")
            q = f"%{query}%"
            params.extend([q, q, q])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = f"""
                SELECT p.*, 
                       h.name as transplant_center_name, h.city as center_city,
                       hla.hla_a_1, hla.hla_a_2, hla.hla_b_1, hla.hla_b_2, hla.hla_dr_1, hla.hla_dr_2
                FROM patients p
                LEFT JOIN hospitals h ON p.transplant_center_id = h.hospital_id
                LEFT JOIN patient_hla hla ON p.patient_id = hla.patient_id
                {where_clause}
                ORDER BY 
                    CASE p.urgency_level 
                        WHEN 'STATUS_1A' THEN 1 
                        WHEN 'CRITICAL' THEN 2
                        WHEN 'HIGH' THEN 3 
                        WHEN 'STATUS_1B' THEN 4 
                        WHEN 'STANDARD' THEN 5 
                        ELSE 6 
                    END,
                    p.waitlist_date ASC
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["hla"] = {
                    "a_1": item.pop("hla_a_1", None),
                    "a_2": item.pop("hla_a_2", None),
                    "b_1": item.pop("hla_b_1", None),
                    "b_2": item.pop("hla_b_2", None),
                    "dr_1": item.pop("hla_dr_1", None),
                    "dr_2": item.pop("hla_dr_2", None),
                }
                results.append(item)
            return results

    def get_waitlist_summary(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM patients WHERE listing_status = 'ACTIVE'")
            total_active = cursor.fetchone()["total"]

            cursor.execute(
                """
                SELECT organ_needed, COUNT(*) as count 
                FROM patients 
                WHERE listing_status = 'ACTIVE' 
                GROUP BY organ_needed
                """
            )
            by_organ = {row["organ_needed"]: row["count"] for row in cursor.fetchall()}

            cursor.execute(
                """
                SELECT urgency_level, COUNT(*) as count 
                FROM patients 
                WHERE listing_status = 'ACTIVE' 
                GROUP BY urgency_level
                """
            )
            by_urgency = {row["urgency_level"]: row["count"] for row in cursor.fetchall()}

            return {
                "total_active_waitlist": total_active,
                "by_organ": by_organ,
                "by_urgency": by_urgency,
            }
