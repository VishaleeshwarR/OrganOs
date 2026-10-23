"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { IntroLandingSplash } from "@/components/IntroLandingSplash";

export default function RootLandingPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    setMounted(true);
    // If intro has already completed during this session, immediately route to AI Copilot
    if (typeof window !== "undefined") {
      const hasCompleted = sessionStorage.getItem("organos_intro_completed");
      if (hasCompleted === "true") {
        router.replace("/copilot");
      }
    }
  }, [router]);

  const handleLandingComplete = () => {
    if (typeof window !== "undefined") {
      sessionStorage.setItem("organos_intro_completed", "true");
    }
    setShowSplash(false);
    router.push("/copilot");
  };

  if (!mounted) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 bg-[#ffffff]">
      {showSplash && (
        <IntroLandingSplash onComplete={handleLandingComplete} />
      )}
    </div>
  );
}
