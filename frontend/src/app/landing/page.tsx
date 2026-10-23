"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DedicatedLandingPage() {
  const router = useRouter();

  useEffect(() => {
    // Landing page is not accessible as a persistent navigation view per brand policy
    router.replace("/");
  }, [router]);

  return null;
}
