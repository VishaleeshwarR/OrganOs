// TransplantLink TypeScript Types

export interface Patient {
  id: number;
  patient_id: string;
  full_name?: string;
  waiting_time_days?: number;
  age: number;
  sex: string;
  blood_group: string;
  height_cm: number;
  weight_kg: number;
  organ_needed: string;
  listing_status: string;
  urgency_level: string;
  waitlist_date: string;
  transplant_center_id: string;
  transplant_center_name?: string;
  center_city?: string;
  pra_percentage: number;
  previous_transplant: boolean | number;
  created_at: string;
  hla?: {
    a_1: string;
    a_2: string;
    b_1: string;
    b_2: string;
    dr_1: string;
    dr_2: string;
  };
}

export interface Organ {
  id: number;
  organ_id: string;
  donor_id: string;
  organ_type: string;
  side?: string;
  blood_group: string;
  status: string;
  quality_grade: string;
  organ_weight_g?: number;
  length_cm?: number;
  procurement_time: string;
  preservation_start: string;
  preservation_method: string;
  donor_hospital_id: string;
  donor_hospital_name?: string;
  donor_hospital_city?: string;
  donor_latitude?: number;
  donor_longitude?: number;
  donor_age?: number;
  donor_sex?: string;
  donor_weight_kg?: number;
  current_location?: string;
  available_until?: string;
  current_elapsed_hours?: number;
  simulated_remaining_hours?: number;
  preservation_status?: string;
  organ_metrics?: Record<string, any>;
  donor_hla?: {
    a_1: string;
    a_2: string;
    b_1: string;
    b_2: string;
    dr_1: string;
    dr_2: string;
  };
}

export interface Hospital {
  [key: string]: any;
  id: number;
  hospital_id: string;
  name: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  hospital_type: string;
  icu_capacity: number;
  organ_storage: boolean | number;
  hla_lab: boolean | number;
  transplant_programs: string[];
  twenty_four_seven_transplant_team: boolean | number;
  airport_access: string;
  ground_transport: string;
  status: string;
}

export interface TransportRoute {
  transport_id: string;
  origin_hospital_id: string;
  destination_hospital_id: string;
  transport_mode: string;
  distance_km: number;
  estimated_minutes: number;
  availability: string;
  priority_transport: boolean | number;
  airport_required: boolean | number;
  origin_name?: string;
  origin_city?: string;
  destination_name?: string;
  destination_city?: string;
  origin_lat?: number;
  origin_lon?: number;
  destination_lat?: number;
  destination_lon?: number;
}

export interface MatchEvaluation {
  [key: string]: any;
  evaluation_id: string;
  patient_id: string;
  organ_id: string;
  overall_result: string;
  match_level: string;
  classification: string;
  abo_result: string;
  hla_result: string;
  size_result: string;
  organ_quality_result: string;
  preservation_result: string;
  transport_result: string;
  center_capability_result: string;
  primary_limiting_factor?: string;
  positive_factors: string[];
  limiting_factors: string[];
  explanation_data: {
    result: string;
    match_level: string;
    classification: string;
    primary_limiting_factor?: string;
    evidence: {
      recipient_id: string;
      recipient_blood_group: string;
      organ_id: string;
      organ_blood_group: string;
      organ_type: string;
      hla_matched_loci: number;
      hla_total_loci: number;
      hla_classification: string;
      quality_grade: string;
      distance_km: number;
      transport_eta_minutes: number;
      transport_mode: string;
      preservation_elapsed_hours: number;
      preservation_max_window_hours: number;
      projected_remaining_hours: number;
      preservation_status: string;
      donor_center: string;
      recipient_center: string;
    };
  };
  transport?: TransportRoute;
  hla_details?: {
    matched_loci: number;
    total_loci: number;
    classification: string;
    matched_alleles: string[];
    patient_alleles: string[];
    donor_alleles: string[];
  };
}

export interface PotentialMatchesResponse {
  patient_id: string;
  organ_type: string;
  total_organs_considered: number;
  potential_matches: number;
  excluded_candidates: number;
  exclusion_summary: {
    abo_incompatible: number;
    transport_not_feasible: number;
    preservation_constraint: number;
    hla_low_compatibility: number;
    center_capability: number;
    size_constraint: number;
    organ_quality: number;
    other_configured_rules: number;
  };
  matches: MatchEvaluation[];
  exclusions: MatchEvaluation[];
  latency_ms?: number;
}

export interface AuditLogEntry {
  id: string | number;
  timestamp: string;
  action: string;
  tool_called?: string;
  patient_context?: string;
  records_evaluated?: number;
  result_summary?: string;
  latency_ms?: number;
  entity_type?: string;
  entity_id?: string;
  details?: any;
  hash?: string;
  ip_address?: string;
  user_id?: string;
}
