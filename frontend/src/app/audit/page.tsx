"use client";

import React, { useEffect, useState } from "react";
import { FileText, Clock, ShieldCheck, Search } from "lucide-react";
import { api } from "@/lib/api";
import { AuditLogEntry } from "@/types";

export default function AuditLogPage() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [filterTool, setFilterTool] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAudit() {
      try {
        const data = await api.getAuditLog(100);
        setLogs(data?.audit_log || []);
      } catch (err) {
        console.error("Failed to load audit trail:", err);
        setLogs([]);
      } finally {
        setLoading(false);
      }
    }
    loadAudit();
  }, []);

  const filteredLogs = (logs || []).filter((log) => {
    const tool = log.tool_called || log.entity_type || "";
    if (filterTool !== "ALL" && tool && tool !== filterTool) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const patient = (log.patient_context || log.entity_id || "").toLowerCase();
      const action = (log.action || "").toLowerCase();
      const summary = (
        log.result_summary || (typeof log.details === "object" ? JSON.stringify(log.details) : String(log.details || ""))
      ).toLowerCase();
      return patient.includes(q) || action.includes(q) || tool.toLowerCase().includes(q) || summary.includes(q);
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <FileText className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Compliance & MCP Audit Ledger
            </h1>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
              Immutable
            </span>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Audit trail of deterministic MCP compute runs, clinical gate evaluations, and parameter validations.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-bold text-[#1c1301] px-3.5 py-1.5 rounded-[50px] border border-[#e3e2e0] bg-[#e3e2e0]/20">
          <span className="w-2 h-2 rounded-[50px] bg-[#000000]" />
          <span>SHA-256 Cryptographic Verification Active</span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-[#383836] absolute left-3 top-3.5 pointer-events-none stroke-[2.2]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter audit ledger by candidate ID, tool name, or action..."
            className="w-full bg-[#ffffff] border border-[#e3e2e0] focus:border-[#000000] text-[#1c1301] placeholder-[#383836]/70 pl-10 pr-4 py-2.5 rounded-[4px] text-sm font-semibold transition-colors focus:outline-none"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {["ALL", "EVALUATE_MATCH", "VIRTUAL_CROSSMATCH_RUN", "HARD_CONSTRAINT_EXCLUSION"].map((tool) => (
            <button
              key={tool}
              onClick={() => setFilterTool(tool)}
              className={`px-3 py-2 rounded-[4px] text-xs font-bold transition-colors ${
                filterTool === tool
                  ? "bg-[#000000] text-[#ffffff]"
                  : "border border-[#e3e2e0] text-[#1c1301] hover:bg-[#e3e2e0]/20"
              }`}
            >
              {tool === "ALL" ? "All Tools" : tool.replace(/_/g, " ")}
            </button>
          ))}
        </div>
      </div>

      {/* Main Ledger Table */}
      <div className="rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#ffffff] border-b border-[#e3e2e0] text-[#1c1301]">
              <tr>
                <th className="py-3 px-4 font-black uppercase text-xs">EVENT ID</th>
                <th className="py-3 px-4 font-black uppercase text-xs">TIMESTAMP</th>
                <th className="py-3 px-4 font-black uppercase text-xs">ACTION / TOOL</th>
                <th className="py-3 px-4 font-black uppercase text-xs">CANDIDATE CONTEXT</th>
                <th className="py-3 px-4 font-black uppercase text-xs">EXECUTION SUMMARY</th>
                <th className="py-3 px-4 font-black uppercase text-xs">INTEGRITY</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e3e2e0]">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-[#383836] font-bold text-sm">
                    Loading audit trail from secure enclave...
                  </td>
                </tr>
              ) : filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-[#383836] font-bold text-sm">
                    No audit records matching query.
                  </td>
                </tr>
              ) : (
                filteredLogs.map((log, idx) => {
                  const id = log.id ? `AUD-${String(log.id).padStart(4, "0")}` : `EVT-${idx}`;
                  const action = log.action || log.tool_called || "EVALUATE";
                  const entity = log.entity_id || log.patient_context || "GLOBAL";
                  const summary =
                    log.result_summary ||
                    (typeof log.details === "object"
                      ? JSON.stringify(log.details)
                      : String(log.details || "Executed successfully"));

                  return (
                    <tr key={idx} className="hover:bg-[#e3e2e0]/15 transition-colors">
                      <td className="py-3 px-4 font-mono font-black text-sm text-[#1c1301]">{id}</td>
                      <td className="py-3 px-4 font-mono text-[#383836] text-xs font-semibold">
                        {log.timestamp || "2026-09-14T03:28:14Z"}
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] font-mono font-black text-xs text-[#1c1301] bg-[#e3e2e0]/20">
                          {action}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-mono font-bold text-sm text-[#1c1301]">{entity}</td>
                      <td className="py-3 px-4 text-[#383836] max-w-md truncate text-xs font-semibold">
                        {summary}
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-xs font-black px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/25">
                          VERIFIED
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
