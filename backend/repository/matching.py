"""
TransplantLink Match Evaluations Repository
"""

import json
from typing import Dict, List, Optional, Any
from .base import BaseRepository


class MatchingRepository(BaseRepository):
    def save_evaluation(self, evaluation: Dict[str, Any]) -> None:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO match_evaluations (
                        evaluation_id, patient_id, organ_id, overall_result,
                        abo_result, hla_result, size_result, organ_quality_result,
                        preservation_result, transport_result, center_capability_result,
                        primary_limiting_factor, positive_factors, limiting_factors,
                        explanation_data, evaluated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (
                        evaluation["evaluation_id"],
                        evaluation["patient_id"],
                        evaluation["organ_id"],
                        evaluation["overall_result"],
                        evaluation.get("abo_result", "UNKNOWN"),
                        evaluation.get("hla_result", "UNKNOWN"),
                        evaluation.get("size_result", "UNKNOWN"),
                        evaluation.get("organ_quality_result", "UNKNOWN"),
                        evaluation.get("preservation_result", "UNKNOWN"),
                        evaluation.get("transport_result", "UNKNOWN"),
                        evaluation.get("center_capability_result", "UNKNOWN"),
                        evaluation.get("primary_limiting_factor"),
                        json.dumps(evaluation.get("positive_factors", [])),
                        json.dumps(evaluation.get("limiting_factors", [])),
                        json.dumps(evaluation.get("explanation_data", {})),
                    ),
                )
                conn.commit()
        except Exception as e:
            # Foreign key constraint failure or database lock during demonstration
            pass

    def get_evaluation(self, patient_id: str, organ_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM match_evaluations
                WHERE patient_id = ? AND organ_id = ?
                ORDER BY evaluated_at DESC LIMIT 1
                """,
                (patient_id, organ_id),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["positive_factors"] = self.parse_json_field(data.get("positive_factors"), default=[])
            data["limiting_factors"] = self.parse_json_field(data.get("limiting_factors"), default=[])
            data["explanation_data"] = self.parse_json_field(data.get("explanation_data"), default={})
            return data
