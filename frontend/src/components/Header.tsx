"use client";

import React, { useState, useEffect } from "react";
import { Search, ChevronDown, Check } from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";

interface HeaderProps {
  onOpenQueryModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenQueryModal }) => {
  const { activeCase, setActiveCaseById, availableCases, searchCases } = useActiveCase();
  const [searchValue, setSearchValue] = useState("");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState<string>("14:28:09 UTC");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toTimeString().split(" ")[0] + " UTC");
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchValue.trim()) {
      searchCases(searchValue);
      setIsDropdownOpen(false);
    }
  };

  return (
    <div className="flex flex-col bg-[#ffffff] border-b border-[#e3e2e0] select-none sticky top-0 z-30">
      {/* Top Clinical Safety Bar */}
      <div className="bg-[#ffffff] border-b border-[#e3e2e0] px-6 py-2.5 flex items-center justify-between text-xs font-bold text-[#383836]">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-[50px] bg-[#000000]" />
          <span className="font-extrabold text-[#1c1301]">
            Clinical Decision Support System
          </span>
          <span className="text-[#e3e2e0] hidden sm:inline">|</span>
          <span className="hidden sm:inline font-semibold">
            Demonstration Mode · Clinician Verification Required
          </span>
        </div>
        <div className="flex items-center space-x-3 text-xs">
          <span className="font-mono font-bold text-[#1c1301]">{currentTime}</span>
        </div>
      </div>

      {/* Main Command Header */}
      <header className="px-6 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#ffffff]">
        {/* Search Bar with Quick Case Switcher */}
        <div className="flex-1 max-w-xl relative">
          <form onSubmit={handleSearchSubmit} className="relative flex items-center">
            <Search className="w-4 h-4 text-[#383836] absolute left-3 pointer-events-none stroke-[2.2]" />
            <input
              type="text"
              value={searchValue}
              onChange={(e) => {
                setSearchValue(e.target.value);
                searchCases(e.target.value);
              }}
              onFocus={() => setIsDropdownOpen(true)}
              placeholder="Search candidate or donor (e.g. Robert Vance, Elena, SYN-ORG-9921)..."
              className="w-full bg-[#ffffff] border border-[#e3e2e0] focus:border-[#000000] text-[#1c1301] placeholder-[#383836]/70 pl-10 pr-24 py-2 rounded-[4px] text-sm font-semibold transition-colors focus:outline-none"
            />
            <button
              type="button"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="absolute right-2 text-xs font-bold bg-[#ffffff] hover:bg-[#e3e2e0]/30 text-[#1c1301] border border-[#e3e2e0] px-2.5 py-1 rounded-[4px] flex items-center space-x-1.5"
            >
              <span>Cases</span>
              <ChevronDown className="w-3.5 h-3.5 stroke-[2.2]" />
            </button>
          </form>

          {/* Dropdown Case Switcher */}
          {isDropdownOpen && (
            <div
              className="absolute top-full left-0 right-0 mt-1 bg-[#ffffff] border border-[#e3e2e0] rounded-[4px] shadow-sm overflow-hidden z-50 divide-y divide-[#e3e2e0]"
              onMouseLeave={() => setIsDropdownOpen(false)}
            >
              <div className="px-3.5 py-2 text-xs font-black text-[#1c1301] bg-[#ffffff] uppercase tracking-wider">
                Select Active Patient Case
              </div>
              {availableCases.map((c) => (
                <button
                  key={c.patientId}
                  onClick={() => {
                    setActiveCaseById(c.patientId);
                    setIsDropdownOpen(false);
                    setSearchValue(c.patientName);
                  }}
                  className={`w-full text-left px-3.5 py-2.5 text-xs flex items-center justify-between hover:bg-[#e3e2e0]/20 transition-colors ${
                    activeCase.patientId === c.patientId ? "bg-[#e3e2e0]/30 font-bold" : "font-semibold"
                  }`}
                >
                  <div>
                    <div className="text-[#1c1301] font-bold text-sm">{c.patientName} ({c.patientId})</div>
                    <div className="text-xs font-semibold text-[#383836]">
                      {c.organNeeded} · {c.patientBloodGroup} · {c.patientAcuity}
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

        {/* Active Focus Pill & Quick Query Button */}
        <div className="flex items-center space-x-3 shrink-0">
          <div className="px-3.5 py-1.5 rounded-[50px] border border-[#e3e2e0] text-xs font-bold text-[#383836] flex items-center space-x-2">
            <span>Active:</span>
            <span className="font-extrabold text-[#1c1301]">{activeCase.patientName}</span>
            <span className="text-[#e3e2e0]">|</span>
            <span className="font-bold text-[#1c1301]">{activeCase.organType}</span>
          </div>

          <button
            onClick={onOpenQueryModal}
            className="px-4 py-1.5 rounded-[4px] bg-[#000000] text-[#ffffff] text-xs font-bold hover:bg-[#1c1301] transition-colors flex items-center space-x-1.5"
          >
            <span>Query</span>
            <kbd className="text-[11px] opacity-80 font-mono font-bold">[/]</kbd>
          </button>
        </div>
      </header>
    </div>
  );
};
