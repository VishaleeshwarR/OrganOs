"use client";

import React from "react";
import Link from "next/link";
import {
  Bot,
  GitCompare,
  ArrowRight,
  Terminal,
  Clock,
  ShieldCheck,
} from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";
import { AnimatedOrganHero } from "@/components/AnimatedOrganHero";

export default function ExecutiveOverviewPage() {
  const { activeCase, availableCases, setActiveCaseById } = useActiveCase();

  return (
    <div className="space-y-10">
      {/* SECTION 1: HERO */}
      <section id="hero">
        <AnimatedOrganHero />
      </section>

      {/* SECTION 2: EXECUTIVE PATIENT & GRAFT ALLOCATION ANALYSIS */}
      <section className="space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
          <div>
            <h2 className="text-2xl sm:text-3xl font-black text-[#1c1301]">
              Executive Gate Clearance Analysis
            </h2>
            <p className="text-sm font-semibold text-[#383836] mt-1">
              Non-repeating executive allocation status for active pair: <strong className="text-[#000000]">{activeCase.patientName}</strong> & <strong className="text-[#000000]">{activeCase.organId}</strong>.
            </p>
          </div>

          {/* Quick Case Switcher */}
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-[#383836]">Case:</span>
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

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="flex items-center justify-between text-xs font-bold text-[#383836]">
              <span className="uppercase tracking-wider">Gate 1: Serology</span>
              <span className="text-xs px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                CLEARED
              </span>
            </div>
            <div className="text-base font-black text-[#1c1301]">ABO Identical</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              Recipient {activeCase.patientBloodGroup} to Donor {activeCase.donorBloodGroup}. Complete isohemagglutinin compatibility verified.
            </p>
          </div>

          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="flex items-center justify-between text-xs font-bold text-[#383836]">
              <span className="uppercase tracking-wider">Gate 2: Biometrics</span>
              <span className="text-xs px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                CLEARED
              </span>
            </div>
            <div className="text-base font-black text-[#1c1301]">PHMR 1.04 Ratio</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              Predicted heart mass ratio within +4% physiological tolerance. Intrathoracic cavity dimensions compatible.
            </p>
          </div>

          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="flex items-center justify-between text-xs font-bold text-[#383836]">
              <span className="uppercase tracking-wider">Gate 3: Virtual XM</span>
              <span className="text-xs px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                CLEARED
              </span>
            </div>
            <div className="text-base font-black text-[#1c1301]">0 DSA Detected</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              Luminex Single Antigen Bead assay shows 0 donor-specific antibodies against donor HLA alleles.
            </p>
          </div>

          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="flex items-center justify-between text-xs font-bold text-[#383836]">
              <span className="uppercase tracking-wider">Gate 4: Viability</span>
              <span className="text-xs px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-[#1c1301] bg-[#e3e2e0]/20">
                CLEARED
              </span>
            </div>
            <div className="text-base font-black text-[#1c1301]">Active Perfusion</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              {activeCase.perfusionRig}. Flow {activeCase.coronaryFlow}, Lactate {activeCase.lactate}.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 3: FEATURES */}
      <section id="features" className="space-y-5">
        <div className="border-b border-[#e3e2e0] pb-3">
          <h2 className="text-2xl sm:text-3xl font-black text-[#1c1301]">System Protocol Features</h2>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Standardized clinical coordination components integrated with the Model Context Protocol.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="w-8 h-8 rounded-[4px] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301]">
              <GitCompare className="w-4 h-4 stroke-[2.2]" />
            </div>
            <div className="text-sm font-black text-[#1c1301]">Deterministic Matching</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              4-gate evaluation executing serology, biometric sizing, virtual crossmatch, and physiological thresholds without subjective drift.
            </p>
          </div>

          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="w-8 h-8 rounded-[4px] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301]">
              <Terminal className="w-4 h-4 stroke-[2.2]" />
            </div>
            <div className="text-sm font-black text-[#1c1301]">MCP Tool Registry</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              Tools like <code>evaluate_compatibility</code> and <code>search_patients</code> connect real-time data to surgical teams.
            </p>
          </div>

          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="w-8 h-8 rounded-[4px] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301]">
              <Clock className="w-4 h-4 stroke-[2.2]" />
            </div>
            <div className="text-sm font-black text-[#1c1301]">Cold Ischemia Radar</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              Corridor telemetry factoring flight speeds and ambulance transfers against the graft safe preservation ceiling.
            </p>
          </div>

          <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2.5">
            <div className="w-8 h-8 rounded-[4px] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301]">
              <ShieldCheck className="w-4 h-4 stroke-[2.2]" />
            </div>
            <div className="text-sm font-black text-[#1c1301]">Compliance Auditing</div>
            <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
              Tamper-evident logs of every clinical parameter examined, providing auditability for organ allocation review.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 4: CTA TO COPILOT */}
      <section id="cta" className="p-7 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5">
          <div className="space-y-1.5">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-[50px] border border-[#e3e2e0] text-xs font-bold text-[#1c1301] bg-[#e3e2e0]/20">
              <Bot className="w-3.5 h-3.5 text-[#000000] stroke-[2.2]" />
              <span>AI Clinical Copilot & MCP Query Console</span>
            </div>
            <h3 className="text-lg sm:text-xl font-black text-[#1c1301]">
              Have questions regarding this candidate or donor graft?
            </h3>
            <p className="text-xs sm:text-sm font-semibold text-[#383836]">
              Query HLA crossmatches, cold ischemia thresholds, or policy clearance via the interactive copilot.
            </p>
          </div>

          <Link
            href="/copilot"
            className="px-5 py-3 rounded-[4px] bg-[#000000] text-[#ffffff] text-sm font-extrabold hover:bg-[#1c1301] inline-flex items-center space-x-2 shrink-0 transition-colors"
          >
            <span>Open Dedicated Chatbot</span>
            <ArrowRight className="w-4 h-4 stroke-[2.2]" />
          </Link>
        </div>
      </section>
    </div>
  );
}
