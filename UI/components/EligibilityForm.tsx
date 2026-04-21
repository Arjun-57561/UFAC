"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { eligibilitySchema, type EligibilityFormData } from "@/lib/api";
import { TogglePill } from "./TogglePill";
import { Search, IndianRupee, HelpCircle } from "lucide-react";
import { motion } from "framer-motion";

interface EligibilityFormProps {
  onSubmit: (data: EligibilityFormData) => void;
  isLoading: boolean;
}

export function EligibilityForm({ onSubmit, isLoading }: EligibilityFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<EligibilityFormData>({
    resolver: zodResolver(eligibilitySchema),
  });

  const watchedValues = watch();

  const Tooltip = ({ text }: { text: string }) => (
    <div className="group relative inline-block">
      <HelpCircle className="w-4 h-4 text-[hsl(var(--text-muted))] cursor-help" />
      <div className="absolute left-0 bottom-full mb-2 w-64 p-2 bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 text-xs text-[hsl(var(--text-secondary))]">
        {text}
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {/* Section 1: Personal Details */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-[hsl(var(--text-muted))] uppercase tracking-wide">
          Personal Details
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-[hsl(var(--text-primary))] mb-2">
              Your Occupation <span className="text-red-500">*</span>
            </label>
            <input
              {...register("occupation")}
              type="text"
              placeholder="e.g. Farmer"
              disabled={isLoading}
              className="w-full px-4 py-3 rounded-lg bg-[hsl(var(--bg-input))] border border-[hsl(var(--border))] text-[hsl(var(--text-primary))] placeholder:text-[hsl(var(--text-muted))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] disabled:opacity-50"
            />
            {errors.occupation && (
              <p className="text-sm text-red-500 mt-1">
                {errors.occupation.message}
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-[hsl(var(--text-primary))] mb-2">
                State
              </label>
              <input
                {...register("state")}
                type="text"
                placeholder="e.g. Punjab"
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-lg bg-[hsl(var(--bg-input))] border border-[hsl(var(--border))] text-[hsl(var(--text-primary))] placeholder:text-[hsl(var(--text-muted))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] disabled:opacity-50"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[hsl(var(--text-primary))] mb-2">
                District
              </label>
              <input
                {...register("district")}
                type="text"
                placeholder="e.g. Ludhiana"
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-lg bg-[hsl(var(--bg-input))] border border-[hsl(var(--border))] text-[hsl(var(--text-primary))] placeholder:text-[hsl(var(--text-muted))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] disabled:opacity-50"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-[hsl(var(--border))]" />

      {/* Section 2: Land & Financial Details */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-[hsl(var(--text-muted))] uppercase tracking-wide">
          Land & Financial Details
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-[hsl(var(--text-primary))] mb-2">
              Land Ownership
            </label>
            <TogglePill
              value={
                watchedValues.land_ownership === "yes"
                  ? true
                  : watchedValues.land_ownership === "no"
                  ? false
                  : undefined
              }
              onChange={(val) => setValue("land_ownership", val ? "yes" : "no")}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-[hsl(var(--text-primary))] mb-2">
              Annual Income (₹)
            </label>
            <div className="relative">
              <IndianRupee className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[hsl(var(--text-muted))]" />
              <input
                {...register("annual_income", { valueAsNumber: true })}
                type="number"
                placeholder="Leave blank if unknown"
                disabled={isLoading}
                className="w-full pl-10 pr-4 py-3 rounded-lg bg-[hsl(var(--bg-input))] border border-[hsl(var(--border))] text-[hsl(var(--text-primary))] placeholder:text-[hsl(var(--text-muted))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] disabled:opacity-50"
              />
            </div>
            <p className="text-xs text-[hsl(var(--text-muted))] mt-1">
              Leave blank if unknown
            </p>
            {errors.annual_income && (
              <p className="text-sm text-red-500 mt-1">
                {errors.annual_income.message}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="border-t border-[hsl(var(--border))]" />

      {/* Section 3: Verification & Eligibility Checks */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-[hsl(var(--text-muted))] uppercase tracking-wide">
          Verification & Eligibility Checks
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium text-[hsl(var(--text-primary))]">
                Aadhaar Linked to Bank
              </label>
            </div>
            <TogglePill
              value={watchedValues.aadhaar_linked}
              onChange={(val) => setValue("aadhaar_linked", val)}
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-[hsl(var(--text-primary))]">
              Aadhaar e-KYC Completed
            </label>
            <TogglePill
              value={watchedValues.aadhaar_ekyc_done}
              onChange={(val) => setValue("aadhaar_ekyc_done", val)}
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-[hsl(var(--text-primary))]">
              Bank Account Exists
            </label>
            <TogglePill
              value={watchedValues.bank_account}
              onChange={(val) => setValue("bank_account", val)}
            />
          </div>

          <div className="pt-4 border-t border-[hsl(var(--border))]">
            <p className="text-sm font-semibold text-[hsl(var(--text-muted))] mb-4">
              Disqualifier Check
            </p>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[hsl(var(--text-primary))]">
                    Income Tax Payer?
                  </label>
                  <Tooltip text="Are you registered as an income tax payer?" />
                </div>
                <TogglePill
                  value={watchedValues.income_tax_payer}
                  onChange={(val) => setValue("income_tax_payer", val)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[hsl(var(--text-primary))]">
                    Government Employee?
                  </label>
                  <Tooltip text="Are you currently employed by the government?" />
                </div>
                <TogglePill
                  value={watchedValues.govt_employee}
                  onChange={(val) => setValue("govt_employee", val)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[hsl(var(--text-primary))]">
                    Monthly Pension &gt; ₹10,000?
                  </label>
                  <Tooltip text="Do you receive a monthly pension exceeding ₹10,000?" />
                </div>
                <TogglePill
                  value={watchedValues.pension_above_10k}
                  onChange={(val) => setValue("pension_above_10k", val)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[hsl(var(--text-primary))]">
                    Practicing Professional?
                  </label>
                  <Tooltip text="Doctors, lawyers, CAs, engineers registered with professional bodies" />
                </div>
                <TogglePill
                  value={watchedValues.practicing_professional}
                  onChange={(val) => setValue("practicing_professional", val)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[hsl(var(--text-primary))]">
                    Constitutional Post Holder?
                  </label>
                  <Tooltip text="Do you hold any constitutional position?" />
                </div>
                <TogglePill
                  value={watchedValues.constitutional_post_holder}
                  onChange={(val) => setValue("constitutional_post_holder", val)}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <motion.button
        type="submit"
        disabled={isLoading}
        whileHover={!isLoading ? { scale: 1.02 } : {}}
        whileTap={!isLoading ? { scale: 0.98 } : {}}
        className="w-full px-8 py-4 rounded-lg bg-[hsl(var(--accent))] text-white font-semibold flex items-center justify-center gap-2 shadow-lg hover:shadow-[0_0_30px_hsl(var(--accent-glow)/0.3)] transition-shadow disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
            />
            Analyzing with 5 AI agents...
          </>
        ) : (
          <>
            <Search className="w-5 h-5" />
            Analyze Eligibility
          </>
        )}
      </motion.button>
    </form>
  );
}
