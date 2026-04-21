"use client";

import { useState } from "react";
import { PageTransition } from "@/components/PageTransition";
import { EligibilityForm } from "@/components/EligibilityForm";
import { ResultsPanel } from "@/components/ResultsPanel";
import { Wheat } from "lucide-react";
import { motion } from "framer-motion";
import {
  checkEligibility,
  type EligibilityFormData,
  type UFACResponse,
  APIError,
} from "@/lib/api";

export default function CheckPage() {
  const [result, setResult] = useState<{
    response: UFACResponse;
    responseTime: number;
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: EligibilityFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      // Map form data to API format
      const apiData = {
        occupation: data.occupation,
        land_ownership: data.land_ownership,
        aadhaar_linked: data.aadhaar_linked,
        aadhaar_ekyc_done: data.aadhaar_ekyc_done,
        bank_account: data.bank_account,
        annual_income: data.annual_income,
        income_tax_payer: data.income_tax_payer,
        govt_employee: data.govt_employee,
        pension_above_10k: data.pension_above_10k,
        practicing_professional: data.practicing_professional,
        constitutional_post_holder: data.constitutional_post_holder,
        state: data.state,
        district: data.district,
      };

      const { data: response, responseTime } = await checkEligibility(apiData);
      setResult({ response, responseTime });

      // Scroll to results on mobile
      if (window.innerWidth < 768) {
        setTimeout(() => {
          window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
        }, 100);
      }
    } catch (err) {
      if (err instanceof APIError) {
        if (err.status === 0) {
          setError(
            "⚠️ Cannot connect to UFAC Engine. Make sure the backend is running on port 8000."
          );
        } else if (err.status === 500) {
          setError("Something went wrong during analysis. Please try again.");
        } else if (err.status === 503) {
          setError("AI service is temporarily unavailable.");
        } else {
          setError(err.message);
        }
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Wheat className="w-8 h-8 text-[hsl(var(--accent))]" />
            <h1 className="text-4xl font-bold text-[hsl(var(--text-primary))]">
              Check PM-KISAN Eligibility
            </h1>
          </div>
          <p className="text-[hsl(var(--text-muted))] max-w-2xl mx-auto">
            Fill in your details below to get an AI-powered assessment of your
            PM-KISAN eligibility status
          </p>
        </motion.div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-4xl mx-auto mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500 text-red-500"
          >
            <div className="flex items-start gap-2">
              <span className="text-xl">⚠️</span>
              <div>
                <p className="font-semibold">Error</p>
                <p className="text-sm">{error}</p>
                <button
                  onClick={() => setError(null)}
                  className="mt-2 text-sm underline hover:no-underline"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Left: Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:sticky lg:top-24 lg:self-start"
          >
            <div className="p-8 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))]">
              <div className="flex items-center gap-2 mb-6">
                <Wheat className="w-5 h-5 text-[hsl(var(--accent))]" />
                <h2 className="text-2xl font-bold text-[hsl(var(--text-primary))]">
                  Your Information
                </h2>
              </div>
              <EligibilityForm onSubmit={handleSubmit} isLoading={isLoading} />
            </div>
          </motion.div>

          {/* Right: Results */}
          {result && (
            <div>
              <ResultsPanel
                response={result.response}
                responseTime={result.responseTime}
              />
            </div>
          )}

          {/* Placeholder when no results */}
          {!result && !isLoading && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="hidden lg:flex items-center justify-center p-12 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] border-dashed"
            >
              <div className="text-center space-y-4">
                <div className="text-6xl">📊</div>
                <p className="text-[hsl(var(--text-muted))]">
                  Your results will appear here
                </p>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </PageTransition>
  );
}
