"""
TransplantLink Hospital & Centers Repository
"""

from typing import Dict, List, Optional, Any
from .base import BaseRepository


class HospitalRepository(BaseRepository):
    def get_hospital(self, hospital_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospitals WHERE hospital_id = ?", (hospital_id,))
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["transplant_programs"] = self.parse_json_field(data.get("transplant_programs"), default=[])
            return data

    def list_hospitals(
        self,
        organ_program: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            conditions = []
            params = []

            if city and city.upper() != "ALL":
                conditions.append("UPPER(city) = UPPER(?)")
                params.append(city)
            if state and state.upper() != "ALL":
                conditions.append("UPPER(state) = UPPER(?)")
                params.append(state)

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            sql = f"SELECT * FROM hospitals {where_clause} ORDER BY name ASC LIMIT ?"
            params.append(limit)

            cursor.execute(sql, params)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["transplant_programs"] = self.parse_json_field(item.get("transplant_programs"), default=[])
                if organ_program and organ_program.upper() != "ALL":
                    programs_upper = [p.upper() for p in item["transplant_programs"]]
                    if organ_program.upper() not in programs_upper:
                        continue
                results.append(item)
            return results

    def find_transplant_centers(self, organ_type: Optional[str] = None, location: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.list_hospitals(organ_program=organ_type, city=location)
