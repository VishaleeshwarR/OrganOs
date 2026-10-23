"use client";

import React, { useState } from "react";
import { Server, ChevronDown, ChevronUp } from "lucide-react";

interface McpActivityItem {
  tool: string;
  records_evaluated: number;
  latency_ms: number;
  status: string;
  factors?: string[];
  parameters?: Record<string, any>;
}

interface McpActivityPanelProps {
  activities?: McpActivityItem[];
}

export const McpActivityPanel: React.FC<McpActivityPanelProps> = ({ activities }) => {
  const [expanded, setExpanded] = useState(false);

  const defaultActivities: McpActivityItem[] = [
    {
      tool: "find_potential_matches",
      records_evaluated: 27,
      latency_ms: 184,
      status: "Complete",
      factors: ["ABO Compatibility", "6-Loci HLA Alleles", "Cold Ischemia Window", "Logistics Feasibility"],
      parameters: { patient_id: "REC-2026-00421", organ_type: "Heart" },
    },
    {
      tool: "get_patient",
      records_evaluated: 1,
      latency_ms: 21,
      status: "Complete",
      factors: ["HLA Loci", "PRA Percentage", "Urgency Tier", "Listing Status"],
      parameters: { patient_id: "REC-2026-00421" },
    },
    {
      tool: "evaluate_compatibility",
      records_evaluated: 1,
      latency_ms: 38,
      status: "Complete",
      factors: ["Virtual Crossmatch", "Biometric Mass Ratio", "Viability Clearance"],
      parameters: { patient_id: "REC-2026-00421", organ_id: "SYN-ORG-9921" },
    },
  ];

  const items = activities && activities.length > 0 ? activities : defaultActivities;

  return (
    <div className="border border-[#e3e2e0] rounded-[10px] bg-[#ffffff] overflow-hidden text-xs">
      <div
        onClick={() => setExpanded(!expanded)}
        className="px-4 py-3 flex items-center justify-between cursor-pointer hover:bg-[#e3e2e0]/20 transition-colors select-none"
      >
        <div className="flex items-center space-x-2">
          <Server className="w-4 h-4 text-[#000000]" />
          <span className="font-bold text-[#1c1301]">
            Deterministic MCP Tool Execution Log ({items.length} tools executed)
          </span>
        </div>
        <div className="flex items-center space-x-2 text-[11px] text-[#383836]">
          <span>View Execution Trail</span>
          {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </div>
      </div>

      {expanded && (
        <div className="p-4 border-t border-[#e3e2e0] space-y-2 bg-[#ffffff]">
          {items.map((act, idx) => (
            <div key={idx} className="p-2.5 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff] space-y-1">
              <div className="flex items-center justify-between font-mono">
                <span className="font-bold text-[#1c1301]">{act.tool}</span>
                <span className="text-[10px] text-[#383836]">{act.latency_ms} ms</span>
              </div>
              <div className="text-[11px] text-[#383836]">
                Records Evaluated: {act.records_evaluated} · Status: {act.status}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
