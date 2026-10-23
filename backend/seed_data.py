"""
TransplantLink Deterministic Synthetic Registry Seed Generator
Generates realistic, internally consistent synthetic transplant registry data.
Seed: 20260914.
Guarantees canonical scenario for REC-2026-00421: 27 evaluated, 8 matches, 19 excluded.
"""

import os
import sys
import json
import math
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

SEED = 20260914
random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "transplantlink.db"
SEED_SQL_PATH = BASE_DIR.parent / "supabase" / "seed.sql"

# Common HLA Allele pools
HLA_A_ALLELES = ["A1", "A2", "A3", "A11", "A24", "A26", "A29", "A31", "A33", "A68"]
HLA_B_ALLELES = ["B7", "B8", "B15", "B27", "B35", "B40", "B44", "B51", "B52", "B57"]
HLA_DR_ALLELES = ["DR1", "DR3", "DR4", "DR7", "DR9", "DR11", "DR13", "DR15", "DR17"]
BLOOD_GROUPS = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
BG_WEIGHTS = [0.38, 0.04, 0.22, 0.03, 0.26, 0.03, 0.03, 0.01]
ORGAN_TYPES = ["Kidney", "Liver", "Heart", "Lung", "Pancreas"]
URGENCY_LEVELS = ["STATUS_1A", "CRITICAL", "HIGH", "STATUS_1B", "STANDARD"]
URGENCY_WEIGHTS = [0.08, 0.12, 0.30, 0.25, 0.25]

# Top Indian Healthcare and Medical Institution hubs
CITIES_DATA = [
    {"city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
    {"city": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946},
    {"city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777},
    {"city": "Delhi NCR", "state": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"city": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867},
    {"city": "Kochi", "state": "Kerala", "lat": 9.9312, "lon": 76.2673},
    {"city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639},
    {"city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714},
    {"city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567},
    {"city": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0168, "lon": 76.9558},
    {"city": "Chandigarh", "state": "Punjab", "lat": 30.7333, "lon": 76.7794},
    {"city": "Thiruvananthapuram", "state": "Kerala", "lat": 8.5241, "lon": 76.9366},
    {"city": "Bhubaneswar", "state": "Odisha", "lat": 20.2961, "lon": 85.8245},
    {"city": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873},
    {"city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462},
]


def haversine_km(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(6371 * c, 1)


def create_schema(conn):
    schema_path = BASE_DIR.parent / "supabase" / "migrations" / "01_initial_schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Adapt PostgreSQL script for SQLite
    sqlite_sql = sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
    sqlite_sql = sqlite_sql.replace("TIMESTAMP WITH TIME ZONE", "TEXT")
    sqlite_sql = sqlite_sql.replace("DATE", "TEXT")
    sqlite_sql = sqlite_sql.replace("JSONB", "TEXT")
    sqlite_sql = sqlite_sql.replace("'[]'::jsonb", "'[]'")
    sqlite_sql = sqlite_sql.replace("'{}'::jsonb", "'{}'")
    sqlite_sql = sqlite_sql.replace("NUMERIC(5, 1)", "REAL")
    sqlite_sql = sqlite_sql.replace("NUMERIC(9, 6)", "REAL")
    sqlite_sql = sqlite_sql.replace("NUMERIC(6, 1)", "REAL")
    sqlite_sql = sqlite_sql.replace("NUMERIC(4, 1)", "REAL")
    sqlite_sql = sqlite_sql.replace("NUMERIC(7, 1)", "REAL")

    conn.executescript(sqlite_sql)
    conn.commit()


def generate_data():
    if DB_PATH.exists():
        try:
            DB_PATH.unlink()
        except Exception:
            pass

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    cursor = conn.cursor()

    now = datetime(2026, 9, 14, 9, 42, 18)

    print("[1/7] Seeding 75 Hospitals across Indian centers...")
    hospitals = []
    # Canonical recipient hospital
    canonical_hosp = {
        "hospital_id": "TXC-IN-TN-042",
        "name": "Apex Institute of Organ Transplantation",
        "city": "Bengaluru",
        "state": "Karnataka",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "hospital_type": "APEX_TRANSPLANT_INSTITUTE",
        "icu_capacity": 65,
        "organ_storage": 1,
        "hla_lab": 1,
        "transplant_programs": json.dumps(["Kidney", "Liver", "Heart", "Lung", "Pancreas"]),
        "twenty_four_seven_transplant_team": 1,
        "airport_access": "WITHIN_30_MINS",
        "ground_transport": "DEDICATED_AMBULANCE",
        "status": "OPERATIONAL",
    }
    hospitals.append(canonical_hosp)

    # Canonical donor hospital in Chennai (286 km away)
    canonical_donor_hosp = {
        "hospital_id": "HSP-IN-CHN-001",
        "name": "Madras Medical Specialty Hospital",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "hospital_type": "GOVERNMENT_MEDICAL_COLLEGE",
        "icu_capacity": 55,
        "organ_storage": 1,
        "hla_lab": 1,
        "transplant_programs": json.dumps(["Kidney", "Liver", "Heart", "Lung"]),
        "twenty_four_seven_transplant_team": 1,
        "airport_access": "WITHIN_20_MINS",
        "ground_transport": "DEDICATED_AMBULANCE",
        "status": "OPERATIONAL",
    }
    hospitals.append(canonical_donor_hosp)

    hosp_types = ["GOVERNMENT_MEDICAL_COLLEGE", "SUPERSPECIALTY_TRUST", "APEX_TRANSPLANT_INSTITUTE", "PRIVATE_TERTIARY_HOSPITAL"]
    hosp_prefixes = ["City General", "Memorial Specialty", "All-India Institute of", "National Center for", "Metropolitan", "Imperial Care", "Global Lifeline", "Narayana Institute of"]

    for i in range(3, 76):
        city_info = CITIES_DATA[(i - 1) % len(CITIES_DATA)]
        # Add slight jitter to coordinates
        lat = city_info["lat"] + random.uniform(-0.08, 0.08)
        lon = city_info["lon"] + random.uniform(-0.08, 0.08)
        hosp_id = f"HSP-IN-{city_info['city'][:3].upper()}-{i:03d}"
        prefix = random.choice(hosp_prefixes)
        name = f"{prefix} Medical Sciences ({city_info['city']})"
        
        # 85% have Kidney program, others have varied
        programs = ["Kidney"]
        if random.random() < 0.70:
            programs.append("Liver")
        if random.random() < 0.40:
            programs.append("Heart")
        if random.random() < 0.30:
            programs.append("Lung")
        if random.random() < 0.20:
            programs.append("Pancreas")

        hospitals.append({
            "hospital_id": hosp_id,
            "name": name,
            "city": city_info["city"],
            "state": city_info["state"],
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "hospital_type": random.choice(hosp_types),
            "icu_capacity": random.randint(25, 80),
            "organ_storage": 1 if random.random() < 0.95 else 0,
            "hla_lab": 1 if random.random() < 0.90 else 0,
            "transplant_programs": json.dumps(programs),
            "twenty_four_seven_transplant_team": 1 if random.random() < 0.92 else 0,
            "airport_access": "WITHIN_30_MINS" if random.random() < 0.75 else "WITHIN_60_MINS",
            "ground_transport": "DEDICATED_AMBULANCE",
            "status": "OPERATIONAL",
        })

    for h in hospitals:
        cursor.execute(
            """
            INSERT INTO hospitals (hospital_id, name, city, state, latitude, longitude, hospital_type,
                                   icu_capacity, organ_storage, hla_lab, transplant_programs,
                                   twenty_four_seven_transplant_team, airport_access, ground_transport, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                h["hospital_id"], h["name"], h["city"], h["state"], h["latitude"], h["longitude"],
                h["hospital_type"], h["icu_capacity"], h["organ_storage"], h["hla_lab"],
                h["transplant_programs"], h["twenty_four_seven_transplant_team"], h["airport_access"],
                h["ground_transport"], h["status"]
            )
        )
    conn.commit()

    print("[2/7] Generating 1,200+ Transport Routes...")
    transport_routes = []
    # Dedicated canonical road route from Chennai HSP-IN-CHN-001 to Bengaluru TXC-IN-TN-042
    transport_routes.append({
        "transport_id": "TRN-RD-CHN-BLR-01",
        "origin_hospital_id": "HSP-IN-CHN-001",
        "destination_hospital_id": "TXC-IN-TN-042",
        "transport_mode": "DEDICATED_ROAD_AMBULANCE",
        "distance_km": 286.0,
        "estimated_minutes": 195,  # 3h 15m
        "availability": "AVAILABLE",
        "priority_transport": 1,
        "airport_required": 0,
        "departure_time": (now - timedelta(hours=2)).isoformat(),
        "estimated_arrival": (now + timedelta(hours=1, minutes=15)).isoformat(),
    })

    route_set = {("HSP-IN-CHN-001", "TXC-IN-TN-042")}

    # Interconnect hospitals
    for i, orig in enumerate(hospitals):
        # Connect to 15-20 nearest hospitals and 5 major air corridors
        for j, dest in enumerate(hospitals):
            if orig["hospital_id"] == dest["hospital_id"]:
                continue
            if (orig["hospital_id"], dest["hospital_id"]) in route_set:
                continue

            dist = haversine_km(orig["latitude"], orig["longitude"], dest["latitude"], dest["longitude"])
            if dist < 400 or (dist < 1500 and (i < 15 or j < 15)):
                route_id = f"TRN-{len(transport_routes) + 1:05d}"
                if dist < 350:
                    mode = "DEDICATED_ROAD_AMBULANCE"
                    mins = int(round((dist / 70.0) * 60 + 30))
                    airport = 0
                else:
                    mode = "CHARTER_AIR_TRANSFER"
                    mins = int(round((dist / 450.0) * 60 + 90))
                    airport = 1

                transport_routes.append({
                    "transport_id": route_id,
                    "origin_hospital_id": orig["hospital_id"],
                    "destination_hospital_id": dest["hospital_id"],
                    "transport_mode": mode,
                    "distance_km": dist,
                    "estimated_minutes": mins,
                    "availability": "AVAILABLE" if random.random() < 0.95 else "DELAYED",
                    "priority_transport": 1 if random.random() < 0.4 else 0,
                    "airport_required": airport,
                    "departure_time": (now - timedelta(minutes=random.randint(10, 180))).isoformat(),
                    "estimated_arrival": (now + timedelta(minutes=mins)).isoformat(),
                })
                route_set.add((orig["hospital_id"], dest["hospital_id"]))

    for tr in transport_routes:
        cursor.execute(
            """
            INSERT INTO transport_options (transport_id, origin_hospital_id, destination_hospital_id,
                                           transport_mode, distance_km, estimated_minutes, availability,
                                           priority_transport, airport_required, departure_time, estimated_arrival)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tr["transport_id"], tr["origin_hospital_id"], tr["destination_hospital_id"],
                tr["transport_mode"], tr["distance_km"], tr["estimated_minutes"], tr["availability"],
                tr["priority_transport"], tr["airport_required"], tr["departure_time"], tr["estimated_arrival"]
            )
        )
    conn.commit()
    print(f"    Created {len(transport_routes)} transport routes.")

    print("[3/7] Seeding 500 Patients (including canonical test candidate REC-2026-00421)...")
    patients = []
    patient_hlas = []

    # 1. CANONICAL PATIENT
    canonical_pat = {
        "patient_id": "REC-2026-00421",
        "age": 47,
        "sex": "Male",
        "blood_group": "O+",
        "height_cm": 172.0,
        "weight_kg": 68.0,
        "organ_needed": "Kidney",
        "listing_status": "ACTIVE",
        "urgency_level": "HIGH",
        "waitlist_date": "2025-11-18",
        "transplant_center_id": "TXC-IN-TN-042",
        "pra_percentage": 18.0,
        "previous_transplant": 0,
        "created_at": "2025-11-18T09:30:00Z",
    }
    patients.append(canonical_pat)
    patient_hlas.append({
        "patient_id": "REC-2026-00421",
        "hla_a_1": "A2", "hla_a_2": "A3",
        "hla_b_1": "B7", "hla_b_2": "B44",
        "hla_dr_1": "DR4", "hla_dr_2": "DR11",
    })

    # Remaining 499 patients
    for i in range(2, 502):
        if i == 421:
            continue
        pid = f"REC-2026-{i:05d}"
        organ = random.choices(ORGAN_TYPES, weights=[0.50, 0.25, 0.12, 0.08, 0.05])[0]
        bg = random.choices(BLOOD_GROUPS, weights=BG_WEIGHTS)[0]
        urgency = random.choices(URGENCY_LEVELS, weights=URGENCY_WEIGHTS)[0]
        sex = "Male" if random.random() < 0.58 else "Female"
        age = random.randint(18, 72)
        hosp = random.choice(hospitals)["hospital_id"]
        waitlist_days = random.randint(10, 1200)
        wait_date = (now - timedelta(days=waitlist_days)).strftime("%Y-%m-%d")
        pra = round(random.choices([0.0, 5.0, 15.0, 35.0, 75.0], weights=[0.45, 0.25, 0.15, 0.10, 0.05])[0], 1)

        patients.append({
            "patient_id": pid,
            "age": age,
            "sex": sex,
            "blood_group": bg,
            "height_cm": round(random.uniform(150.0, 185.0), 1),
            "weight_kg": round(random.uniform(48.0, 95.0), 1),
            "organ_needed": organ,
            "listing_status": "ACTIVE" if random.random() < 0.90 else random.choice(["SUSPENDED", "MATCHED"]),
            "urgency_level": urgency,
            "waitlist_date": wait_date,
            "transplant_center_id": hosp,
            "pra_percentage": pra,
            "previous_transplant": 1 if random.random() < 0.08 else 0,
            "created_at": (now - timedelta(days=waitlist_days, hours=random.randint(1, 23))).isoformat(),
        })

        patient_hlas.append({
            "patient_id": pid,
            "hla_a_1": random.choice(HLA_A_ALLELES),
            "hla_a_2": random.choice(HLA_A_ALLELES),
            "hla_b_1": random.choice(HLA_B_ALLELES),
            "hla_b_2": random.choice(HLA_B_ALLELES),
            "hla_dr_1": random.choice(HLA_DR_ALLELES),
            "hla_dr_2": random.choice(HLA_DR_ALLELES),
        })

    for p in patients:
        cursor.execute(
            """
            INSERT INTO patients (patient_id, age, sex, blood_group, height_cm, weight_kg,
                                 organ_needed, listing_status, urgency_level, waitlist_date,
                                 transplant_center_id, pra_percentage, previous_transplant, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                p["patient_id"], p["age"], p["sex"], p["blood_group"], p["height_cm"], p["weight_kg"],
                p["organ_needed"], p["listing_status"], p["urgency_level"], p["waitlist_date"],
                p["transplant_center_id"], p["pra_percentage"], p["previous_transplant"], p["created_at"]
            )
        )

    for ph in patient_hlas:
        cursor.execute(
            """
            INSERT INTO patient_hla (patient_id, hla_a_1, hla_a_2, hla_b_1, hla_b_2, hla_dr_1, hla_dr_2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (ph["patient_id"], ph["hla_a_1"], ph["hla_a_2"], ph["hla_b_1"], ph["hla_b_2"], ph["hla_dr_1"], ph["hla_dr_2"])
        )
    conn.commit()

    print("[4/7] Seeding 300 Donors and HLA Profiles...")
    donors = []
    donor_hlas = []

    # Canonical donor 1 (for canonical match ORG-KID-2026-01932 / KID-01932)
    donors.append({
        "donor_id": "DNR-2026-00912",
        "donor_type": "DECEASED_DBD",
        "age": 34,
        "sex": "Male",
        "blood_group": "O+",
        "height_cm": 174.0,
        "weight_kg": 72.0,
        "medical_history": json.dumps({"hypertension": False, "diabetes": False, "smoking": False}),
        "screening_status": "CLEARED",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "donation_date": (now - timedelta(hours=6, minutes=24)).isoformat(),
    })
    donor_hlas.append({
        "donor_id": "DNR-2026-00912",
        "hla_a_1": "A2", "hla_a_2": "A24",
        "hla_b_1": "B7", "hla_b_2": "B35",
        "hla_dr_1": "DR4", "hla_dr_2": "DR15",  # Matches A2, B7, DR4 -> 3 or 4 favorable loci
    })

    # Canonical donor 2 (for canonical excluded ABO organ ORG-KID-2026-01988 / KID-01988)
    donors.append({
        "donor_id": "DNR-2026-00945",
        "donor_type": "DECEASED_DBD",
        "age": 41,
        "sex": "Female",
        "blood_group": "A+",  # Incompatible with O+
        "height_cm": 162.0,
        "weight_kg": 64.0,
        "medical_history": json.dumps({"hypertension": False, "diabetes": False, "smoking": False}),
        "screening_status": "CLEARED",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "donation_date": (now - timedelta(hours=4)).isoformat(),
    })
    donor_hlas.append({
        "donor_id": "DNR-2026-00945",
        "hla_a_1": "A2", "hla_a_2": "A3",
        "hla_b_1": "B7", "hla_b_2": "B44",
        "hla_dr_1": "DR4", "hla_dr_2": "DR11",
    })

    for i in range(3, 301):
        did = f"DNR-2026-{i:05d}"
        bg = random.choices(BLOOD_GROUPS, weights=BG_WEIGHTS)[0]
        age = random.randint(19, 65)
        sex = "Male" if random.random() < 0.62 else "Female"
        hosp = random.choice(hospitals)["hospital_id"]
        hrs_ago = random.randint(3, 48)
        med_hist = {
            "hypertension": random.random() < 0.18,
            "diabetes": random.random() < 0.10,
            "smoking": random.random() < 0.15,
        }

        donors.append({
            "donor_id": did,
            "donor_type": "DECEASED_DBD" if random.random() < 0.85 else "DECEASED_DCD",
            "age": age,
            "sex": sex,
            "blood_group": bg,
            "height_cm": round(random.uniform(152.0, 186.0), 1),
            "weight_kg": round(random.uniform(50.0, 92.0), 1),
            "medical_history": json.dumps(med_hist),
            "screening_status": "CLEARED" if random.random() < 0.96 else "FLAGGED",
            "donor_hospital_id": hosp,
            "donation_date": (now - timedelta(hours=hrs_ago)).isoformat(),
        })

        donor_hlas.append({
            "donor_id": did,
            "hla_a_1": random.choice(HLA_A_ALLELES),
            "hla_a_2": random.choice(HLA_A_ALLELES),
            "hla_b_1": random.choice(HLA_B_ALLELES),
            "hla_b_2": random.choice(HLA_B_ALLELES),
            "hla_dr_1": random.choice(HLA_DR_ALLELES),
            "hla_dr_2": random.choice(HLA_DR_ALLELES),
        })

    for d in donors:
        cursor.execute(
            """
            INSERT INTO donors (donor_id, donor_type, age, sex, blood_group, height_cm, weight_kg,
                               medical_history, screening_status, donor_hospital_id, donation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                d["donor_id"], d["donor_type"], d["age"], d["sex"], d["blood_group"], d["height_cm"],
                d["weight_kg"], d["medical_history"], d["screening_status"], d["donor_hospital_id"], d["donation_date"]
            )
        )

    for dh in donor_hlas:
        cursor.execute(
            """
            INSERT INTO donor_hla (donor_id, hla_a_1, hla_a_2, hla_b_1, hla_b_2, hla_dr_1, hla_dr_2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (dh["donor_id"], dh["hla_a_1"], dh["hla_a_2"], dh["hla_b_1"], dh["hla_b_2"], dh["hla_dr_1"], dh["hla_dr_2"])
        )
    conn.commit()

    print("[5/7] Seeding 700+ Organs & Preservation Events (precisely calibrating 27 Available Kidneys)...")
    organs = []
    preservation_events = []

    # -------------------------------------------------------------
    # PRECISE CALIBRATION OF THE 27 AVAILABLE KIDNEYS FOR REC-2026-00421
    # Canonical recipient: REC-2026-00421 (O+, Kidney, TXC-IN-TN-042 Bengaluru)
    # Required: Exactly 27 evaluated, 8 potential matches, 19 excluded.
    # Matches: 8 (3 HIGH, 5 MODERATE)
    # Exclusions: 19 (ABO incompatible: 8, transport not feasible: 4, preservation constraint: 3, center capability: 2, other/screening/size: 2)
    # -------------------------------------------------------------

    # 8 POTENTIAL MATCHES
    # 1. ORG-KID-2026-01932 (Star match)
    p_start = now - timedelta(hours=6, minutes=24)
    organs.append({
        "organ_id": "ORG-KID-2026-01932",
        "donor_id": "DNR-2026-00912",
        "organ_type": "Kidney",
        "side": "Left",
        "blood_group": "O+",
        "status": "AVAILABLE",
        "quality_grade": "GOOD",
        "organ_weight_g": 182.0,
        "length_cm": 11.4,
        "procurement_time": p_start.isoformat(),
        "preservation_start": p_start.isoformat(),
        "preservation_method": "PULSATILE_MACHINE_PERFUSION",
        "donor_hospital_id": "HSP-IN-CHN-001",
        "current_location": "Chennai",
        "available_until": (p_start + timedelta(hours=30)).isoformat(),
        "organ_metrics": json.dumps({"creatinine": 0.88, "egfr": 96.0, "perfusion_quality": "GOOD", "pump_resistance": 0.28}),
        "created_at": p_start.isoformat(),
        "updated_at": now.isoformat(),
    })
    preservation_events.append({
        "preservation_event_id": "PE-KID-01932",
        "organ_id": "ORG-KID-2026-01932",
        "preservation_method": "PULSATILE_MACHINE_PERFUSION",
        "preservation_start": p_start.isoformat(),
        "current_elapsed_hours": 6.4,
        "simulated_remaining_hours": 23.6,
        "status": "WITHIN_WINDOW",
        "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0, "target_temperature_c": 4.0}),
    })

    # Potential Matches 2 & 3 (HIGH)
    for k_idx, (d_id, elapsed, h_id, rem) in enumerate([
        ("DNR-2026-00003", 5.2, "HSP-IN-CHN-001", 24.8),
        ("DNR-2026-00004", 7.0, "HSP-IN-CHN-001", 23.0),
    ], start=3):
        k_id = f"ORG-KID-2026-0193{k_idx}"
        p_time = now - timedelta(hours=elapsed)
        # Ensure donor is O+ and HLA favorable
        cursor.execute("UPDATE donors SET blood_group = 'O+', donor_hospital_id = ? WHERE donor_id = ?", (h_id, d_id))
        cursor.execute("UPDATE donor_hla SET hla_a_1='A2', hla_a_2='A3', hla_b_1='B7', hla_b_2='B40', hla_dr_1='DR4', hla_dr_2='DR7' WHERE donor_id = ?", (d_id,))
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": "Right",
            "blood_group": "O+",
            "status": "AVAILABLE",
            "quality_grade": "GOOD",
            "organ_weight_g": 178.0,
            "length_cm": 11.2,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": h_id,
            "current_location": "Chennai",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 0.92, "egfr": 92.0, "perfusion_quality": "GOOD"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": elapsed,
            "simulated_remaining_hours": rem,
            "status": "WITHIN_WINDOW",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # Potential Matches 4 to 8 (MODERATE)
    for m_idx, (d_id, elapsed, h_id, rem, side) in enumerate([
        ("DNR-2026-00005", 8.5, "HSP-IN-CHN-001", 21.5, "Left"),
        ("DNR-2026-00006", 11.2, "HSP-IN-CHN-001", 18.8, "Right"),
        ("DNR-2026-00007", 9.0, "HSP-IN-CHN-001", 21.0, "Left"),
        ("DNR-2026-00008", 12.0, "HSP-IN-CHN-001", 18.0, "Right"),
        ("DNR-2026-00009", 10.4, "HSP-IN-CHN-001", 19.6, "Left"),
    ], start=1):
        k_id = f"ORG-KID-2026-0194{m_idx}"
        p_time = now - timedelta(hours=elapsed)
        cursor.execute("UPDATE donors SET blood_group = 'O+', donor_hospital_id = ? WHERE donor_id = ?", (h_id, d_id))
        cursor.execute("UPDATE donor_hla SET hla_a_1='A2', hla_a_2='A24', hla_b_1='B15', hla_b_2='B44', hla_dr_1='DR1', hla_dr_2='DR15' WHERE donor_id = ?", (d_id,))
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": side,
            "blood_group": "O+",
            "status": "AVAILABLE",
            "quality_grade": "GOOD",
            "organ_weight_g": 185.0,
            "length_cm": 11.5,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": h_id,
            "current_location": "Chennai",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 1.05, "egfr": 84.0, "perfusion_quality": "GOOD"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": elapsed,
            "simulated_remaining_hours": rem,
            "status": "WITHIN_WINDOW",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # 19 EXCLUDED CANDIDATES
    # Group A: 8 ABO INCOMPATIBLE (including canonical ORG-KID-2026-01988)
    for abo_idx in range(1, 9):
        k_id = "ORG-KID-2026-01988" if abo_idx == 1 else f"ORG-KID-2026-0180{abo_idx}"
        d_id = "DNR-2026-00945" if abo_idx == 1 else f"DNR-2026-0001{abo_idx}"
        bg = "A+" if abo_idx % 2 == 1 else "B+"
        p_time = now - timedelta(hours=4 + abo_idx)
        cursor.execute("UPDATE donors SET blood_group = ?, donor_hospital_id = 'HSP-IN-CHN-001' WHERE donor_id = ?", (bg, d_id))
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": "Right" if abo_idx % 2 == 0 else "Left",
            "blood_group": bg,
            "status": "AVAILABLE",
            "quality_grade": "GOOD",
            "organ_weight_g": 175.0,
            "length_cm": 11.0,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": "HSP-IN-CHN-001",
            "current_location": "Chennai",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 0.95, "egfr": 90.0, "perfusion_quality": "GOOD"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": 4.0 + abo_idx,
            "simulated_remaining_hours": 26.0 - abo_idx,
            "status": "WITHIN_WINDOW",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # Group B: 4 TRANSPORT NOT FEASIBLE (Far remote centers, e.g. Guwahati/Srinagar with no connecting transport)
    for tr_idx in range(1, 5):
        k_id = f"ORG-KID-2026-0182{tr_idx}"
        d_id = f"DNR-2026-0002{tr_idx}"
        # Remote hospital ID with no active route to TXC-IN-TN-042
        remote_hosp = f"HSP-IN-REM-90{tr_idx}"
        cursor.execute(
            """
            INSERT OR IGNORE INTO hospitals (hospital_id, name, city, state, latitude, longitude,
                                            hospital_type, icu_capacity, organ_storage, hla_lab,
                                            transplant_programs, twenty_four_seven_transplant_team,
                                            airport_access, ground_transport, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                remote_hosp, f"Remote Island Medical Center {tr_idx}", "Port Blair", "Andaman", 11.6234, 92.7265,
                "GOVERNMENT_MEDICAL_COLLEGE", 30, 1, 1, json.dumps(["Kidney"]), 1, "RESTRICTED", "NONE", "OPERATIONAL"
            )
        )
        cursor.execute("UPDATE donors SET blood_group = 'O+', donor_hospital_id = ? WHERE donor_id = ?", (remote_hosp, d_id))
        p_time = now - timedelta(hours=5)
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": "Left",
            "blood_group": "O+",
            "status": "AVAILABLE",
            "quality_grade": "GOOD",
            "organ_weight_g": 180.0,
            "length_cm": 11.3,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": remote_hosp,
            "current_location": "Port Blair",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 0.89, "egfr": 94.0, "perfusion_quality": "GOOD"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": 5.0,
            "simulated_remaining_hours": 25.0,
            "status": "WITHIN_WINDOW",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # Group C: 3 PRESERVATION CONSTRAINT (Elapsed cold ischemia >= 28.5 hours + transit will exceed 30h limit)
    for pr_idx, elapsed in enumerate([28.6, 29.2, 29.8], start=1):
        k_id = f"ORG-KID-2026-0183{pr_idx}"
        d_id = f"DNR-2026-0003{pr_idx}"
        p_time = now - timedelta(hours=elapsed)
        cursor.execute("UPDATE donors SET blood_group = 'O+', donor_hospital_id = 'HSP-IN-CHN-001' WHERE donor_id = ?", (d_id,))
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": "Right",
            "blood_group": "O+",
            "status": "AVAILABLE",
            "quality_grade": "FAIR",
            "organ_weight_g": 170.0,
            "length_cm": 10.8,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": "HSP-IN-CHN-001",
            "current_location": "Chennai",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 1.35, "egfr": 68.0, "perfusion_quality": "FAIR"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": elapsed,
            "simulated_remaining_hours": round(30.0 - elapsed, 1),
            "status": "CRITICAL",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # Group D: 2 CENTER CAPABILITY / SPECIALIZED (Configured test center lacks program)
    for cc_idx in range(1, 3):
        k_id = f"ORG-KID-2026-0184{cc_idx}"
        d_id = f"DNR-2026-0004{cc_idx}"
        p_time = now - timedelta(hours=6)
        cursor.execute("UPDATE donors SET blood_group = 'O+', donor_hospital_id = 'HSP-IN-CHN-001' WHERE donor_id = ?", (d_id,))
        # Recipient center program check: Let's test a scenario where the receiving hospital program is mismatched or status changed
        # We can also simulate special exclusion rule
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": "Left",
            "blood_group": "O+",
            "status": "AVAILABLE",
            "quality_grade": "GOOD",
            "organ_weight_g": 180.0,
            "length_cm": 11.2,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": "HSP-IN-CHN-001",
            "current_location": "Chennai",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 0.90, "egfr": 95.0, "perfusion_quality": "GOOD"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": 6.0,
            "simulated_remaining_hours": 24.0,
            "status": "WITHIN_WINDOW",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # Group E: 2 OTHER CONFIG RULES (Size discrepancy: donor body weight 128kg or 34kg vs 68kg recipient -> ratio > 1.6 or < 0.6)
    for sz_idx, d_wt in enumerate([130.0, 36.0], start=1):
        k_id = f"ORG-KID-2026-0185{sz_idx}"
        d_id = f"DNR-2026-0005{sz_idx}"
        p_time = now - timedelta(hours=7)
        cursor.execute("UPDATE donors SET blood_group = 'O+', weight_kg = ?, donor_hospital_id = 'HSP-IN-CHN-001' WHERE donor_id = ?", (d_wt, d_id))
        organs.append({
            "organ_id": k_id,
            "donor_id": d_id,
            "organ_type": "Kidney",
            "side": "Right",
            "blood_group": "O+",
            "status": "AVAILABLE",
            "quality_grade": "GOOD",
            "organ_weight_g": 240.0 if d_wt > 100 else 95.0,
            "length_cm": 13.5 if d_wt > 100 else 8.2,
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": "STATIC_COLD_STORAGE",
            "donor_hospital_id": "HSP-IN-CHN-001",
            "current_location": "Chennai",
            "available_until": (p_time + timedelta(hours=30)).isoformat(),
            "organ_metrics": json.dumps({"creatinine": 1.02, "egfr": 88.0, "perfusion_quality": "GOOD"}),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })
        preservation_events.append({
            "preservation_event_id": f"PE-{k_id}",
            "organ_id": k_id,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": 7.0,
            "simulated_remaining_hours": 23.0,
            "status": "WITHIN_WINDOW",
            "simulation_parameters": json.dumps({"cold_ischemia_limit": 30.0}),
        })

    # Now handle the 2 center capability organs: point donor hospital to one where receiving center lacks program or vice versa
    # Let's create an exclusive center that does not allow inter-state Kidney allocation without local program clearance
    no_kidney_center = "HSP-IN-DEL-NOKID"
    cursor.execute(
        """
        INSERT OR IGNORE INTO hospitals (hospital_id, name, city, state, latitude, longitude,
                                        hospital_type, icu_capacity, organ_storage, hla_lab,
                                        transplant_programs, twenty_four_seven_transplant_team,
                                        airport_access, ground_transport, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            no_kidney_center, "North Specialty Heart & Lung Institute", "Delhi", "Delhi", 28.6139, 77.2090,
            "APEX_TRANSPLANT_INSTITUTE", 40, 1, 1, json.dumps(["Heart", "Lung"]), 1, "WITHIN_30_MINS", "DEDICATED_AMBULANCE", "OPERATIONAL"
        )
    )
    # The 2 center-capability organs point to no_kidney_center or have donor hospital program restrictions
    organs[23]["donor_hospital_id"] = no_kidney_center
    organs[24]["donor_hospital_id"] = no_kidney_center

    # -------------------------------------------------------------
    # REMAINING ~673 ORGANS (Liver, Heart, Lung, Pancreas, other kidneys)
    # -------------------------------------------------------------
    total_target = 700
    current_count = len(organs)
    organ_types_non_can = ["Liver", "Heart", "Lung", "Pancreas", "Kidney"]

    for i in range(current_count + 1, total_target + 1):
        otype = random.choices(organ_types_non_can, weights=[0.32, 0.16, 0.18, 0.10, 0.24])[0]
        if otype == "Kidney":
            status = random.choice(["TRANSPLANTED", "ALLOCATED", "EXPIRED"])
        else:
            status = "AVAILABLE" if (i <= 160 or random.random() < 0.30) else random.choice(["TRANSPLANTED", "ALLOCATED", "EXPIRED"])
        d_idx = random.randint(30, len(donors) - 1)
        donor = donors[d_idx]
        bg = donor["blood_group"]
        hosp = donor["donor_hospital_id"]
        hrs_ago = random.randint(1, 48)
        p_time = now - timedelta(hours=hrs_ago)
        max_h = 30.0 if otype == "Kidney" else 14.0 if otype == "Liver" else 5.0 if otype == "Heart" else 7.0 if otype == "Lung" else 15.0
        rem_h = max(0.0, round(max_h - hrs_ago, 1))

        if rem_h <= 0:
            pe_status = "EXPIRED"
        elif rem_h <= 2.0:
            pe_status = "CRITICAL"
        elif rem_h <= 4.0:
            pe_status = "APPROACHING_LIMIT"
        else:
            pe_status = "WITHIN_WINDOW"

        # Organ specific metrics
        if otype == "Kidney":
            metrics = {"creatinine": round(random.uniform(0.7, 1.8), 2), "egfr": round(random.uniform(55, 110), 1), "perfusion_quality": "GOOD" if random.random() < 0.8 else "FAIR"}
        elif otype == "Liver":
            metrics = {"ast": random.randint(18, 55), "alt": random.randint(15, 60), "bilirubin": round(random.uniform(0.5, 1.6), 1), "steatosis_percent": random.randint(2, 18)}
        elif otype == "Heart":
            metrics = {"ejection_fraction": random.randint(52, 68), "echo_quality": "GOOD" if random.random() < 0.85 else "FAIR", "inotropic_support": "MINIMAL"}
        elif otype == "Lung":
            metrics = {"pao2_fio2_ratio": random.randint(320, 480), "compliance": round(random.uniform(40, 65), 1), "imaging_quality": "CLEAR"}
        else:
            metrics = {"amylase": random.randint(30, 95), "lipase": random.randint(20, 80), "organ_quality": "FAVORABLE"}

        oid = f"ORG-{otype[:3].upper()}-2026-{i:05d}"
        organs.append({
            "organ_id": oid,
            "donor_id": donor["donor_id"],
            "organ_type": otype,
            "side": random.choice(["Left", "Right"]) if otype in ["Kidney", "Lung"] else None,
            "blood_group": bg,
            "status": status,
            "quality_grade": random.choices(["GOOD", "FAIR", "MARGINAL"], weights=[0.70, 0.22, 0.08])[0],
            "organ_weight_g": round(random.uniform(140.0, 1600.0), 1),
            "length_cm": round(random.uniform(9.0, 24.0), 1),
            "procurement_time": p_time.isoformat(),
            "preservation_start": p_time.isoformat(),
            "preservation_method": random.choice(["STATIC_COLD_STORAGE", "PULSATILE_MACHINE_PERFUSION", "NORMOTHERMIC_MACHINE_PERFUSION"]),
            "donor_hospital_id": hosp,
            "current_location": "Transit / Facility",
            "available_until": (p_time + timedelta(hours=max_h)).isoformat(),
            "organ_metrics": json.dumps(metrics),
            "created_at": p_time.isoformat(),
            "updated_at": now.isoformat(),
        })

        preservation_events.append({
            "preservation_event_id": f"PE-{oid}",
            "organ_id": oid,
            "preservation_method": "STATIC_COLD_STORAGE",
            "preservation_start": p_time.isoformat(),
            "current_elapsed_hours": float(hrs_ago),
            "simulated_remaining_hours": rem_h,
            "status": pe_status,
            "simulation_parameters": json.dumps({"cold_ischemia_limit": max_h}),
        })

    from collections import Counter
    counts = Counter(o["organ_id"] for o in organs)
    dups = [k for k, v in counts.items() if v > 1]
    if dups:
        print("[DEBUG] DUPLICATE ORGANS DETECTED:", dups)

    for o in organs:
        cursor.execute(
            """
            INSERT INTO organs (organ_id, donor_id, organ_type, side, blood_group, status, quality_grade,
                               organ_weight_g, length_cm, procurement_time, preservation_start, preservation_method,
                               donor_hospital_id, current_location, available_until, organ_metrics, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                o["organ_id"], o["donor_id"], o["organ_type"], o["side"], o["blood_group"], o["status"],
                o["quality_grade"], o["organ_weight_g"], o["length_cm"], o["procurement_time"],
                o["preservation_start"], o["preservation_method"], o["donor_hospital_id"], o["current_location"],
                o["available_until"], o["organ_metrics"], o["created_at"], o["updated_at"]
            )
        )

    for pe in preservation_events:
        cursor.execute(
            """
            INSERT INTO preservation_events (preservation_event_id, organ_id, preservation_method,
                                            preservation_start, current_elapsed_hours, simulated_remaining_hours,
                                            status, simulation_parameters)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pe["preservation_event_id"], pe["organ_id"], pe["preservation_method"], pe["preservation_start"],
                pe["current_elapsed_hours"], pe["simulated_remaining_hours"], pe["status"], pe["simulation_parameters"]
            )
        )
    conn.commit()
    print(f"    Created {len(organs)} organs and preservation records.")

    print("[6/7] Generating 2,000+ Historical Allocation Events...")
    allocation_events = []
    event_types = ["OFFERED", "ACCEPTED", "DECLINED", "EXPIRED", "TRANSFERRED", "TRANSPLANTED"]
    event_weights = [0.35, 0.22, 0.20, 0.05, 0.08, 0.10]
    outcomes = ["COMPLETED", "PROCEEDING", "ORGAN_UNSUITABLE", "TRANSIT_DELAY", "RECIPIENT_UNWELL"]

    for i in range(1, 2150):
        ev_type = random.choices(event_types, weights=event_weights)[0]
        days_back = random.randint(1, 180)
        ev_time = (now - timedelta(days=days_back, hours=random.randint(1, 23), minutes=random.randint(1, 59))).isoformat()
        p = random.choice(patients)
        o = random.choice(organs)
        dist = round(random.uniform(15.0, 1200.0), 1)

        allocation_events.append({
            "event_id": f"ALLOC-EV-{i:06d}",
            "organ_id": o["organ_id"],
            "patient_id": p["patient_id"],
            "event_type": ev_type,
            "event_timestamp": ev_time,
            "reason": "Routine clinical allocation protocol match" if ev_type in ["OFFERED", "ACCEPTED", "TRANSPLANTED"] else "Simulated donor-recipient immunological variance",
            "distance_km": dist,
            "compatibility_category": "FAVORABLE" if ev_type in ["ACCEPTED", "TRANSPLANTED"] else "UNFAVORABLE",
            "transport_status": "COMPLETED" if ev_type == "TRANSPLANTED" else "IN_TRANSIT" if ev_type == "TRANSFERRED" else "SCHEDULED",
            "outcome": random.choice(outcomes),
        })

    for ae in allocation_events:
        cursor.execute(
            """
            INSERT INTO allocation_events (event_id, organ_id, patient_id, event_type, event_timestamp,
                                          reason, distance_km, compatibility_category, transport_status, outcome)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ae["event_id"], ae["organ_id"], ae["patient_id"], ae["event_type"], ae["event_timestamp"],
                ae["reason"], ae["distance_km"], ae["compatibility_category"], ae["transport_status"], ae["outcome"]
            )
        )
    conn.commit()
    print(f"    Created {len(allocation_events)} historical allocation events.")

    # Dump SQL seed script for Supabase
    print("[7/7] Generating Supabase seed.sql script...")
    export_to_sql_file(conn, SEED_SQL_PATH)
    conn.close()
    print("Database seeding completed successfully.")


def export_to_sql_file(conn, target_path: Path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("-- TransplantLink Synthetic Registry Supabase Seed File\n")
        f.write("-- Notice: 100% Synthetic demonstration data.\n\n")
        # Dump inserts
        for line in conn.iterdump():
            if line.startswith("INSERT INTO"):
                f.write(line + "\n")
    print(f"Exported Supabase SQL seed to {target_path}")


def verify_database():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as c FROM patients")
    pat_count = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM donors")
    dnr_count = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM organs")
    org_count = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM hospitals")
    hosp_count = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM transport_options")
    trn_count = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM allocation_events")
    alloc_count = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM organs WHERE organ_type = 'Kidney' AND status = 'AVAILABLE'")
    avail_kidneys = cursor.fetchone()["c"]

    print("==================================================")
    print("TRANSPLANTLINK SYNTHETIC REGISTRY VERIFICATION")
    print("==================================================")
    print(f"Patients count:            {pat_count} (Expected: 500)")
    print(f"Donors count:              {dnr_count} (Expected: 300)")
    print(f"Organs count:              {org_count} (Expected: 700+)")
    print(f"Hospitals count:           {hosp_count} (Expected: 75+)")
    print(f"Transport routes count:    {trn_count} (Expected: 1,200+)")
    print(f"Allocation events count:   {alloc_count} (Expected: 2,000+)")
    print(f"Available Kidneys:         {avail_kidneys} (Expected: 27)")
    print("==================================================")

    # Test canonical matching engine evaluation
    from backend.repository.patients import PatientRepository
    from backend.repository.organs import OrganRepository
    from backend.repository.hospitals import HospitalRepository
    from backend.repository.logistics import LogisticsRepository
    from backend.matching_engine import MatchingEngine

    pat_repo = PatientRepository()
    org_repo = OrganRepository()
    hosp_repo = HospitalRepository()
    log_repo = LogisticsRepository()
    engine = MatchingEngine(hosp_repo, log_repo)

    rec = pat_repo.get_patient("REC-2026-00421")
    assert rec is not None, "Canonical patient REC-2026-00421 not found!"

    candidate_organs = org_repo.search_available_organs(organ_type="Kidney")
    eval_res = engine.find_potential_matches(rec, candidate_organs)

    print(f"Matching Evaluation for REC-2026-00421 (Kidney):")
    print(f"  Total Considered:    {eval_res['total_organs_considered']} (Expected: 27)")
    print(f"  Potential Matches:   {eval_res['potential_matches']} (Expected: 8)")
    print(f"  Excluded Candidates: {eval_res['excluded_candidates']} (Expected: 19)")
    print(f"  Exclusion Summary:   {json.dumps(eval_res['exclusion_summary'], indent=2)}")
    print("==================================================")

    conn.close()
    return eval_res


if __name__ == "__main__":
    generate_data()
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_database()
