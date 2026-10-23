"use client";

import React, { useEffect, useState } from "react";
import { Building2, Search, CheckCircle, XCircle } from "lucide-react";
import { api } from "@/lib/api";
import { Hospital } from "@/types";

export default function HospitalsPage() {
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [selectedHospital, setSelectedHospital] = useState<Hospital | null>(null);
  const [organProgram, setOrganProgram] = useState("ALL");
  const [cityFilter, setCityFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);

  const loadHospitals = async () => {
    setLoading(true);
    try {
      const data = await api.getHospitals({
        organ_program: organProgram,
        city: cityFilter,
      });
      setHospitals(data.hospitals);
      if (data.hospitals.length > 0 && !selectedHospital) {
        setSelectedHospital(data.hospitals[0]);
      }
    } catch (err) {
      console.error("Failed to load hospitals:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHospitals();
  }, [organProgram, cityFilter]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e3e2e0] pb-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <Building2 className="w-6 h-6 text-[#000000] stroke-[2.2]" />
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-[#1c1301]">
              Transplant Centers & Facilities
            </h1>
          </div>
          <p className="text-sm font-semibold text-[#383836] mt-1">
            Certified transplant institutions with cold storage facilities, HLA laboratories, and 24/7 surgical retrieval readiness.
          </p>
        </div>

        <div className="text-xs font-bold text-[#1c1301] px-3.5 py-1.5 rounded-[50px] border border-[#e3e2e0] bg-[#e3e2e0]/20">
          Indexed: <strong className="text-[#000000] font-black">{hospitals.length}</strong> Centers
        </div>
      </div>

      {/* Filter Strip */}
      <div className="p-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-black text-[#1c1301] uppercase tracking-wider mb-1.5">
            Organ Program Certification
          </label>
          <select
            value={organProgram}
            onChange={(e) => setOrganProgram(e.target.value)}
            className="w-full px-3.5 py-2 text-sm font-semibold border border-[#e3e2e0] rounded-[4px] text-[#1c1301] bg-[#ffffff] focus:outline-none focus:border-[#000000]"
          >
            <option value="ALL">All Certified Programs</option>
            <option value="Kidney">Kidney Transplantation</option>
            <option value="Liver">Liver Transplantation</option>
            <option value="Heart">Heart Transplantation</option>
            <option value="Lung">Lung Transplantation</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-black text-[#1c1301] uppercase tracking-wider mb-1.5">
            Metropolitan Region
          </label>
          <select
            value={cityFilter}
            onChange={(e) => setCityFilter(e.target.value)}
            className="w-full px-3.5 py-2 text-sm font-semibold border border-[#e3e2e0] rounded-[4px] text-[#1c1301] bg-[#ffffff] focus:outline-none focus:border-[#000000]"
          >
            <option value="ALL">All Regions</option>
            <option value="Seattle">Seattle (Washington)</option>
            <option value="San Francisco">San Francisco (California)</option>
            <option value="Portland">Portland (Oregon)</option>
            <option value="Stanford">Stanford (California)</option>
          </select>
        </div>
      </div>

      {/* Hospital List and Selected Detail */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] overflow-hidden">
          <div className="px-5 py-3 border-b border-[#e3e2e0] text-xs font-black text-[#1c1301] uppercase tracking-wider">
            Registered Centers ({hospitals.length})
          </div>
          <div className="divide-y divide-[#e3e2e0] max-h-[500px] overflow-y-auto">
            {loading ? (
              <div className="p-8 text-center text-[#383836] font-bold text-sm">Loading centers...</div>
            ) : (
              hospitals.map((h) => {
                const isSelected = selectedHospital?.hospital_id === h.hospital_id;
                return (
                  <div
                    key={h.hospital_id}
                    onClick={() => setSelectedHospital(h)}
                    className={`p-4 cursor-pointer transition-colors ${
                      isSelected ? "bg-[#e3e2e0]/35 font-bold ring-1 ring-[#000000]" : "hover:bg-[#e3e2e0]/15"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-black text-sm text-[#1c1301]">{h.name}</span>
                      <span className="font-mono text-xs font-bold text-[#383836]">{h.hospital_id}</span>
                    </div>
                    <div className="text-xs font-semibold text-[#383836] mt-1">
                      {h.city}, {h.state} · ICU Beds: <strong className="text-[#000000]">{h.icu_beds}</strong> · HLA Lab: <strong className="text-[#000000]">{h.has_hla_lab ? "Yes" : "No"}</strong>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Selected Center Details */}
        <div className="lg:col-span-5 rounded-[10px] border border-[#e3e2e0] bg-[#ffffff] p-6 space-y-5">
          {selectedHospital ? (
            <>
              <div className="border-b border-[#e3e2e0] pb-4">
                <span className="text-xs font-bold px-2.5 py-0.5 rounded-[50px] border border-[#e3e2e0] text-[#1c1301] bg-[#e3e2e0]/20">
                  {selectedHospital.hospital_id}
                </span>
                <h3 className="text-lg sm:text-xl font-black text-[#1c1301] mt-2">{selectedHospital.name}</h3>
                <p className="text-xs sm:text-sm font-semibold text-[#383836] mt-0.5">{selectedHospital.city}, {selectedHospital.state}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
                  <div className="text-xs text-[#383836] font-black uppercase">ICU CAPACITY</div>
                  <div className="text-xl font-black text-[#1c1301] mt-1">{selectedHospital.icu_beds} Beds</div>
                </div>
                <div className="p-4 rounded-[4px] border border-[#e3e2e0] bg-[#ffffff]">
                  <div className="text-xs text-[#383836] font-black uppercase">HLA LABORATORY</div>
                  <div className="text-xl font-black text-[#1c1301] mt-1">
                    {selectedHospital.has_hla_lab ? "Certified" : "Off-Site"}
                  </div>
                </div>
              </div>

              <div>
                <div className="text-xs text-[#1c1301] font-black uppercase tracking-wider mb-2">Certified Programs</div>
                <div className="flex flex-wrap gap-2">
                  {(selectedHospital.organ_programs || []).map((prog: string, idx: number) => (
                    <span key={idx} className="px-2.5 py-1 rounded-[4px] border border-[#e3e2e0] text-xs font-bold text-[#1c1301] bg-[#e3e2e0]/20">
                      {prog}
                    </span>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="p-8 text-center text-[#383836] font-bold text-sm">Select a hospital to view details.</div>
          )}
        </div>
      </div>
    </div>
  );
}
