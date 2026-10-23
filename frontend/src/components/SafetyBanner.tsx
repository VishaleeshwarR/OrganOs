"use client";

import React from "react";
import { AlertTriangle } from "lucide-react";

export const SafetyBanner: React.FC = () => {
  return (
    <div className="bg-[#ffffff] border-b border-[#e3e2e0] text-[#383836] px-4 py-1.5 text-xs flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <span className="inline-flex items-center px-1.5 py-0.2 rounded-[4px] border border-[#e3e2e0] text-[#1c1301] font-mono font-bold text-[10px] tracking-wider">
          SYNTHETIC DEMO
        </span>
        <span className="font-semibold text-[#1c1301]">
          Clinical Decision-Support Demonstration Prototype
        </span>
        <span className="hidden md:inline text-[#383836]">
          — Synthetic data only. Clinician verification required for actual organ allocation.
        </span>
      </div>
      <div className="flex items-center space-x-2 text-[11px] font-mono text-[#383836]">
        <span>Deterministic MCP Engine</span>
      </div>
    </div>
  );
};
