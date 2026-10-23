"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

export interface ActiveCase {
  patientId: string;
  patientName: string;
  patientAge: number;
  patientSex: string;
  patientBloodGroup: string;
  patientAcuity: string;
  patientWaitDays: number;
  patientSupport: string;
  patientHospital: string;
  organNeeded: string;
  cPRA: number;
  organId: string;
  organType: string;
  donorId: string;
  donorAge: number;
  donorSex: string;
  donorBloodGroup: string;
  donorHospital: string;
  donorCity: string;
  perfusionRig: string;
  perfusionTemp: string;
  coronaryFlow: string;
  aorticPressure: string;
  lactate: string;
  flightCarrier: string;
  flightEtaMin: number;
  citRemaining: string;
  matchScore: number;
  mandatoryGatesPassed: number;
}

export const PRESET_CASES: Record<string, ActiveCase> = {
  "REC-2026-00421": {
    patientId: "REC-2026-00421",
    patientName: "Robert Vance",
    patientAge: 54,
    patientSex: "M",
    patientBloodGroup: "O Rh+",
    patientAcuity: "Status 1A (Impella 5.5)",
    patientWaitDays: 428,
    patientSupport: "Impella 5.5 (4.2 L/min), Milrinone 0.375 mcg/kg/min",
    patientHospital: "UCSF Medical Center, CCU Bed 14-B",
    organNeeded: "Thoracic Heart",
    cPRA: 78,
    organId: "SYN-ORG-9921",
    organType: "Thoracic Heart",
    donorId: "D-4081",
    donorAge: 28,
    donorSex: "M",
    donorBloodGroup: "O Rh+",
    donorHospital: "Harborview Medical Center",
    donorCity: "Seattle, WA (BFI Airport)",
    perfusionRig: "TransMedics OCS Heart #02 (Pulsatile)",
    perfusionTemp: "4.2 °C",
    coronaryFlow: "1.10 L/min",
    aorticPressure: "82 mmHg",
    lactate: "2.1 mmol/L (Downward Trend)",
    flightCarrier: "MEDEVAC 921TX (Learjet 45 @ FL240)",
    flightEtaMin: 18,
    citRemaining: "02:41:18",
    matchScore: 94.2,
    mandatoryGatesPassed: 4,
  },
  "REC-2026-00109": {
    patientId: "REC-2026-00109",
    patientName: "Elena Rostova",
    patientAge: 46,
    patientSex: "F",
    patientBloodGroup: "O Rh+",
    patientAcuity: "Status 1B (ICU Intubated)",
    patientWaitDays: 312,
    patientSupport: "Vasoactive inotropes, Intubated",
    patientHospital: "Stanford Health Care, ICU Room 4",
    organNeeded: "Thoracic Heart",
    cPRA: 12,
    organId: "SYN-ORG-9921",
    organType: "Thoracic Heart",
    donorId: "D-4081",
    donorAge: 28,
    donorSex: "M",
    donorBloodGroup: "O Rh+",
    donorHospital: "Harborview Medical Center",
    donorCity: "Seattle, WA (BFI Airport)",
    perfusionRig: "TransMedics OCS Heart #02",
    perfusionTemp: "4.2 °C",
    coronaryFlow: "1.10 L/min",
    aorticPressure: "82 mmHg",
    lactate: "2.1 mmol/L",
    flightCarrier: "MEDEVAC 921TX",
    flightEtaMin: 22,
    citRemaining: "02:41:18",
    matchScore: 88.5,
    mandatoryGatesPassed: 4,
  },
  "REC-2026-00388": {
    patientId: "REC-2026-00388",
    patientName: "Marcus Chen",
    patientAge: 61,
    patientSex: "M",
    patientBloodGroup: "B Rh+",
    patientAcuity: "Status 2 (Hemodialysis 3x/wk)",
    patientWaitDays: 684,
    patientSupport: "Hemodialysis via AV Fistula",
    patientHospital: "UC Davis Medical Center",
    organNeeded: "Left Kidney",
    cPRA: 0,
    organId: "SYN-ORG-9918",
    organType: "Left Kidney",
    donorId: "D-3912",
    donorAge: 41,
    donorSex: "M",
    donorBloodGroup: "B Rh+",
    donorHospital: "Portland Medical Center",
    donorCity: "Portland, OR",
    perfusionRig: "LifePort Kidney Rig #11 (Hypothermic Pulsatile)",
    perfusionTemp: "4.0 °C",
    coronaryFlow: "98 mL/min renal flow",
    aorticPressure: "Resistive Index: 0.28",
    lactate: "Normal clearance",
    flightCarrier: "Falcon Ground Medical Van 04",
    flightEtaMin: 35,
    citRemaining: "18:42:00",
    matchScore: 84.1,
    mandatoryGatesPassed: 4,
  },
};

interface CaseContextType {
  activeCase: ActiveCase;
  setActiveCaseById: (id: string) => void;
  searchCases: (term: string) => void;
  availableCases: ActiveCase[];
}

const CaseContext = createContext<CaseContextType>({
  activeCase: PRESET_CASES["REC-2026-00421"],
  setActiveCaseById: () => {},
  searchCases: () => {},
  availableCases: Object.values(PRESET_CASES),
});

export const useActiveCase = () => useContext(CaseContext);

export const CaseProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeId, setActiveId] = useState<string>("REC-2026-00421");

  const setActiveCaseById = (id: string) => {
    if (PRESET_CASES[id]) {
      setActiveId(id);
    }
  };

  const searchCases = (term: string) => {
    const q = term.toLowerCase().trim();
    if (!q) return;
    const match = Object.values(PRESET_CASES).find(
      (c) =>
        c.patientId.toLowerCase().includes(q) ||
        c.patientName.toLowerCase().includes(q) ||
        c.organId.toLowerCase().includes(q) ||
        c.organType.toLowerCase().includes(q) ||
        c.donorId.toLowerCase().includes(q)
    );
    if (match) {
      setActiveId(match.patientId);
    }
  };

  return (
    <CaseContext.Provider
      value={{
        activeCase: PRESET_CASES[activeId] || PRESET_CASES["REC-2026-00421"],
        setActiveCaseById,
        searchCases,
        availableCases: Object.values(PRESET_CASES),
      }}
    >
      {children}
    </CaseContext.Provider>
  );
};
