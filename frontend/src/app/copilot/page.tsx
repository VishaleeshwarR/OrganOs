"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Bot,
  Send,
  User,
  Key,
  ShieldCheck,
  RefreshCw,
  Info,
  ChevronDown,
  Check,
  Activity,
  Heart,
  Plane,
  AlertTriangle,
} from "lucide-react";
import { api } from "@/lib/api";
import { useActiveCase, PRESET_CASES } from "@/context/CaseContext";

interface ChatMessage {
  id: string;
  sender: "doctor" | "copilot";
  timestamp: string;
  text: string;
  sources?: string[];
  status?: string;
}

/**
 * Formats raw LLM / MCP response text by stripping markdown symbols
 * and converting to clean readable HTML.
 */
function formatLlmResponse(raw: string): string {
  if (!raw) return "";

  let text = raw;

  // Remove blockquote markers (> at the start of lines)
  text = text.replace(/^>\s?/gm, "");

  // Convert markdown bold (**text** or __text__) to <strong>
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  text = text.replace(/__(.+?)__/g, "<strong>$1</strong>");

  // Convert markdown italic (*text* or _text_)
  text = text.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, "<em>$1</em>");
  text = text.replace(/(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g, "<em>$1</em>");

  // Convert ### headings to styled divs
  text = text.replace(/^###\s+(.+)$/gm, '<div class="copilot-heading">$1</div>');
  text = text.replace(/^##\s+(.+)$/gm, '<div class="copilot-heading">$1</div>');
  text = text.replace(/^#\s+(.+)$/gm, '<div class="copilot-heading">$1</div>');

  // Convert plain text headings like SUMMARY: or DETAILED ANALYSIS:
  text = text.replace(
    /^(SUMMARY|DETAILED CLINICAL ANALYSIS|DETAILED ANALYSIS|REGISTRY EVIDENCE|CLINICAL EVIDENCE|RECOMMENDATION|VERIFICATION DETERMINATION):/gm,
    '<div class="copilot-heading">$1:</div>'
  );

  // Convert bullet points (• or - or *) to styled list items
  text = text.replace(/^[•\-\*]\s+(.+)$/gm, '<div class="copilot-bullet">$1</div>');

  // Remove any remaining stray markdown characters (```, etc.)
  text = text.replace(/```/g, "");

  // Convert numbered lists (1. 2. etc.) to styled items
  text = text.replace(/^\d+\.\s+(.+)$/gm, '<div class="copilot-bullet">$1</div>');

  // Clean up excessive newlines
  text = text.replace(/\n{3,}/g, "\n\n");

  // Convert remaining newlines to <br/> for proper HTML rendering
  text = text.replace(/\n/g, "<br/>");

  // Remove leftover ℹ️ emoji duplication
  text = text.replace(/ℹ️\s*/g, "");

  return text.trim();
}

export default function ClinicalCopilotPage() {
  const { activeCase, setActiveCaseById, availableCases } = useActiveCase();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [customApiKey, setCustomApiKey] = useState("");
  const [showKeySettings, setShowKeySettings] = useState(false);
  const [isPatientDropdownOpen, setIsPatientDropdownOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const patientDropdownRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "msg-init-1",
      sender: "copilot",
      timestamp: "14:27:00 UTC",
      text: `Clinical Decision-Support Copilot online. Active patient: ${activeCase.patientName} (${activeCase.patientId}) · ${activeCase.organNeeded} · ${activeCase.patientBloodGroup} · ${activeCase.patientAcuity}.\n\nAll queries are grounded directly in the Model Context Protocol (MCP) server registry, matching the Patient Dossier, Matching Workspace, and Logistics Radar across OrganOS. Ask any clinical inquiry regarding this candidate.`,
      sources: ["mcp:get_patient", "mcp:evaluate_compatibility", "mcp:find_potential_matches"],
    },
  ]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Close patient dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (patientDropdownRef.current && !patientDropdownRef.current.contains(e.target as Node)) {
        setIsPatientDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // When patient changes via CaseContext (syncs globally across all pages)
  const handleSelectPatient = (id: string) => {
    setActiveCaseById(id);
    setIsPatientDropdownOpen(false);
    const c = PRESET_CASES[id];
    if (!c) return;
    setMessages((prev) => [
      ...prev,
      {
        id: `switch-p-${Date.now()}`,
        sender: "copilot",
        timestamp: new Date().toTimeString().split(" ")[0] + " UTC",
        text: `Active patient switched to: ${c.patientName} (${c.patientId})\n\nClinical Parameters:\n- Organ Required: ${c.organNeeded}\n- Blood Group: ${c.patientBloodGroup}\n- Acuity Tier: ${c.patientAcuity}\n- Waitlist Tenure: ${c.patientWaitDays} Days\n- cPRA Sensitization: ${c.cPRA}%\n- Receiving Hospital: ${c.patientHospital}\n- Clinical Support: ${c.patientSupport}\n- Primary Registry Match: ${c.organId} (${c.matchScore} / 100 Composite Fit Score)\n\nAll dashboard pages are synchronized to this patient. Ready for clinical inquiry.`,
        sources: ["mcp:get_patient", "mcp:evaluate_compatibility"],
      },
    ]);
  };

  // Process Doctor Query via Backend LLM & MCP Server
  const handleSendQuery = async (queryText?: string) => {
    const textToSend = (queryText || input).trim();
    if (!textToSend || loading) return;

    const userMessage: ChatMessage = {
      id: `doc-${Date.now()}`,
      sender: "doctor",
      timestamp: new Date().toTimeString().split(" ")[0] + " UTC",
      text: textToSend,
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!queryText) setInput("");
    setLoading(true);

    try {
      // Send query focused on active patient to backend
      const res = await api.submitQuery(textToSend, {
        patient_id: activeCase.patientId,
        api_key: customApiKey.trim() || undefined,
      });

      const sourcesList = (res.data_sources_consulted || []).map((s) => `mcp:${s.tool}`);

      const copilotMessage: ChatMessage = {
        id: `cop-${Date.now()}`,
        sender: "copilot",
        timestamp: new Date().toTimeString().split(" ")[0] + " UTC",
        text: res.answer || "No clinical evaluation response received from copilot.",
        sources: sourcesList.length > 0 ? sourcesList : ["mcp:get_patient", "mcp:evaluate_compatibility", "mcp:find_potential_matches"],
        status: res.llm_status,
      };

      setMessages((prev) => [...prev, copilotMessage]);
    } catch (err: any) {
      const errorMsg = err?.message || String(err) || "Failed to communicate with LLM / MCP backend.";
      const errorMessage: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: "copilot",
        timestamp: new Date().toTimeString().split(" ")[0] + " UTC",
        text: `ERROR: ${errorMsg}\n\nUnable to reach LLM reasoning engine or MCP server. Please check backend status and API configuration.`,
        sources: ["api:query_error"],
        status: "ERROR",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Title & Subtitle */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <Bot className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              AI Clinical Copilot & MCP Reasoning Console
            </h1>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Grounded clinical decision-support reasoning assistant. Responses are synchronized with all OrganOS platform pages.
          </p>
        </div>

        {/* LLM Key Settings Toggle */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowKeySettings(!showKeySettings)}
            className="flex items-center space-x-2 px-3 py-1.5 rounded-[4px] border border-[#e3e2e0] hover:border-[#000000] text-xs font-bold text-[#1c1301] transition-colors bg-[#ffffff]"
          >
            <Key className="w-3.5 h-3.5 text-[#383836]" />
            <span>{customApiKey ? "Custom LLM Key Configured" : "LLM API Key Settings"}</span>
          </button>
        </div>
      </div>

      {/* LLM Key Settings Drawer */}
      {showKeySettings && (
        <div className="p-4 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] space-y-3 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-black uppercase tracking-wider text-[#1c1301] flex items-center space-x-2">
              <Key className="w-3.5 h-3.5 text-[#000000]" />
              <span>Model & API Key Configuration</span>
            </span>
            <span className="text-[11px] font-bold text-[#383836]">
              Primary: Gemini Flash-Lite (High Uptime) | Backup: Groq Fallback
            </span>
          </div>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="password"
              value={customApiKey}
              onChange={(e) => setCustomApiKey(e.target.value)}
              placeholder="Paste Google Gemini or Groq API Key (optional)"
              className="flex-1 px-3 py-2 text-xs border border-[#e3e2e0] rounded-[4px] font-mono focus:outline-none focus:border-[#000000]"
            />
            {customApiKey && (
              <button
                onClick={() => setCustomApiKey("")}
                className="px-3 py-2 text-xs font-bold border border-[#e3e2e0] rounded-[4px] hover:bg-[#e3e2e0]/20 text-[#383836]"
              >
                Clear
              </button>
            )}
          </div>
          <div className="text-[11px] font-semibold text-[#383836]">
            By default, OrganOS utilizes high-availability Gemini Flash-Lite with automatic Groq backup. If any key experiences an outage or rate limit, clinical reasoning seamlessly continues with the backup key.
          </div>
        </div>
      )}

      {/* ACTIVE PATIENT SELECTION CARD (NO DONOR SELECTION) */}
      <div className="bg-[#ffffff] border border-[#e3e2e0] rounded-[10px] p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#e3e2e0] pb-3">
          <div className="flex items-center space-x-2.5">
            <User className="w-5 h-5 text-[#000000] stroke-[2.2]" />
            <div>
              <span className="text-xs font-black uppercase tracking-wider text-[#1c1301]">
                Active Candidate Patient
              </span>
              <span className="ml-2 text-xs font-bold px-2 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
                Synchronized Across All Pages
              </span>
            </div>
          </div>

          {/* Dropdown Patient Picker */}
          <div className="relative" ref={patientDropdownRef}>
            <button
              onClick={() => setIsPatientDropdownOpen(!isPatientDropdownOpen)}
              className="px-4 py-2 rounded-[4px] border border-[#000000] bg-[#ffffff] hover:bg-[#e3e2e0]/20 text-left transition-colors flex items-center space-x-3 text-xs font-bold text-[#1c1301]"
            >
              <span>Switch Patient: <strong>{activeCase.patientName}</strong> ({activeCase.patientId})</span>
              <ChevronDown className={`w-3.5 h-3.5 text-[#383836] transition-transform ${isPatientDropdownOpen ? "rotate-180" : ""}`} />
            </button>

            {isPatientDropdownOpen && (
              <div className="absolute right-0 top-full mt-1 w-80 bg-[#ffffff] border border-[#e3e2e0] rounded-[4px] shadow-lg overflow-hidden z-50 divide-y divide-[#e3e2e0]">
                <div className="px-3.5 py-2 text-[11px] font-black text-[#1c1301] bg-[#ffffff] uppercase tracking-wider">
                  Select Candidate Patient
                </div>
                {availableCases.map((c) => (
                  <button
                    key={c.patientId}
                    onClick={() => handleSelectPatient(c.patientId)}
                    className={`w-full text-left px-3.5 py-2.5 text-xs flex items-center justify-between hover:bg-[#e3e2e0]/20 transition-colors ${
                      activeCase.patientId === c.patientId ? "bg-[#e3e2e0]/35 font-bold" : "font-semibold"
                    }`}
                  >
                    <div>
                      <div className="text-[#1c1301] font-bold text-sm">{c.patientName}</div>
                      <div className="text-xs font-medium text-[#383836]">
                        {c.patientId} · {c.organNeeded} · {c.patientBloodGroup}
                      </div>
                      <div className="text-[11px] font-bold text-[#1c1301] mt-0.5">
                        {c.patientAcuity}
                      </div>
                    </div>
                    {activeCase.patientId === c.patientId && (
                      <Check className="w-4 h-4 text-[#000000] stroke-[2.5]" />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Detailed Patient Parameters Grid (Matching All Site Pages) */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
          <div className="p-3 rounded-[6px] border border-[#e3e2e0] bg-[#ffffff]">
            <div className="text-[11px] font-black uppercase text-[#383836]">CANDIDATE</div>
            <div className="font-extrabold text-sm text-[#1c1301] mt-1 truncate">{activeCase.patientName}</div>
            <div className="text-xs font-mono font-bold text-[#383836]">{activeCase.patientId}</div>
          </div>

          <div className="p-3 rounded-[6px] border border-[#e3e2e0] bg-[#ffffff]">
            <div className="text-[11px] font-black uppercase text-[#383836]">ORGAN REQUIRED</div>
            <div className="font-extrabold text-sm text-[#1c1301] mt-1">{activeCase.organNeeded}</div>
            <div className="text-xs font-bold text-[#383836]">Type: {activeCase.patientBloodGroup}</div>
          </div>

          <div className="p-3 rounded-[6px] border border-[#e3e2e0] bg-[#ffffff]">
            <div className="text-[11px] font-black uppercase text-[#383836]">ACUITY TIER</div>
            <div className="font-extrabold text-sm text-[#1c1301] mt-1 truncate">{activeCase.patientAcuity}</div>
            <div className="text-xs font-bold text-[#383836]">Tenure: {activeCase.patientWaitDays} Days</div>
          </div>

          <div className="p-3 rounded-[6px] border border-[#e3e2e0] bg-[#ffffff]">
            <div className="text-[11px] font-black uppercase text-[#383836]">SENSITIZATION</div>
            <div className="font-extrabold text-sm text-[#1c1301] mt-1">{activeCase.cPRA}% cPRA</div>
            <div className="text-xs font-bold text-[#383836]">Anti-HLA High Cutoff</div>
          </div>

          <div className="p-3 rounded-[6px] border border-[#e3e2e0] bg-[#ffffff]">
            <div className="text-[11px] font-black uppercase text-[#383836]">RECEIVING HOSPITAL</div>
            <div className="font-extrabold text-sm text-[#1c1301] mt-1 truncate">{activeCase.patientHospital}</div>
            <div className="text-xs font-bold text-[#383836]">OPTN Region 5</div>
          </div>

          <div className="p-3 rounded-[6px] border border-[#e3e2e0] bg-[#ffffff]">
            <div className="text-[11px] font-black uppercase text-[#383836]">PRIMARY MATCH</div>
            <div className="font-extrabold text-sm text-[#1c1301] mt-1 truncate">{activeCase.organId}</div>
            <div className="text-xs font-bold text-[#000000]">{activeCase.matchScore} / 100 Score</div>
          </div>
        </div>
      </div>

      {/* QUICK CLINICIAN PROMPTS (Patient Specific) */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-black uppercase tracking-wider text-[#1c1301] mr-1">Suggested Inquiries:</span>
        <button
          onClick={() => handleSendQuery(`Assess immunological compatibility, 12-locus HLA profile, and virtual crossmatch for ${activeCase.patientName} (${activeCase.patientId})`)}
          className="px-3 py-1.5 rounded-[4px] border border-[#e3e2e0] hover:border-[#000000] text-xs font-bold text-[#1c1301] hover:bg-[#e3e2e0]/20 transition-colors bg-[#ffffff]"
        >
          HLA & Virtual Crossmatch
        </button>
        <button
          onClick={() => handleSendQuery(`Provide composite 4-gate UNOS policy clearance determination and match ranking for ${activeCase.patientName}`)}
          className="px-3 py-1.5 rounded-[4px] border border-[#e3e2e0] hover:border-[#000000] text-xs font-bold text-[#1c1301] hover:bg-[#e3e2e0]/20 transition-colors bg-[#ffffff]"
        >
          4-Gate Policy Determination
        </button>
        <button
          onClick={() => handleSendQuery(`Calculate flight logistics corridor, transfer ETA, and remaining cold ischemia time budget for ${activeCase.patientName}`)}
          className="px-3 py-1.5 rounded-[4px] border border-[#e3e2e0] hover:border-[#000000] text-xs font-bold text-[#1c1301] hover:bg-[#e3e2e0]/20 transition-colors bg-[#ffffff]"
        >
          Cold Ischemia & Flight Logistics
        </button>
        <button
          onClick={() => handleSendQuery(`Review waitlist priority, clinical acuity, and mechanical circulatory support status for ${activeCase.patientName}`)}
          className="px-3 py-1.5 rounded-[4px] border border-[#e3e2e0] hover:border-[#000000] text-xs font-bold text-[#1c1301] hover:bg-[#e3e2e0]/20 transition-colors bg-[#ffffff]"
        >
          Waitlist Priority & Acuity
        </button>
      </div>

      {/* CHAT MESSAGES LOG */}
      <div className="rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] p-6 space-y-4 min-h-[440px] max-h-[620px] overflow-y-auto">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`p-5 rounded-[4px] leading-relaxed border ${
              m.sender === "doctor"
                ? "border-[#e3e2e0] bg-[#e3e2e0]/25 text-[#1c1301] ml-6 sm:ml-12"
                : "border-[#000000] bg-[#ffffff] text-[#1c1301] mr-6 sm:mr-12 shadow-sm"
            }`}
          >
            <div className="flex items-center justify-between mb-2.5 pb-2 border-b border-[#e3e2e0]">
              <span className="font-black text-xs sm:text-sm uppercase tracking-wider text-[#1c1301]">
                {m.sender === "doctor" ? "Clinician Inquiry" : "Model Context Protocol & LLM Reasoning"}
              </span>
              <span className="font-mono text-xs font-black text-[#383836]">{m.timestamp}</span>
            </div>

            {m.sender === "copilot" ? (
              <div
                className="copilot-response text-[15px] sm:text-base font-semibold leading-relaxed text-[#1c1301]"
                dangerouslySetInnerHTML={{ __html: formatLlmResponse(m.text) }}
              />
            ) : (
              <div className="whitespace-pre-line text-[15px] sm:text-base font-semibold leading-relaxed text-[#1c1301]">{m.text}</div>
            )}

            {m.sources && m.sources.length > 0 && (
              <div className="mt-3.5 pt-2.5 border-t border-[#e3e2e0] flex flex-wrap items-center gap-2 text-xs text-[#383836]">
                <span className="font-black text-[#1c1301]">MCP Tools Consulted:</span>
                {m.sources.map((s, idx) => (
                  <span key={idx} className="font-mono px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] font-bold text-[#1c1301] bg-[#e3e2e0]/20">
                    {s}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="p-5 rounded-[4px] border border-[#000000] bg-[#ffffff] mr-6 sm:mr-12 shadow-sm flex items-center space-x-3">
            <RefreshCw className="w-5 h-5 animate-spin text-[#000000]" />
            <div className="text-sm font-bold text-[#1c1301]">
              Executing MCP tools (get_patient, evaluate_compatibility) and synthesizing clinical reasoning...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* INPUT FORM */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendQuery();
        }}
        className="flex items-center space-x-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Ask any clinical question regarding ${activeCase.patientName} (${activeCase.patientId})...`}
          disabled={loading}
          className="flex-1 px-4 py-3 rounded-[4px] border border-[#e3e2e0] focus:border-[#000000] focus:outline-none text-sm font-semibold text-[#1c1301] placeholder:text-[#383836] bg-[#ffffff] transition-colors"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-6 py-3 rounded-[4px] bg-[#000000] text-[#ffffff] font-extrabold text-sm hover:bg-[#1c1301] disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          <span>Send</span>
          <Send className="w-4 h-4 stroke-[2.2]" />
        </button>
      </form>

      {/* Regulatory Notice */}
      <div className="flex items-center space-x-2 text-xs font-semibold text-[#383836] border-t border-[#e3e2e0] pt-4">
        <ShieldCheck className="w-4 h-4 text-[#000000] stroke-[2.2]" />
        <span>
          Clinical Decision Support Prototype. Grounded in deterministic Model Context Protocol (MCP) data. All medical determinations require board-certified surgeon sign-off.
        </span>
      </div>

      {/* Copilot Response Typography Styles */}
      <style jsx global>{`
        .copilot-response {
          line-height: 1.7;
        }
        .copilot-heading {
          font-weight: 900;
          font-size: 1.05rem;
          color: #1c1301;
          margin-top: 1.25rem;
          margin-bottom: 0.5rem;
          padding-bottom: 0.25rem;
          border-bottom: 1px solid #e3e2e0;
          letter-spacing: 0.02em;
          text-transform: uppercase;
        }
        .copilot-heading:first-child {
          margin-top: 0;
        }
        .copilot-bullet {
          padding-left: 1.25rem;
          position: relative;
          margin-bottom: 0.4rem;
          font-weight: 600;
        }
        .copilot-bullet::before {
          content: "—";
          position: absolute;
          left: 0.25rem;
          font-weight: 900;
          color: #000000;
        }
        .copilot-response strong {
          font-weight: 800;
          color: #000000;
        }
        .copilot-response em {
          font-style: normal;
          font-weight: 700;
          color: #1c1301;
        }
      `}</style>
    </div>
  );
}
