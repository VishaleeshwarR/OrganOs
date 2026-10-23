"use client";

import React from "react";
import Link from "next/link";
import {
  User,
  Activity,
  AlertTriangle,
  GitCompare,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";

export default function PatientDossierPage() {
  const { activeCase, availableCases, setActiveCaseById } = useActiveCase();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <User className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Patient Clinical Dossier
            </h1>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
              {activeCase.patientAcuity}
            </span>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Recipient immunological profile, 12-locus HLA typing, and waitlist tenure for <strong className="text-[#000000]">{activeCase.patientName}</strong>.
          </p>
        </div>

        {/* Case Switcher */}
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-[#383836]">Candidate:</span>
          {availableCases.map((c) => (
            <button
              key={c.patientId}
              onClick={() => setActiveCaseById(c.patientId)}
              className={`px-3 py-1.5 rounded-[4px] text-xs font-bold transition-colors ${
                activeCase.patientId === c.patientId
                  ? "bg-[#000000] text-[#ffffff]"
                  : "border border-[#e3e2e0] text-[#1c1301] hover:bg-[#e3e2e0]/20"
              }`}
            >
              {c.patientName}
            </button>
          ))}
        </div>
      </div>

      {/* Main Candidate Card */}
      <div className="bg-[#ffffff] border border-[#e3e2e0] rounded-[10px] p-6 sm:p-7 space-y-7">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-5 border-b border-[#e3e2e0] pb-5">
          <div className="flex items-center space-x-4">
            <div className="w-14 h-14 rounded-[10px] bg-[#ffffff] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301] font-black text-xl">
              {activeCase.patientName.split(" ").map((n) => n[0]).join("")}
            </div>
            <div>
              <div className="flex items-center space-x-3">
                <h2 className="text-xl sm:text-2xl font-black text-[#1c1301]">{activeCase.patientName}</h2>
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
                  {activeCase.patientId}
                </span>
              </div>
              <div className="text-sm font-semibold text-[#383836] mt-1">
                {activeCase.patientAge}y · Sex: {activeCase.patientSex} · Blood Group: <strong className="text-[#000000]">{activeCase.patientBloodGroup}</strong> · Organ Required: <strong className="text-[#000000]">{activeCase.organNeeded}</strong>
              </div>
            </div>
          </div>

          <Link
            href="/matching"
            className="px-4 py-2 bg-[#000000] hover:bg-[#1c1301] text-[#ffffff] text-sm font-extrabold rounded-[4px] transition-colors flex items-center space-x-2 self-start md:self-auto"
          >
            <GitCompare className="w-4 h-4 stroke-[2.2]" />
            <span>Launch Matching Matrix</span>
          </Link>
        </div>

        {/* Unique Analysis: Recipient Sensitization & Clinical Tenure */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">WAITLIST TENURE</div>
            <div className="text-2xl sm:text-3xl font-black text-[#1c1301] mt-1">{activeCase.patientWaitDays} Days</div>
            <div className="text-[#383836] text-xs font-semibold mt-0.5">Continuous Active Listing</div>
          </div>
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">CALCULATED PRA (cPRA)</div>
            <div className="text-2xl sm:text-3xl font-black text-[#1c1301] mt-1">{activeCase.cPRA}% Sensitized</div>
            <div className="text-[#383836] text-xs font-semibold mt-0.5">Class I & Class II Luminex</div>
          </div>
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">RECEIVING CENTER</div>
            <div className="text-base font-black text-[#1c1301] mt-1 truncate">{activeCase.patientHospital}</div>
            <div className="text-[#383836] text-xs font-semibold mt-0.5">OPTN Region 5 Allocation</div>
          </div>
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">CLINICAL SUPPORT TIER</div>
            <div className="text-base font-black text-[#1c1301] mt-1 truncate">{activeCase.patientSupport}</div>
            <div className="text-[#383836] text-xs font-semibold mt-0.5">Inpatient CCU Monitoring</div>
          </div>
        </div>

        {/* 12-Locus HLA Profile Analysis (Unique Recipient Analysis) */}
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b border-[#e3e2e0] pb-2">
            <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
              Recipient 12-Locus HLA Allelic Profile
            </h3>
            <span className="text-xs font-bold text-[#383836]">High-Resolution Genotyping</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] font-black text-xs">HLA-A</div>
              <div className="font-extrabold text-[#1c1301] mt-1 font-mono text-sm">*02:01, *24:02</div>
            </div>
            <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] font-black text-xs">HLA-B</div>
              <div className="font-extrabold text-[#1c1301] mt-1 font-mono text-sm">*08:01, *44:02</div>
            </div>
            <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] font-black text-xs">HLA-C</div>
              <div className="font-extrabold text-[#1c1301] mt-1 font-mono text-sm">*07:01, *07:02</div>
            </div>
            <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] font-black text-xs">HLA-DRB1</div>
              <div className="font-extrabold text-[#1c1301] mt-1 font-mono text-sm">*03:01, *15:01</div>
            </div>
          </div>
        </div>

        {/* Sensitized Antibodies & Unacceptable Antigens Panel */}
        <div className="border border-[#e3e2e0] p-5 rounded-[10px] space-y-2 bg-[#ffffff]">
          <div className="text-[#1c1301] font-black text-sm flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-[#000000] stroke-[2.2]" />
            <span>Documented Unacceptable Donor Antigens (MFI &gt; 5,000 Cutoff)</span>
          </div>
          <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
            Anti-HLA-B*07:02 (8,830 MFI) · Anti-HLA-A*01:01 (5,620 MFI). Any procured graft expressing these specific antigens triggers an automated exclusion under UNOS Policy Rule 4.1a to prevent hyperacute crossmatch rejection.
          </p>
        </div>
      </div>
    </div>
  );
}
