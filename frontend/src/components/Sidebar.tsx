"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bot,
  GitCompare,
  User,
  Heart,
  Navigation,
  BarChart3,
  FileText,
  Radio,
  Layers,
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  // Navigation items strictly without any landing screen option
  const navItems = [
    { label: "Clinical Copilot", href: "/copilot", icon: Bot, tag: "AI + MCP" },
    { label: "Executive Overview", href: "/overview", icon: Layers },
    { label: "Matching Engine", href: "/matching", icon: GitCompare },
    { label: "Patient Dossier", href: "/patients", icon: User },
    { label: "Donor & Telemetry", href: "/organs", icon: Heart },
    { label: "Logistics Radar", href: "/logistics", icon: Navigation },
    { label: "Registry Analytics", href: "/analytics", icon: BarChart3 },
    { label: "Compliance Audit", href: "/audit", icon: FileText },
  ];

  return (
    <aside className="w-72 bg-[#ffffff] border-r border-[#e3e2e0] flex flex-col shrink-0 h-screen sticky top-0 select-none z-20">
      {/* Brand Header */}
      <div className="p-5 border-b border-[#e3e2e0] flex items-center justify-between">
        <Link href="/copilot" className="flex items-center space-x-3.5">
          <div className="w-9 h-9 rounded-[10px] bg-[#000000] text-[#ffffff] flex items-center justify-center font-black text-base">
            O
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-black text-base text-[#1c1301] tracking-tight">ORGANOS</span>
              <span className="text-[11px] font-extrabold px-1.5 py-0.5 rounded-[4px] border border-[#e3e2e0] text-[#1c1301]">
                v4.28
              </span>
            </div>
            <p className="text-xs font-bold text-[#383836]">Clinical Allocation</p>
          </div>
        </Link>
      </div>

      {/* Protocol Banner */}
      <div className="px-5 py-3 bg-[#ffffff] border-b border-[#e3e2e0] flex items-center justify-between text-xs text-[#383836]">
        <span className="text-xs font-bold text-[#1c1301]">UNOS/OPTN PROTOCOL</span>
        <span className="text-xs font-black px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
          Active
        </span>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
        <div className="text-xs font-black text-[#1c1301] px-3 mb-3 uppercase tracking-wider">
          Workspace Views
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3.5 py-3 text-[15px] rounded-[4px] transition-colors ${
                isActive
                  ? "bg-[#000000] text-[#ffffff] font-extrabold"
                  : "text-[#383836] hover:text-[#000000] hover:bg-[#e3e2e0]/30 font-bold"
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon
                  className={`w-4.5 h-4.5 ${
                    isActive ? "text-[#ffffff] stroke-[2.4]" : "text-[#1c1301] stroke-[2]"
                  }`}
                />
                <span>{item.label}</span>
              </div>
              {item.tag && (
                <span
                  className={`text-[11px] px-2 py-0.5 rounded-[4px] border font-black ${
                    isActive
                      ? "border-[#ffffff]/40 text-[#ffffff] bg-[#ffffff]/10"
                      : "border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20"
                  }`}
                >
                  {item.tag}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-[#e3e2e0] text-xs text-[#383836] space-y-2">
        <div className="flex items-center justify-between font-bold">
          <span>Security Protocol:</span>
          <span className="font-mono text-xs font-extrabold text-[#1c1301]">Enclave v2</span>
        </div>
        <div className="text-xs font-bold text-[#1c1301] flex items-center space-x-1.5">
          <span className="w-2 h-2 rounded-[50px] bg-[#000000]" />
          <span>MCP Server Connected</span>
        </div>
      </div>
    </aside>
  );
};
