"use client";

import React, { useState } from "react";
import { Search, X, Clock, ArrowRight, Bot } from "lucide-react";
import { api } from "@/lib/api";

interface ClinicalQueryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectOrgan?: (organId: string, patientId: string) => void;
}

export const ClinicalQueryModal: React.FC<ClinicalQueryModalProps> = ({
  isOpen,
  onClose,
  onSelectOrgan,
}) => {
  const [query, setQuery] = useState(
    "Evaluate candidate REC-2026-00421 compatibility against available donor graft SYN-ORG-9921."
  );
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.submitQuery(query);
      setResponse(res);
    } catch (err: any) {
      setError(err.message || "Failed to execute clinical registry query");
    } finally {
      setLoading(false);
    }
  };

  const sampleQueries = [
    "Assess HLA crossmatch and virtual XM for candidate REC-2026-00421 against SYN-ORG-9921.",
    "Evaluate cold ischemia time margin and flight logistics for donor graft.",
    "Check donor medical history and any contraindications under UNOS policy.",
  ];

  return (
    <div className="fixed inset-0 z-50 bg-[#000000]/40 flex items-center justify-center p-4">
      <div className="bg-[#ffffff] rounded-[10px] border border-[#e3e2e0] max-w-2xl w-full overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="bg-[#ffffff] px-5 py-3.5 flex items-center justify-between border-b border-[#e3e2e0]">
          <div className="flex items-center space-x-2">
            <Search className="w-4 h-4 text-[#000000]" />
            <h3 className="font-bold text-xs uppercase tracking-wider text-[#1c1301]">
              Clinical Natural Language Query
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-[#383836] hover:text-[#000000] p-1 rounded-[4px] transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 overflow-y-auto space-y-4 text-xs">
          {/* Query Form */}
          <form onSubmit={handleSearch} className="space-y-2">
            <div className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask any clinical question regarding candidate or donor..."
                className="flex-1 px-3.5 py-2 rounded-[4px] border border-[#e3e2e0] text-xs text-[#1c1301] focus:outline-none focus:border-[#000000]"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-[#000000] text-[#ffffff] font-medium rounded-[4px] hover:bg-[#1c1301] transition-colors disabled:opacity-50"
              >
                {loading ? "Searching..." : "Execute"}
              </button>
            </div>

            {/* Quick Sample Chips */}
            <div className="flex flex-wrap gap-1.5 pt-1">
              {sampleQueries.map((q, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => {
                    setQuery(q);
                  }}
                  className="px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] text-[10px] text-[#383836] hover:text-[#1c1301] hover:bg-[#e3e2e0]/20 text-left truncate max-w-xs"
                >
                  {q}
                </button>
              ))}
            </div>
          </form>

          {/* Results Area */}
          {error && (
            <div className="p-3 rounded-[4px] border border-[#e3e2e0] text-[#1c1301] text-xs">
              {error}
            </div>
          )}

          {response && (
            <div className="space-y-3 pt-2 border-t border-[#e3e2e0]">
              <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff] space-y-2 leading-relaxed whitespace-pre-line text-[#1c1301]">
                <div className="text-[10px] font-bold text-[#383836] uppercase tracking-wider">
                  Ground Evidence & MCP Reasoning
                </div>
                <div>{response.answer}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
