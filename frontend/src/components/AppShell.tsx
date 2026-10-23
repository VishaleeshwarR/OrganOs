"use client";

import React, { useState, createContext, useContext } from "react";
import { usePathname } from "next/navigation";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { ClinicalQueryModal } from "./ClinicalQueryModal";
import { MatchInspectorModal } from "./MatchInspectorModal";
import { MatchEvaluation } from "@/types";

interface ShellContextType {
  openQueryModal: () => void;
  inspectEvaluation: (evaluation: MatchEvaluation) => void;
}

const ShellContext = createContext<ShellContextType>({
  openQueryModal: () => {},
  inspectEvaluation: () => {},
});

export const useShell = () => useContext(ShellContext);

export const AppShell: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const pathname = usePathname();
  const [isQueryModalOpen, setIsQueryModalOpen] = useState(false);
  const [inspectedEval, setInspectedEval] = useState<MatchEvaluation | null>(null);

  const openQueryModal = () => setIsQueryModalOpen(true);
  const inspectEvaluation = (evaluation: MatchEvaluation) => setInspectedEval(evaluation);

  // Global key listener for '/' to open clinical query
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "/" && !["INPUT", "TEXTAREA"].includes((e.target as HTMLElement).tagName)) {
        e.preventDefault();
        setIsQueryModalOpen(true);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // On the root landing page, display clean full screen without sidebar/header
  if (pathname === "/") {
    return (
      <ShellContext.Provider value={{ openQueryModal, inspectEvaluation }}>
        <div className="min-h-screen bg-[#ffffff] text-[#1c1301] antialiased">
          {children}
        </div>
      </ShellContext.Provider>
    );
  }

  return (
    <ShellContext.Provider value={{ openQueryModal, inspectEvaluation }}>
      <div className="min-h-screen bg-[#ffffff] text-[#1c1301] flex antialiased">
        {/* Left Persistent Navigation Sidebar */}
        <Sidebar />

        {/* Right Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto bg-[#ffffff]">
          <Header onOpenQueryModal={() => setIsQueryModalOpen(true)} />
          <main className="flex-1 p-6 lg:p-8 max-w-7xl w-full mx-auto">
            {children}
          </main>

          {/* Minimal flat brand footer */}
          <footer className="bg-[#ffffff] border-t border-[#e3e2e0] py-4 px-8 text-xs text-[#383836] flex flex-col sm:flex-row items-center justify-between gap-2">
            <div className="flex items-center space-x-2">
              <span className="text-[#000000] font-bold">ORGANOS v4.28</span>
              <span>•</span>
              <span>SYNTHETIC TRANSPLANT ALLOCATION REGISTRY</span>
              <span>•</span>
              <span>OPTN / UNOS COMPLIANT</span>
            </div>
            <div>
              Deterministic MCP Server Compute · Flat Brand Architecture
            </div>
          </footer>
        </div>
      </div>

      {/* Global Clinical Query Modal */}
      <ClinicalQueryModal
        isOpen={isQueryModalOpen}
        onClose={() => setIsQueryModalOpen(false)}
        onSelectOrgan={(organId, patientId) => {
          window.location.href = `/matching?patient=${patientId}&organ=${organId}`;
        }}
      />

      {/* Match Inspector Modal */}
      <MatchInspectorModal
        isOpen={!!inspectedEval}
        onClose={() => setInspectedEval(null)}
        evaluation={inspectedEval}
      />
    </ShellContext.Provider>
  );
};
