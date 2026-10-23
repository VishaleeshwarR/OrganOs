"use client";

import React from "react";
import { X } from "lucide-react";
import { MatchEvaluation } from "@/types";

interface MatchInspectorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectOrgan?: (organId: string, patientId: string) => void;
  evaluation: MatchEvaluation | null;
}

export const MatchInspectorModal: React.FC<MatchInspectorModalProps> = ({
  isOpen,
  onClose,
  evaluation,
}) => {
  if (!isOpen || !evaluation) return null;

  const isMatch = evaluation.overall_result === "POTENTIAL_MATCH";
  const evidence = evaluation.explanation_data?.evidence;

  return (
    <div className="fixed inset-0 z-50 bg-[#000000]/40 flex items-center justify-center p-4">
      <div className="bg-[#ffffff] rounded-[10px] border border-[#e3e2e0] max-w-3xl w-full overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="px-5 py-3.5 flex items-center justify-between border-b border-[#e3e2e0] bg-[#ffffff]">
          <div className="flex items-center space-x-3">
            <span className="px-2 py-0.5 rounded-[50px] border border-[#e3e2e0] font-mono text-xs uppercase text-[#1c1301]">
              {isMatch ? "SURFACED MATCH" : "EXCLUDED"}
            </span>
            <div>
              <h3 className="font-bold text-xs uppercase tracking-wide text-[#1c1301]">
                GRAFT {evaluation.organ_id} ↔ CANDIDATE {evaluation.patient_id}
              </h3>
              <p className="text-[11px] text-[#383836]">
                Level: {evaluation.match_level} ({evaluation.classification})
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-[#383836] hover:text-[#000000] p-1 rounded-[4px] transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto flex-1 space-y-4 text-xs">
          <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff] space-y-1">
            <div className="font-bold text-[#1c1301] text-xs">
              {evaluation.explanation_data?.result || "Deterministic Evaluation Complete"}
            </div>
            <p className="text-[11px] text-[#383836] leading-relaxed">
              Classification: {evaluation.explanation_data?.classification || "Multi-gate clinical criteria evaluated."}
              {evaluation.explanation_data?.primary_limiting_factor && (
                <span> · Limiting Factor: {evaluation.explanation_data.primary_limiting_factor}</span>
              )}
            </p>
          </div>

          {/* Evidence Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] text-[10px] uppercase font-bold">ABO STATUS</div>
              <div className="font-bold text-[#1c1301] mt-1">
                {evidence?.organ_blood_group} → {evidence?.recipient_blood_group}
              </div>
            </div>

            <div className="p-3 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] text-[10px] uppercase font-bold">HLA MATCH</div>
              <div className="font-bold text-[#1c1301] mt-1">
                {evidence?.hla_matched_loci}/6 Loci
              </div>
            </div>

            <div className="p-3 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] text-[10px] uppercase font-bold">TRANSPORT ETA</div>
              <div className="font-bold text-[#1c1301] mt-1">
                {evidence?.transport_eta_minutes} min
              </div>
            </div>

            <div className="p-3 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
              <div className="text-[#383836] text-[10px] uppercase font-bold">CIT MARGIN</div>
              <div className="font-bold text-[#1c1301] mt-1">
                +{evidence?.projected_remaining_hours}h Safe
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
