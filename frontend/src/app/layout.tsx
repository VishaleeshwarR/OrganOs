import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/AppShell";
import { CaseProvider } from "@/context/CaseContext";

export const metadata: Metadata = {
  title: "OrganOS — Clinical Transplant Coordination Workspace",
  description: "Evidence-grounded clinical decision support system for organ allocation and donor matching.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#ffffff] text-[#1c1301] antialiased">
        <CaseProvider>
          <AppShell>{children}</AppShell>
        </CaseProvider>
      </body>
    </html>
  );
}
