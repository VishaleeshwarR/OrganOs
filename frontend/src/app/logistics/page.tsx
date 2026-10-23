"use client";

import React from "react";
import Link from "next/link";
import { Navigation, Plane, Truck, Clock, ArrowRight } from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";

export default function LogisticsPage() {
  const { activeCase, availableCases, setActiveCaseById } = useActiveCase();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <Navigation className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Logistics & Transfer Radar
            </h1>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
              Corridor Active
            </span>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Flight corridor telemetry, airspace vector, and cold ischemia time budget for graft transfer to <strong className="text-[#000000]">{activeCase.patientHospital}</strong>.
          </p>
        </div>

        {/* Case Switcher */}
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-[#383836]">Route:</span>
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
              {c.patientName.split(" ")[0]}
            </button>
          ))}
        </div>
      </div>

      {/* Main Logistics Card */}
      <div className="bg-[#ffffff] border border-[#e3e2e0] rounded-[10px] p-6 sm:p-7 space-y-7">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-5 border-b border-[#e3e2e0] pb-5">
          <div className="flex items-center space-x-4">
            <div className="w-14 h-14 rounded-[10px] bg-[#ffffff] border border-[#e3e2e0] flex items-center justify-center text-[#1c1301]">
              <Plane className="w-8 h-8 text-[#000000] stroke-[2]" />
            </div>
            <div>
              <div className="flex items-center space-x-3">
                <h2 className="text-xl sm:text-2xl font-black text-[#1c1301]">{activeCase.flightCarrier}</h2>
                <span className="text-xs font-extrabold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
                  Airborne Vector
                </span>
              </div>
              <div className="text-sm font-semibold text-[#383836] mt-1">
                Origin: <strong className="text-[#000000]">{activeCase.donorCity}</strong> → Destination: <strong className="text-[#000000]">{activeCase.patientHospital}</strong>
              </div>
            </div>
          </div>

          <Link
            href="/matching"
            className="px-4 py-2 bg-[#000000] hover:bg-[#1c1301] text-[#ffffff] text-sm font-extrabold rounded-[4px] transition-colors flex items-center space-x-2 self-start md:self-auto"
          >
            <span>Review Active Pair</span>
            <ArrowRight className="w-4 h-4 stroke-[2.2]" />
          </Link>
        </div>

        {/* Unique Analysis: Transit Telemetry & Ischemic Window Budget */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">TOUCHDOWN ETA</div>
            <div className="text-2xl sm:text-3xl font-black text-[#1c1301] mt-1">{activeCase.flightEtaMin} Minutes</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Direct Air Corridor Vector</div>
          </div>
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">PRESERVATION BUFFER (CIT)</div>
            <div className="text-2xl sm:text-3xl font-black text-[#1c1301] mt-1">+{activeCase.citRemaining}</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Safe Surgical Margin</div>
          </div>
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">CRUISE ALTITUDE & SPEED</div>
            <div className="text-base font-black text-[#1c1301] mt-1">FL240 · 430 KTAS</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Learjet 45 Dedicated Medevac</div>
          </div>
          <div className="bg-[#ffffff] p-5 rounded-[10px] border border-[#e3e2e0] space-y-1">
            <div className="text-[#383836] uppercase text-xs font-black">AIRSPACE WEATHER</div>
            <div className="text-base font-black text-[#1c1301] mt-1">VFR Nominal</div>
            <div className="text-xs font-semibold text-[#383836] mt-0.5">Zero Weather Hold Detected</div>
          </div>
        </div>

        {/* Ground Corridor & Operating Room Inoculation Timeline */}
        <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-2">
          <div className="flex items-center space-x-2">
            <Truck className="w-5 h-5 text-[#000000] stroke-[2.2]" />
            <span className="font-black text-sm text-[#1c1301]">Dedicated Ground Medical Transport Corridor</span>
          </div>
          <p className="text-xs sm:text-sm font-semibold text-[#383836] leading-relaxed">
            Airport Signature Flight Support FBO staging to {activeCase.patientHospital} Surgical Suite #4. Projected ground ambulance transit time: 18 minutes with dedicated lights & siren police escort staged.
          </p>
        </div>
      </div>
    </div>
  );
}
