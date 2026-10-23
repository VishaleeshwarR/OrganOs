"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Heart,
  Clock,
  Activity,
  GitCompare,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";

export default function OrganTelemetryPage() {
  const { activeCase, availableCases, setActiveCaseById } = useActiveCase();
  const [citElapsedSecs, setCitElapsedSecs] = useState(4367); // 01:12:47

  useEffect(() => {
    const timer = setInterval(() => {
      setCitElapsedSecs((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatElapsed = (secs: number) => {
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <Heart className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Donor Graft & Perfusion Telemetry
            </h1>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
              {activeCase.organId}
            </span>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Real-time machine perfusion hemodynamics, perfusate lactate clearance, and procurement viability for <strong className="text-[#000000]">{activeCase.organType}</strong>.
          </p>
        </div>

        {/* Case Switcher */}
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-[#383836]">Target Graft:</span>
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
              {c.organId}
            </button>
          ))}
        </div>
      </div>

      {/* Main Perfusion Telemetry Card */}
      <div className="bg-[#ffffff] border border-[#e3e2e0] rounded-[10px] p-6 sm:p-7 space-y-7">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-5 border-b border-[#e3e2e0] pb-5">
          <div className="flex items-center space-x-4">
            <div className="w-14 h-14 rounded-[10px] bg-[#ffffff] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301]">
              <Heart className="w-8 h-8 text-[#000000] stroke-[2]" />
            </div>
            <div>
              <div className="flex items-center space-x-3">
                <h2 className="text-xl sm:text-2xl font-black text-[#1c1301]">{activeCase.organType} ({activeCase.organId})</h2>
                <span className="text-xs font-extrabold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
                  Preserved Active
                </span>
              </div>
              <div className="text-sm font-semibold text-[#383836] mt-1">
                Donor {activeCase.donorId} ({activeCase.donorAge}y {activeCase.donorSex}) · Blood Group: <strong className="text-[#000000]">{activeCase.donorBloodGroup}</strong> · Procured at: <strong className="text-[#000000]">{activeCase.donorHospital}</strong>
              </div>
            </div>
          </div>

          <Link
            href="/matching"
            className="px-4 py-2 bg-[#000000] hover:bg-[#1c1301] text-[#ffffff] text-sm font-extrabold rounded-[4px] transition-colors flex items-center space-x-2 self-start md:self-auto"
          >
            <GitCompare className="w-4 h-4 stroke-[2.2]" />
            <span>Verify Crossmatch Matrix</span>
          </Link>
        </div>

        {/* Unique Graft Physiological Analysis: Perfusion Telemetry Dials */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="bg-[#ffffff] p-4 rounded-[10px] border border-[#e3e2e0] text-center space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">ISCHEMIA ELAPSED</div>
            <div className="text-xl sm:text-2xl font-black text-[#1c1301] mt-1 font-mono">
              {formatElapsed(citElapsedSecs)}
            </div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Limit: 04:00:00</div>
          </div>

          <div className="bg-[#ffffff] p-4 rounded-[10px] border border-[#e3e2e0] text-center space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">AORTIC PRESSURE</div>
            <div className="text-xl sm:text-2xl font-black text-[#1c1301] mt-1">{activeCase.aorticPressure}</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Normotensive Target</div>
          </div>

          <div className="bg-[#ffffff] p-4 rounded-[10px] border border-[#e3e2e0] text-center space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">PERFUSION FLOW</div>
            <div className="text-xl sm:text-2xl font-black text-[#1c1301] mt-1">{activeCase.coronaryFlow}</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Continuous Coronary</div>
          </div>

          <div className="bg-[#ffffff] p-4 rounded-[10px] border border-[#e3e2e0] text-center space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">PERFUSATE TEMP</div>
            <div className="text-xl sm:text-2xl font-black text-[#1c1301] mt-1">{activeCase.perfusionTemp}</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Regulated Cold Buffer</div>
          </div>

          <div className="bg-[#ffffff] p-4 rounded-[10px] border border-[#e3e2e0] text-center space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">LACTATE CLEARANCE</div>
            <div className="text-xl sm:text-2xl font-black text-[#1c1301] mt-1">{activeCase.lactate.split(" ")[0]}</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Downhill Trend</div>
          </div>

          <div className="bg-[#ffffff] p-4 rounded-[10px] border border-[#e3e2e0] text-center space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">PUMP RHYTHM</div>
            <div className="text-xl sm:text-2xl font-black text-[#1c1301] mt-1">74 BPM</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Pulsatile OCS Rig</div>
          </div>
        </div>

        {/* Procurement Biopsy Findings & Viability Metrics (Unique to Organs page) */}
        <div className="space-y-4">
          <div className="border-b border-[#e3e2e0] pb-2">
            <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
              Procurement Biopsy & Morphometric Assessment
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2">
              <div className="text-[#383836] text-xs font-black uppercase">HISTOPATHOLOGY BIOPSY</div>
              <div className="font-black text-base text-[#1c1301]">Zero Evidence of Microthrombi</div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                Frozen section review confirms preserved myocyte architecture and absence of acute ischemia reperfusion injury.
              </p>
            </div>

            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2">
              <div className="text-[#383836] text-xs font-black uppercase">CORONARY ANGIOGRAM</div>
              <div className="font-black text-base text-[#1c1301]">Pristine Coronary Vessels</div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                Donor coronary catheterization reveals zero stenosis in LAD, LCx, and RCA branches.
              </p>
            </div>

            <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2">
              <div className="text-[#383836] text-xs font-black uppercase">ECHOCARDIOGRAPHY LVEF</div>
              <div className="font-black text-base text-[#1c1301]">LVEF 62% Pre-Procurement</div>
              <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
                Normal biventricular systolic function with normal wall motion and absence of valvular regurgitation.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
