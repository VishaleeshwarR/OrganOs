"use client";

import React from "react";
import { Navigation, Clock, Plane, Truck } from "lucide-react";

interface RouteVisualizerProps {
  originName: string;
  originCity: string;
  destName: string;
  destCity: string;
  distanceKm: number;
  etaMinutes: number;
  mode: string;
  preservationRemainingHours: number;
  organId?: string;
  patientId?: string;
}

export const RouteVisualizer: React.FC<RouteVisualizerProps> = ({
  originName,
  originCity,
  destName,
  destCity,
  distanceKm,
  etaMinutes,
  mode,
  preservationRemainingHours,
  organId,
  patientId,
}) => {
  const isAir = mode.includes("AIR");
  const hrs = Math.floor(etaMinutes / 60);
  const mins = etaMinutes % 60;
  const etaFormatted = hrs > 0 ? `${hrs}h ${mins}m` : `${mins}m`;

  return (
    <div className="border border-[#e3e2e0] rounded-[10px] bg-[#ffffff] overflow-hidden text-xs">
      {/* Header Bar */}
      <div className="bg-[#ffffff] px-4 py-2.5 flex items-center justify-between border-b border-[#e3e2e0]">
        <div className="flex items-center space-x-2">
          <Navigation className="w-4 h-4 text-[#000000]" />
          <span className="font-bold text-xs uppercase tracking-wider text-[#1c1301]">
            Transit Logistics & Cold Ischemia Timeline
          </span>
        </div>
        <div className="flex items-center space-x-2 text-[11px] text-[#383836]">
          <span>Graft: <strong className="text-[#1c1301]">{organId || "SYN-ORG-9921"}</strong></span>
          <span className="text-[#e3e2e0]">|</span>
          <span>Recipient: <strong className="text-[#1c1301]">{patientId || "REC-2026-00421"}</strong></span>
        </div>
      </div>

      {/* Route Diagram */}
      <div className="p-5 bg-[#ffffff] border-b border-[#e3e2e0]">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Origin Node */}
          <div className="flex-1 bg-[#ffffff] p-4 rounded-[4px] border border-[#e3e2e0] w-full md:w-auto">
            <div className="text-[10px] font-bold text-[#383836] uppercase tracking-wider mb-1">
              Donor Procurement Facility
            </div>
            <div className="font-bold text-[#1c1301]">{originName}</div>
            <div className="text-[11px] text-[#383836]">{originCity}</div>
          </div>

          {/* Transit Corridor Midpoint */}
          <div className="flex flex-col items-center justify-center px-4 py-2 text-center">
            <div className="p-2 rounded-[50px] border border-[#e3e2e0] bg-[#ffffff] mb-1">
              {isAir ? <Plane className="w-4 h-4 text-[#000000]" /> : <Truck className="w-4 h-4 text-[#000000]" />}
            </div>
            <div className="font-bold text-[#1c1301]">{distanceKm} km · {etaFormatted}</div>
            <div className="text-[10px] text-[#383836] font-mono">{mode}</div>
          </div>

          {/* Destination Node */}
          <div className="flex-1 bg-[#ffffff] p-4 rounded-[4px] border border-[#e3e2e0] w-full md:w-auto text-left md:text-right">
            <div className="text-[10px] font-bold text-[#383836] uppercase tracking-wider mb-1">
              Recipient Operating Theater
            </div>
            <div className="font-bold text-[#1c1301]">{destName}</div>
            <div className="text-[11px] text-[#383836]">{destCity}</div>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="p-4 grid grid-cols-2 md:grid-cols-4 gap-3 bg-[#ffffff]">
        <div>
          <div className="text-[10px] font-bold text-[#383836] uppercase">FLIGHT VECTOR</div>
          <div className="font-bold text-[#1c1301] mt-0.5">{mode}</div>
        </div>
        <div>
          <div className="text-[10px] font-bold text-[#383836] uppercase">ESTIMATED ETA</div>
          <div className="font-bold text-[#1c1301] mt-0.5">{etaFormatted}</div>
        </div>
        <div>
          <div className="text-[10px] font-bold text-[#383836] uppercase">SAFE CIT MARGIN</div>
          <div className="font-bold text-[#1c1301] mt-0.5">+{preservationRemainingHours}h Buffer</div>
        </div>
        <div>
          <div className="text-[10px] font-bold text-[#383836] uppercase">TRANSIT CORRIDOR</div>
          <div className="font-bold text-[#1c1301] mt-0.5">Cleared</div>
        </div>
      </div>
    </div>
  );
};
