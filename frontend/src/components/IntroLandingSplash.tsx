"use client";

import React, { useState, useEffect } from "react";
import { Heart, ArrowRight } from "lucide-react";

export const IntroLandingSplash: React.FC<{ onComplete: () => void }> = ({ onComplete }) => {
  const [progressPercent, setProgressPercent] = useState(0);
  const [systole, setSystole] = useState(false);
  const [isExiting, setIsExiting] = useState(false);
  const [alreadyCompleted, setAlreadyCompleted] = useState(false);

  // Check if intro has already run in this session
  useEffect(() => {
    if (typeof window !== "undefined") {
      const hasRun = sessionStorage.getItem("organos_intro_completed");
      if (hasRun === "true") {
        setAlreadyCompleted(true);
        onComplete();
      }
    }
  }, [onComplete]);

  // 3-second loading cycle
  useEffect(() => {
    if (alreadyCompleted) return;

    const startTime = Date.now();
    const duration = 2800; // 2.8 seconds

    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min((elapsed / duration) * 100, 100);
      setProgressPercent(progress);

      if (elapsed >= duration) {
        clearInterval(timer);
        setIsExiting(true);
        if (typeof window !== "undefined") {
          sessionStorage.setItem("organos_intro_completed", "true");
        }
        setTimeout(() => {
          onComplete();
        }, 250);
      }
    }, 30);

    return () => clearInterval(timer);
  }, [onComplete, alreadyCompleted]);

  // Systole heart pulse cycle
  useEffect(() => {
    const interval = setInterval(() => {
      setSystole(true);
      setTimeout(() => setSystole(false), 200);
    }, 800);
    return () => clearInterval(interval);
  }, []);

  const handleSkip = () => {
    setIsExiting(true);
    if (typeof window !== "undefined") {
      sessionStorage.setItem("organos_intro_completed", "true");
    }
    setTimeout(() => {
      onComplete();
    }, 100);
  };

  if (alreadyCompleted) {
    return null;
  }

  // Calculate SVG stroke parameters for circular perimeter around organ
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (circumference * progressPercent) / 100;

  return (
    <div
      onClick={handleSkip}
      className={`fixed inset-0 z-50 flex flex-col justify-between bg-[#ffffff] text-[#1c1301] p-6 sm:p-10 select-none cursor-pointer transition-opacity duration-300 ${
        isExiting ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
      style={{
        fontFamily:
          'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* Top Protocol Status */}
      <header className="w-full flex items-center justify-between text-xs text-[#383836]">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-[50px] bg-[#000000]" />
          <span className="font-semibold text-[#1c1301] tracking-wider uppercase">
            ORGANOS ALLOCATION CLUSTER
          </span>
          <span className="text-[#e3e2e0]">|</span>
          <span>OPTN / UNOS SECURE SYNC</span>
        </div>

        <div className="flex items-center space-x-3">
          <span className="text-[11px] font-mono text-[#383836]">v4.28</span>
          <span className="px-2 py-0.5 rounded-[4px] border border-[#e3e2e0] text-[#1c1301] text-[10px] font-medium uppercase">
            INITIALIZING
          </span>
        </div>
      </header>

      {/* Main Center Stage: Organ Animation with Loading Ring Tightly Around It */}
      <main className="flex-1 flex flex-col items-center justify-center text-center my-auto py-8">
        <div className="space-y-6 flex flex-col items-center">
          {/* Circular Loading Progress Around the Organ Animation */}
          <div className="relative w-48 h-48 flex items-center justify-center">
            {/* SVG Circular Loading Track Encircling the Organ */}
            <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
              {/* Background Track */}
              <circle
                cx="60"
                cy="60"
                r={radius}
                fill="none"
                stroke="#e3e2e0"
                strokeWidth="3.5"
              />
              {/* Active Progress Arc Around Organ */}
              <circle
                cx="60"
                cy="60"
                r={radius}
                fill="none"
                stroke="#000000"
                strokeWidth="3.5"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                className="transition-all duration-100 ease-linear"
              />
            </svg>

            {/* Organ Animation Center (Pulsating Anatomical Heart) */}
            <div
              className={`absolute inset-0 flex flex-col items-center justify-center transition-transform duration-200 ${
                systole ? "scale-108" : "scale-95"
              }`}
            >
              <Heart className="w-16 h-16 text-[#000000] stroke-[1.6]" />
              <span className="text-[10px] font-mono text-[#383836] mt-1 font-semibold">
                72 BPM
              </span>
            </div>
          </div>

          {/* Loading Indicator Right Around/Below Organ Animation */}
          <div className="space-y-1">
            <div className="text-xl font-bold tracking-tight text-[#1c1301]">
              Loading Transplant Registry... {Math.round(progressPercent)}%
            </div>
            <p className="text-xs text-[#383836] max-w-sm">
              Establishing deterministic MCP connection & verifying UNOS policy clearance.
            </p>
          </div>
        </div>
      </main>

      {/* Footer bar with skip pill */}
      <footer className="w-full flex items-center justify-between text-xs text-[#383836] border-t border-[#e3e2e0] pt-4">
        <div>
          <span>Click anywhere to enter workstation</span>
        </div>
        <button
          onClick={handleSkip}
          className="px-3.5 py-1.5 rounded-[50px] border border-[#e3e2e0] hover:border-[#000000] text-xs font-medium text-[#1c1301] flex items-center space-x-1.5 transition-colors"
        >
          <span>Enter Now</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </footer>
    </div>
  );
};
