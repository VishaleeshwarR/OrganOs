"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  ArrowRight,
  Bot,
  GitCompare,
  Heart,
  Clock,
  ShieldCheck,
} from "lucide-react";
import { useActiveCase } from "@/context/CaseContext";

export const AnimatedOrganHero: React.FC<{ onScrollToChat?: () => void }> = ({ onScrollToChat }) => {
  const { activeCase } = useActiveCase();
  const [systole, setSystole] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(74);

  // Pulse ticker
  useEffect(() => {
    const interval = setInterval(() => {
      setSystole(true);
      setTimeout(() => setSystole(false), 240);
    }, 850);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="rounded-[10px] bg-[#ffffff] border border-[#e3e2e0] p-6 lg:p-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left Column: Brand & Active Allocation Overview */}
        <div className="lg:col-span-7 space-y-5">
          <div className="flex flex-wrap items-center gap-2.5">
            <span className="inline-flex items-center px-3.5 py-1.5 rounded-[50px] text-xs font-bold border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
              <span className="w-2 h-2 rounded-[50px] bg-[#000000] mr-2" />
              UNOS Protocol v4.28 Verified
            </span>
            <span className="inline-flex items-center px-3.5 py-1.5 rounded-[50px] text-xs font-bold border border-[#e3e2e0] text-[#1c1301]">
              Continuous Telemetry Active
            </span>
          </div>

          <div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-[#1c1301] leading-none">
              OrganOS Clinical Allocation
            </h1>
            <p className="text-lg sm:text-xl text-[#383836] mt-3 font-semibold leading-relaxed">
              Clinical decision workstation evaluating candidate <span className="text-[#000000] font-black underline decoration-[#e3e2e0] underline-offset-4">{activeCase.patientName}</span> against donor graft <span className="text-[#000000] font-black underline decoration-[#e3e2e0] underline-offset-4">{activeCase.organId}</span>.
            </p>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-3.5 pt-2">
            <Link
              href="/copilot"
              className="px-6 py-3 rounded-[4px] bg-[#000000] text-[#ffffff] text-base font-extrabold hover:bg-[#1c1301] transition-colors inline-flex items-center space-x-2"
            >
              <Bot className="w-5 h-5 stroke-[2.2]" />
              <span>Open Clinical Copilot</span>
              <ArrowRight className="w-5 h-5 stroke-[2.2]" />
            </Link>
            <Link
              href="/matching"
              className="px-6 py-3 rounded-[4px] border border-[#e3e2e0] text-[#1c1301] text-base font-extrabold hover:bg-[#e3e2e0]/30 transition-colors inline-flex items-center space-x-2"
            >
              <GitCompare className="w-5 h-5 stroke-[2.2]" />
              <span>Matching Matrix</span>
            </Link>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-3 gap-5 pt-6 border-t border-[#e3e2e0]">
            <div>
              <div className="text-xs sm:text-sm font-black uppercase tracking-wider text-[#383836]">Composite Score</div>
              <div className="text-3xl sm:text-4xl font-black text-[#1c1301] mt-1.5">{activeCase.matchScore} / 100</div>
            </div>
            <div>
              <div className="text-xs sm:text-sm font-black uppercase tracking-wider text-[#383836]">Gates Cleared</div>
              <div className="text-3xl sm:text-4xl font-black text-[#1c1301] mt-1.5">{activeCase.mandatoryGatesPassed} / 4 Passed</div>
            </div>
            <div>
              <div className="text-xs sm:text-sm font-black uppercase tracking-wider text-[#383836]">CIT Safe Margin</div>
              <div className="text-3xl sm:text-4xl font-black text-[#1c1301] mt-1.5">+{activeCase.citRemaining}</div>
            </div>
          </div>
        </div>

        {/* Right Column: Flat Organ Animation with Loading Perimeter Ring */}
        <div className="lg:col-span-5 flex flex-col items-center justify-center">
          <div className="w-full max-w-sm rounded-[10px] border border-[#e3e2e0] p-6 bg-[#ffffff] text-center space-y-4">
            <div className="text-xs font-black text-[#1c1301] uppercase tracking-wider">
              Procured Graft Physiology
            </div>

            {/* Circular Perimeter Loading Track Encircling the Organ */}
            <div className="relative w-44 h-44 mx-auto flex items-center justify-center">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  fill="none"
                  stroke="#e3e2e0"
                  strokeWidth="4"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  fill="none"
                  stroke="#000000"
                  strokeWidth="4"
                  strokeDasharray="263.89"
                  strokeDashoffset={263.89 - (263.89 * loadingProgress) / 100}
                  strokeLinecap="round"
                  className="transition-all duration-300"
                />
              </svg>

              {/* Pulsating Organ inside the Ring */}
              <div
                className={`absolute flex flex-col items-center justify-center transition-transform duration-200 ${
                  systole ? "scale-108" : "scale-95"
                }`}
              >
                <Heart className="w-14 h-14 text-[#000000] stroke-[1.8]" />
                <span className="text-xs font-mono text-[#1c1301] mt-1 font-black">
                  72 BPM
                </span>
              </div>
            </div>

            <div className="space-y-1">
              <div className="text-sm font-black text-[#1c1301]">
                {activeCase.organType} · {activeCase.organId}
              </div>
              <div className="text-xs font-bold text-[#383836]">
                Perfusion: {activeCase.coronaryFlow} · Lactate {activeCase.lactate}
              </div>
            </div>

            <div className="pt-3 border-t border-[#e3e2e0] flex items-center justify-between text-xs font-bold text-[#383836]">
              <span>Perfusion Viability Buffer</span>
              <span className="font-mono font-black text-sm text-[#1c1301]">{loadingProgress}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
