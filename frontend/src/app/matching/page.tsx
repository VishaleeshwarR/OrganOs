"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  GitCompare,
  CheckCircle2,
  XCircle,
  Clock,
  ArrowRight,
  ShieldCheck,
  Check,
} from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";

export default function MatchingPage() {
  const { activeCase, availableCases, setActiveCaseById } = useActiveCase();
  const [offerAccepted, setOfferAccepted] = useState(false);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <GitCompare className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Deterministic Matching Analysis Workspace
            </h1>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
              Case #{activeCase.patientId.replace("REC-2026-00", "MATCH-")}
            </span>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Algorithmic 4-gate verification and candidate exclusion matrix for <strong className="text-[#000000]">{activeCase.patientName}</strong> against graft <strong className="text-[#000000]">{activeCase.organId}</strong>.
          </p>
        </div>

        {/* Case Switcher */}
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-[#383836]">Case:</span>
          {availableCases.map((c) => (
            <button
              key={c.patientId}
              onClick={() => {
                setActiveCaseById(c.patientId);
                setOfferAccepted(false);
              }}
              className={`px-3 py-1.5 rounded-[4px] text-xs font-bold transition-colors ${
                activeCase.patientId === c.patientId
                  ? "bg-[#000000] text-[#ffffff]"
                  : "border border-[#e3e2e0] text-[#1c1301] hover:bg-[#e3e2e0]/20"
              }`}
            >
              {c.patientName.split(" ")[0]}
            </button>
          ))}
        </div>
      </div>

      {/* Primary Score & Acceptance Decision Bar */}
      <div className="bg-[#ffffff] border border-[#e3e2e0] rounded-[10px] p-6 sm:p-7 space-y-7">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-5 border-b border-[#e3e2e0] pb-5">
          <div>
            <div className="flex items-center space-x-3.5">
              <span className="text-4xl sm:text-5xl font-black text-[#1c1301]">
                {activeCase.matchScore}
                <span className="text-lg text-[#383836] font-bold"> / 100</span>
              </span>
              <span className="text-xs sm:text-sm px-3 py-1 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] font-extrabold bg-[#e3e2e0]/25">
                Rank #1 SURFACED ALLOCATION
              </span>
            </div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] mt-1.5">
              Composite Fit Score generated deterministically via UNOS Policy Algorithm v4.28.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => setOfferAccepted(!offerAccepted)}
              className={`px-5 py-2.5 text-sm font-extrabold rounded-[4px] transition-colors flex items-center space-x-2 ${
                offerAccepted
                  ? "bg-[#e3e2e0]/35 border border-[#000000] text-[#1c1301]"
                  : "bg-[#000000] hover:bg-[#1c1301] text-[#ffffff]"
              }`}
            >
              {offerAccepted ? (
                <>
                  <Check className="w-4 h-4 text-[#000000] stroke-[2.5]" />
                  <span>Allocation Clearance Staged</span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-4 h-4 stroke-[2.2]" />
                  <span>Authorize Primary Offer</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* 4 Deterministic Gates Breakdown (Unique to Matching Engine) */}
        <div className="space-y-4">
          <div className="border-b border-[#e3e2e0] pb-2">
            <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
              Deterministic Gate-by-Gate Evaluation
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Gate 1 */}
            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-black text-sm sm:text-base text-[#1c1301]">Gate 1: Serological ABO Compatibility</span>
                <span className="text-xs px-2.5 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                  PASSED
                </span>
              </div>
              <div className="text-xs font-bold text-[#383836]">
                Formula: Isohemagglutinin Cross-Match Matrix. Donor: {activeCase.donorBloodGroup} → Recipient: {activeCase.patientBloodGroup}.
              </div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                Complete immunological sero-identity confirmed. Zero risk of ABO incompatible hyperacute hemolysis.
              </p>
            </div>

            {/* Gate 2 */}
            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-black text-sm sm:text-base text-[#1c1301]">Gate 2: Biometric Sizing & Predicted Mass</span>
                <span className="text-xs px-2.5 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                  PASSED
                </span>
              </div>
              <div className="text-xs font-bold text-[#383836]">
                Formula: Predicted Heart Mass Ratio (PHMR = 1.04). Allowed tolerance: 0.80 – 1.30.
              </div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                Intrathoracic cavity dimensions compatible. Mass variance within +4% ideal surgical clearance.
              </p>
            </div>

            {/* Gate 3 */}
            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-black text-sm sm:text-base text-[#1c1301]">Gate 3: Virtual Crossmatch & Donor-Specific Antibodies</span>
                <span className="text-xs px-2.5 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                  PASSED
                </span>
              </div>
              <div className="text-xs font-bold text-[#383836]">
                Formula: Luminex Single Antigen MFI cutoff &lt; 1,000 MFI across 12 loci.
              </div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                0 DSA identified in recipient serum against donor alleles. Recipient cPRA {activeCase.cPRA}% avoided.
              </p>
            </div>

            {/* Gate 4 */}
            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-black text-sm sm:text-base text-[#1c1301]">Gate 4: Machine Perfusion Viability & CIT Safe Margin</span>
                <span className="text-xs px-2.5 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                  PASSED
                </span>
              </div>
              <div className="text-xs font-bold text-[#383836]">
                Formula: Coronary Flow &gt; 1.0 L/min, Lactate Vector Decreasing, CIT Margin &gt; 90 min.
              </div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                Active coronary flow {activeCase.coronaryFlow}, Lactate {activeCase.lactate}. Safe CIT buffer +{activeCase.citRemaining}.
              </p>
            </div>
          </div>
        </div>

        {/* Excluded Candidates Matrix (Unique to Matching Engine) */}
        <div className="space-y-4">
          <div className="border-b border-[#e3e2e0] pb-2">
            <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
              Candidate Pool Exclusion Audit (27 Organs Screened)
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div className="p-4 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-1">
              <div className="text-[#383836] text-xs font-black uppercase">ABO INCOMPATIBLE</div>
              <div className="text-2xl font-black text-[#1c1301] mt-1">12 Grafts</div>
              <p className="text-xs font-semibold text-[#383836] mt-0.5">Excluded by Serology Gate 1</p>
            </div>

            <div className="p-4 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-1">
              <div className="text-[#383836] text-xs font-black uppercase">SIZE / MASS VARIANCE</div>
              <div className="text-2xl font-black text-[#1c1301] mt-1">8 Grafts</div>
              <p className="text-xs font-semibold text-[#383836] mt-0.5">PHMR Outside [0.80, 1.30]</p>
            </div>

            <div className="p-4 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-1">
              <div className="text-[#383836] text-xs font-black uppercase">TRANSIT CIT EXCEEDED</div>
              <div className="text-2xl font-black text-[#1c1301] mt-1">4 Grafts</div>
              <p className="text-xs font-semibold text-[#383836] mt-0.5">Transit ETA &gt; 4h 00m</p>
            </div>

            <div className="p-4 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-1">
              <div className="text-[#383836] text-xs font-black uppercase">VIABLE CANDIDATES</div>
              <div className="text-2xl font-black text-[#1c1301] mt-1">3 Grafts</div>
              <p className="text-xs font-semibold text-[#383836] mt-0.5">Top Match: {activeCase.organId}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
