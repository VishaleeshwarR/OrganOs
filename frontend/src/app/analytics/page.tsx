"use client";

import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import { BarChart3, Database } from "lucide-react";
import { api } from "@/lib/api";

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const res = await api.getChartsData();
        setData(res);
      } catch (err) {
        console.error("Failed to load analytics:", err);
      } finally {
        setLoading(false);
      }
    }
    loadAnalytics();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <BarChart3 className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Registry Epidemiological Analytics
            </h1>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Population-level organ allocation trends, procurement volume, and post-transplant survival distributions.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-bold text-[#1c1301] px-3.5 py-1.5 rounded-[50px] border border-[#e3e2e0] bg-[#e3e2e0]/20">
          <span className="w-2 h-2 rounded-[50px] bg-[#000000]" />
          <span>OPTN Population Pipeline</span>
        </div>
      </div>

      {loading ? (
        <div className="py-24 text-center text-[#383836] text-sm font-bold">
          Compiling analytics pipelines from synthetic registry...
        </div>
      ) : (
        <div className="space-y-6">
          {/* Row 1: Inventory & Outcomes */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Chart 1: Inventory */}
            <div className="bg-[#ffffff] p-6 rounded-[10px] border border-[#e3e2e0] space-y-4">
              <div className="border-b border-[#e3e2e0] pb-2.5">
                <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
                  Organ Inventory by Category
                </h3>
                <p className="text-xs font-semibold text-[#383836] mt-0.5">Breakdown by anatomical organ type and clinical grade</p>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data?.inventory_distribution || []}>
                    <CartesianGrid strokeDasharray="2 2" stroke="#e3e2e0" />
                    <XAxis dataKey="organ_type" tick={{ fontSize: 12, fill: "#1c1301", fontWeight: 700 }} />
                    <YAxis tick={{ fontSize: 12, fill: "#1c1301", fontWeight: 700 }} />
                    <Tooltip contentStyle={{ fontSize: "12px", fontWeight: 600, backgroundColor: "#ffffff", color: "#1c1301", border: "1px solid #e3e2e0", borderRadius: "4px" }} />
                    <Legend wrapperStyle={{ fontSize: "12px", fontWeight: 700, paddingTop: "8px" }} />
                    <Bar dataKey="good_quality" name="Standard Criteria" fill="#000000" stackId="a" />
                    <Bar dataKey="marginal_quality" name="Extended Criteria" fill="#383836" stackId="a" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 2: Matching Outcomes */}
            <div className="bg-[#ffffff] p-6 rounded-[10px] border border-[#e3e2e0] space-y-4">
              <div className="border-b border-[#e3e2e0] pb-2.5">
                <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
                  Evaluation Outcome Distribution
                </h3>
                <p className="text-xs font-semibold text-[#383836] mt-0.5">Surfaced allocations vs exclusion constraint frequencies</p>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data?.matching_outcomes || []} layout="vertical">
                    <CartesianGrid strokeDasharray="2 2" stroke="#e3e2e0" />
                    <XAxis type="number" tick={{ fontSize: 12, fill: "#1c1301", fontWeight: 700 }} />
                    <YAxis dataKey="outcome" type="category" tick={{ fontSize: 11, fill: "#1c1301", fontWeight: 700 }} width={140} />
                    <Tooltip contentStyle={{ fontSize: "12px", fontWeight: 600, backgroundColor: "#ffffff", color: "#1c1301", border: "1px solid #e3e2e0", borderRadius: "4px" }} />
                    <Bar dataKey="count" name="Evaluations" fill="#1c1301" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Row 2: Procurement Over Time */}
          <div className="bg-[#ffffff] p-6 rounded-[10px] border border-[#e3e2e0] space-y-4">
            <div className="border-b border-[#e3e2e0] pb-2.5">
              <h3 className="text-sm font-black text-[#1c1301] uppercase tracking-wider">
                Monthly Procurement Trends by Organ Category
              </h3>
              <p className="text-xs font-semibold text-[#383836] mt-0.5">Historical volume tracking across Kidney, Liver, and Thoracic grafts</p>
            </div>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data?.availability_trend || []}>
                  <CartesianGrid strokeDasharray="2 2" stroke="#e3e2e0" />
                  <XAxis dataKey="month" tick={{ fontSize: 11, fill: "#1c1301", fontWeight: 700 }} />
                  <YAxis tick={{ fontSize: 12, fill: "#1c1301", fontWeight: 700 }} />
                  <Tooltip contentStyle={{ fontSize: "12px", fontWeight: 600, backgroundColor: "#ffffff", color: "#1c1301", border: "1px solid #e3e2e0", borderRadius: "4px" }} />
                  <Legend wrapperStyle={{ fontSize: "12px", fontWeight: 700, paddingTop: "8px" }} />
                  <Line type="monotone" dataKey="Kidney" stroke="#000000" strokeWidth={2.5} dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="Liver" stroke="#383836" strokeWidth={2.5} strokeDasharray="4 4" dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="Heart" stroke="#1c1301" strokeWidth={2.5} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
