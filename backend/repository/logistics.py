"""
TransplantLink Logistics & Transport Repository
"""

import math
from typing import Dict, List, Optional, Any
from .base import BaseRepository


class LogisticsRepository(BaseRepository):
    def find_transport_options(
        self,
        origin_hospital_id: str,
        destination_hospital_id: str,
    ) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, 
                       ho.name as origin_name, ho.city as origin_city, ho.latitude as origin_lat, ho.longitude as origin_lon,
                       hd.name as destination_name, hd.city as destination_city, hd.latitude as destination_lat, hd.longitude as destination_lon
                FROM transport_options t
                JOIN hospitals ho ON t.origin_hospital_id = ho.hospital_id
                JOIN hospitals hd ON t.destination_hospital_id = hd.hospital_id
                WHERE t.origin_hospital_id = ? AND t.destination_hospital_id = ?
                ORDER BY t.estimated_minutes ASC
                """,
                (origin_hospital_id, destination_hospital_id),
            )
            rows = cursor.fetchall()
            if rows:
                return [dict(r) for r in rows]

            # If no direct pre-seeded route in the table, calculate dynamic geodesic route
            return self._synthesize_route(origin_hospital_id, destination_hospital_id, conn)

    def _synthesize_route(self, origin_id: str, dest_id: str, conn) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospitals WHERE hospital_id = ?", (origin_id,))
        orig = cursor.fetchone()
        cursor.execute("SELECT * FROM hospitals WHERE hospital_id = ?", (dest_id,))
        dest = cursor.fetchone()

        if not orig or not dest:
            return []

        if orig["airport_access"] == "RESTRICTED" or orig["ground_transport"] == "NONE":
            return []

        # Haversine distance in km
        lat1, lon1 = math.radians(orig["latitude"]), math.radians(orig["longitude"])
        lat2, lon2 = math.radians(dest["latitude"]), math.radians(dest["longitude"])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        km = round(6371 * c, 1)

        routes = []
        if km < 350:
            # Road transport viable: average speed 70 km/h + 30 min prep
            eta_mins = int(round((km / 70.0) * 60 + 30))
            routes.append({
                "transport_id": f"TRN-RD-{origin_id[-4:]}-{dest_id[-4:]}",
                "origin_hospital_id": origin_id,
                "destination_hospital_id": dest_id,
                "transport_mode": "DEDICATED_ROAD_AMBULANCE",
                "distance_km": km,
                "estimated_minutes": eta_mins,
                "availability": "AVAILABLE",
                "priority_transport": True,
                "airport_required": False,
                "origin_name": orig["name"],
                "origin_city": orig["city"],
                "origin_lat": orig["latitude"],
                "origin_lon": orig["longitude"],
                "destination_name": dest["name"],
                "destination_city": dest["city"],
                "destination_lat": dest["latitude"],
                "destination_lon": dest["longitude"],
            })

        # Air transport (always possible or for longer distances)
        # Flight avg speed 450 km/h + 90 min airport transfer & handover
        air_eta_mins = int(round((km / 450.0) * 60 + 90))
        routes.append({
            "transport_id": f"TRN-AIR-{origin_id[-4:]}-{dest_id[-4:]}",
            "origin_hospital_id": origin_id,
            "destination_hospital_id": dest_id,
            "transport_mode": "CHARTER_AIR_TRANSFER",
            "distance_km": km,
            "estimated_minutes": air_eta_mins,
            "availability": "AVAILABLE",
            "priority_transport": True,
            "airport_required": True,
            "origin_name": orig["name"],
            "origin_city": orig["city"],
            "origin_lat": orig["latitude"],
            "origin_lon": orig["longitude"],
            "destination_name": dest["name"],
            "destination_city": dest["city"],
            "destination_lat": dest["latitude"],
            "destination_lon": dest["longitude"],
        })

        return sorted(routes, key=lambda r: r["estimated_minutes"])

    def calculate_transport_eta(self, transport_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, ho.name as origin_name, hd.name as destination_name
                FROM transport_options t
                JOIN hospitals ho ON t.origin_hospital_id = ho.hospital_id
                JOIN hospitals hd ON t.destination_hospital_id = hd.hospital_id
                WHERE t.transport_id = ?
                """,
                (transport_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            hours = data["estimated_minutes"] // 60
            minutes = data["estimated_minutes"] % 60
            data["formatted_eta"] = f"{hours}h {minutes:02d}m"
            return data
