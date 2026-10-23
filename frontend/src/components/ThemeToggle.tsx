"use client";

import React from "react";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "@/context/ThemeContext";

export const ThemeToggle: React.FC<{ showLabel?: boolean; className?: string }> = ({
  showLabel = false,
  className = "",
}) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      type="button"
      className={`relative inline-flex items-center justify-center p-1.5 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff] text-[#1c1301] hover:bg-[#e3e2e0]/30 transition-colors ${className}`}
      title={theme === "dark" ? "Switch to Light Theme" : "Switch to Dark Theme"}
      aria-label="Toggle Theme"
    >
      {theme === "dark" ? (
        <Sun className="w-3.5 h-3.5 text-[#1c1301]" />
      ) : (
        <Moon className="w-3.5 h-3.5 text-[#1c1301]" />
      )}
      {showLabel && (
        <span className="ml-1.5 text-xs">
          {theme === "dark" ? "Light Mode" : "Dark Mode"}
        </span>
      )}
    </button>
  );
};
