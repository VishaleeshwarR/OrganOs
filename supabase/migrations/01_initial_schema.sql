-- TransplantLink Supabase PostgreSQL Schema Migration
-- Notice: Prototype using entirely synthetic demonstration data.

-- 1. Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    sex VARCHAR(10) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    height_cm NUMERIC(5, 1) NOT NULL,
    weight_kg NUMERIC(5, 1) NOT NULL,
    organ_needed VARCHAR(50) NOT NULL,
    listing_status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    urgency_level VARCHAR(50) NOT NULL DEFAULT 'STANDARD',
    waitlist_date DATE NOT NULL,
    transplant_center_id VARCHAR(50) NOT NULL,
    pra_percentage NUMERIC(4, 1) NOT NULL DEFAULT 0.0,
    previous_transplant BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_patients_organ_needed ON patients(organ_needed);
CREATE INDEX IF NOT EXISTS idx_patients_blood_group ON patients(blood_group);
CREATE INDEX IF NOT EXISTS idx_patients_listing_status ON patients(listing_status);

-- 2. Patient HLA Table
CREATE TABLE IF NOT EXISTS patient_hla (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    hla_a_1 VARCHAR(20) NOT NULL,
    hla_a_2 VARCHAR(20) NOT NULL,
    hla_b_1 VARCHAR(20) NOT NULL,
    hla_b_2 VARCHAR(20) NOT NULL,
    hla_dr_1 VARCHAR(20) NOT NULL,
    hla_dr_2 VARCHAR(20) NOT NULL
);

-- 3. Hospitals Table
CREATE TABLE IF NOT EXISTS hospitals (
    id SERIAL PRIMARY KEY,
    hospital_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,
    hospital_type VARCHAR(100) NOT NULL DEFAULT 'GOVERNMENT_MEDICAL_COLLEGE',
    icu_capacity INTEGER NOT NULL DEFAULT 40,
    organ_storage BOOLEAN NOT NULL DEFAULT TRUE,
    hla_lab BOOLEAN NOT NULL DEFAULT TRUE,
    transplant_programs JSONB NOT NULL DEFAULT '[]'::jsonb,
    twenty_four_seven_transplant_team BOOLEAN NOT NULL DEFAULT TRUE,
    airport_access VARCHAR(50) NOT NULL DEFAULT 'WITHIN_30_MINS',
    ground_transport VARCHAR(50) NOT NULL DEFAULT 'DEDICATED_AMBULANCE',
    status VARCHAR(50) NOT NULL DEFAULT 'OPERATIONAL'
);

CREATE INDEX IF NOT EXISTS idx_hospitals_city ON hospitals(city);

-- 4. Donors Table
CREATE TABLE IF NOT EXISTS donors (
    id SERIAL PRIMARY KEY,
    donor_id VARCHAR(50) UNIQUE NOT NULL,
    donor_type VARCHAR(50) NOT NULL DEFAULT 'DECEASED_DBD',
    age INTEGER NOT NULL,
    sex VARCHAR(10) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    height_cm NUMERIC(5, 1) NOT NULL,
    weight_kg NUMERIC(5, 1) NOT NULL,
    medical_history JSONB NOT NULL DEFAULT '{}'::jsonb,
    screening_status VARCHAR(50) NOT NULL DEFAULT 'CLEARED',
    donor_hospital_id VARCHAR(50) NOT NULL REFERENCES hospitals(hospital_id),
    donation_date TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_donors_blood_group ON donors(blood_group);

-- 5. Donor HLA Table
CREATE TABLE IF NOT EXISTS donor_hla (
    id SERIAL PRIMARY KEY,
    donor_id VARCHAR(50) UNIQUE NOT NULL REFERENCES donors(donor_id) ON DELETE CASCADE,
    hla_a_1 VARCHAR(20) NOT NULL,
    hla_a_2 VARCHAR(20) NOT NULL,
    hla_b_1 VARCHAR(20) NOT NULL,
    hla_b_2 VARCHAR(20) NOT NULL,
    hla_dr_1 VARCHAR(20) NOT NULL,
    hla_dr_2 VARCHAR(20) NOT NULL
);

-- 6. Organs Table
CREATE TABLE IF NOT EXISTS organs (
    id SERIAL PRIMARY KEY,
    organ_id VARCHAR(50) UNIQUE NOT NULL,
    donor_id VARCHAR(50) NOT NULL REFERENCES donors(donor_id) ON DELETE CASCADE,
    organ_type VARCHAR(50) NOT NULL,
    side VARCHAR(20),
    blood_group VARCHAR(10) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE',
    quality_grade VARCHAR(20) NOT NULL DEFAULT 'GOOD',
    organ_weight_g NUMERIC(6, 1),
    length_cm NUMERIC(4, 1),
    procurement_time TIMESTAMP WITH TIME ZONE NOT NULL,
    preservation_start TIMESTAMP WITH TIME ZONE NOT NULL,
    preservation_method VARCHAR(100) NOT NULL DEFAULT 'STATIC_COLD_STORAGE',
    donor_hospital_id VARCHAR(50) NOT NULL REFERENCES hospitals(hospital_id),
    current_location VARCHAR(100) NOT NULL,
    available_until TIMESTAMP WITH TIME ZONE NOT NULL,
    organ_metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_organs_type_status ON organs(organ_type, status);
CREATE INDEX IF NOT EXISTS idx_organs_blood_group ON organs(blood_group);

-- 7. Transport Options Table
CREATE TABLE IF NOT EXISTS transport_options (
    id SERIAL PRIMARY KEY,
    transport_id VARCHAR(50) UNIQUE NOT NULL,
    origin_hospital_id VARCHAR(50) NOT NULL REFERENCES hospitals(hospital_id),
    destination_hospital_id VARCHAR(50) NOT NULL REFERENCES hospitals(hospital_id),
    transport_mode VARCHAR(50) NOT NULL,
    distance_km NUMERIC(7, 1) NOT NULL,
    estimated_minutes INTEGER NOT NULL,
    availability VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE',
    priority_transport BOOLEAN NOT NULL DEFAULT FALSE,
    airport_required BOOLEAN NOT NULL DEFAULT FALSE,
    departure_time TIMESTAMP WITH TIME ZONE,
    estimated_arrival TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_transport_origin_dest ON transport_options(origin_hospital_id, destination_hospital_id);

-- 8. Preservation Events Table
CREATE TABLE IF NOT EXISTS preservation_events (
    id SERIAL PRIMARY KEY,
    preservation_event_id VARCHAR(50) UNIQUE NOT NULL,
    organ_id VARCHAR(50) NOT NULL REFERENCES organs(organ_id) ON DELETE CASCADE,
    preservation_method VARCHAR(100) NOT NULL,
    preservation_start TIMESTAMP WITH TIME ZONE NOT NULL,
    current_elapsed_hours NUMERIC(4, 1) NOT NULL,
    simulated_remaining_hours NUMERIC(4, 1) NOT NULL,
    status VARCHAR(50) NOT NULL,
    simulation_parameters JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_preservation_organ ON preservation_events(organ_id);

-- 9. Match Evaluations Table
CREATE TABLE IF NOT EXISTS match_evaluations (
    id SERIAL PRIMARY KEY,
    evaluation_id VARCHAR(50) UNIQUE NOT NULL,
    patient_id VARCHAR(50) NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    organ_id VARCHAR(50) NOT NULL REFERENCES organs(organ_id) ON DELETE CASCADE,
    overall_result VARCHAR(50) NOT NULL,
    abo_result VARCHAR(50) NOT NULL,
    hla_result VARCHAR(50) NOT NULL,
    size_result VARCHAR(50) NOT NULL,
    organ_quality_result VARCHAR(50) NOT NULL,
    preservation_result VARCHAR(50) NOT NULL,
    transport_result VARCHAR(50) NOT NULL,
    center_capability_result VARCHAR(50) NOT NULL,
    primary_limiting_factor VARCHAR(100),
    positive_factors JSONB NOT NULL DEFAULT '[]'::jsonb,
    limiting_factors JSONB NOT NULL DEFAULT '[]'::jsonb,
    explanation_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_eval_patient_organ ON match_evaluations(patient_id, organ_id);

-- 10. Allocation Events Table (Historical & Audit)
CREATE TABLE IF NOT EXISTS allocation_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE NOT NULL,
    organ_id VARCHAR(50) NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    reason TEXT,
    distance_km NUMERIC(7, 1),
    compatibility_category VARCHAR(50),
    transport_status VARCHAR(50),
    outcome VARCHAR(50) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_allocation_events_type ON allocation_events(event_type);
CREATE INDEX IF NOT EXISTS idx_allocation_events_timestamp ON allocation_events(event_timestamp);
