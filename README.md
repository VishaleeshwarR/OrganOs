# TransplantLink — Clinical Decision Support & MCP Transplant Coordination Prototype

> **NOTICE**: Prototype operating on **100% synthetic demonstration data**.  
> *The MCP server retrieves and computes. The AI explains. The frontend visualizes. The clinician makes the decision.*

---

## 1. Overview

**TransplantLink** is a clinical decision-support workstation for organ transplant coordination built on the **Model Context Protocol (MCP)**, **Supabase / PostgreSQL**, a deterministic clinical matching engine, and a **Next.js 15** operations workstation interface.

### Core Architecture

```
                         ┌───────────────────────┐
                         │       Supabase        │
                         │    PostgreSQL DB      │
                         │ (or Embedded Fallback)│
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  TransplantLink MCP   │
                         │       Server          │
                         │                       │
                         │ Tools + Resources     │
                         │ Deterministic Engine  │
                         │ Structured Evidence   │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
             ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
             │ Next.js 15  │  │  AI Agent   │  │   ChatGPT   │
             │ Frontend    │  │ Query       │  │ External    │
             │ Workstation │  │ Reasoner    │  │ MCP Client  │
             └─────────────┘  └─────────────┘  └─────────────┘
```

---

## 2. Key Features

1. **Synthetic Registry**:
   - **500 Patients** with HLA typing (A, B, DR loci), PRA%, urgency tiers, and listing dates.
   - **300 Donors** with comprehensive screening and HLA profiles.
   - **700 Organs** (Kidney, Liver, Heart, Lung, Pancreas) with physiological metrics (eGFR, creatinine, steatosis%, ejection fraction).
   - **80 Transplant Centers** across Indian hubs with ICU capacities, 24/7 teams, and organ programs.
   - **1,950 Transport Corridors** (Road, Air) with realistic distances and ETAs.
   - **2,149 Historical Allocation Events** for longitudinal visual analytics.

2. **Canonical Test Demonstration Scenario**:
   - Recipient: `REC-2026-00421` (47yo Male, O+, Kidney candidate, High urgency, PRA 18%, Center `TXC-IN-TN-042` Bengaluru)
   - Evaluates: **27 candidate organs**
   - Surfaced Matches: **8 potential matches** (3 High, 5 Moderate)
   - Exclusions: **19 excluded** (8 ABO incompatible, 4 transport infeasible, 3 preservation risk, 2 center missing program, 2 size discrepancy)

3. **Match Explanation Inspector ("Why?" and "Why Not?")**:
   - Structured evidence for every decision.
   - Positive clinical factors (ABO match, HLA loci alignment, cold ischemia margin, receiving center authorization).
   - Negative factors (exact reason: e.g. donor A+ to recipient O+, missing transport corridor, cold ischemia limit exceeded).

4. **Visual Analytics (5 Recharts Visualizations)**:
   - Organ Inventory Distribution (by organ type and quality grade)
   - Matching Outcomes Breakdown (potential matches vs exclusion categories)
   - Organ Availability Trend (monthly time-series)
   - Transport Distance vs. Transit ETA (scatter plot demonstrating logistics)
   - Historical Allocation Outcomes (Offers, Accepted, Declined, Expired, Transplanted)

5. **Clinical Registry Query & MCP Activity**:
   - Natural language registry query grounded in real MCP tools.
   - Discreet "Data Sources Consulted" inspection widget showing latency, records evaluated, and tool names.

---

## 3. Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Install Backend Dependencies & Seed Database
```powershell
pip install -r backend/requirements.txt
python -m backend.seed_data --verify
```

### 2. Run Backend & MCP Test Suite
```powershell
python -m backend.test_suite
```

### 3. Start Backend FastAPI Server (Port 8000)
```powershell
python run_backend.py
```

### 4. Start Next.js Frontend (Port 3000)
```powershell
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 4. MCP Tools Reference

| Tool Name | Parameters | Description |
|---|---|---|
| `get_patient` | `patient_id` | Retrieves patient profile, HLA alleles, PRA%, and urgency |
| `search_patients` | `organ_needed, blood_group, urgency_level, ...` | Filters registry candidates |
| `get_waitlist` | — | Retrieves aggregate waitlist summary |
| `search_available_organs`| `organ_type, blood_group, location, ...` | Searches procured organs in preservation |
| `get_organ_details` | `organ_id` | Retrieves organ metrics, preservation countdown, and donor data |
| `get_donor` | `donor_id` | Retrieves donor medical history and HLA profile |
| `get_donor_organs` | `donor_id` | Retrieves organs procured from donor |
| `evaluate_compatibility` | `patient_id, organ_id` | Deterministic 10-factor evaluation of recipient-organ pair |
| `find_potential_matches` | `patient_id, organ_type` | Star tool: Evaluates all candidates and returns categorized exclusions |
| `get_hospital` | `hospital_id` | Retrieves hospital capabilities and authorized programs |
| `find_transplant_centers`| `organ_type, location` | Searches certified transplant centers |
| `find_transport_options` | `organ_id, destination_hospital_id` | Calculates road and air routes, distance, and ETAs |
| `calculate_transport_eta`| `transport_id` | Details route timing projections |
| `get_preservation_status`| `organ_id` | Cold ischemia elapsed and simulated remaining hours |
| `get_registry_statistics`| — | Executive summary metrics of registry state |
| `get_match_statistics` | `patient_id` | Candidate ratios and matching counts for listed patient |

---

## 5. Running MCP Server for External Clients (ChatGPT / Claude / Antigravity)

### Stdio Transport:
```powershell
python -m backend.run_mcp_stdio
```

### FastMCP / SSE Bridge:
The FastAPI server at `http://localhost:8000` exposes MCP tool invocations via `/api/mcp/call` and lists all schemas via `/api/mcp/tools`.

---

## 6. Safety & Clinical Boundaries

> **TransplantLink is a clinical decision-support prototype.**  
> Results are generated from synthetic demonstration data and configured simulation criteria. They do not constitute actual medical advice, clinical allocation determinations, or legal transplant decisions.
