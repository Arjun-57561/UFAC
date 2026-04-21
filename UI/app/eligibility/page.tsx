'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutWrapper } from '@/components/layout-wrapper';
import { EligibilityForm } from '@/components/eligibility-form';
import { EligibilityResults, EligibilityResult } from '@/components/eligibility-results';
import { useUFACAssessment } from '@/hooks/useUFACAssessment';

interface FormData {
  fullName: string;
  age: number;
  landHolding: number;
  annualIncome: number;
  cropCategory: string;
}

export default function EligibilityPage() {
  const [result, setResult] = useState<EligibilityResult | null>(null);
  const [fullName, setFullName] = useState<string>('');
  const { assess, isLoading, error } = useUFACAssessment();

  const checkEligibility = async (data: FormData) => {
    try {
      setFullName(data.fullName);
      
      // Map form data to API format
      const apiInput = {
        occupation: 'farmer',
        land_ownership: data.landHolding > 0 ? 'yes' : 'no',
        annual_income: data.annualIncome,
        // Add more mappings as needed
      };

      const response = await assess(apiInput);

      // Map API response to UI result format
      const reasons: string[] = [];
      
      // Add known facts as positive reasons
      response.known_facts.forEach(fact => {
        reasons.push(`✓ ${fact}`);
      });

      // Add assumptions with warning
      response.assumptions.forEach(assumption => {
        reasons.push(`⚠ Assumption: ${assumption}`);
      });

      // Add unknowns as information needed
      response.unknowns.forEach(unknown => {
        reasons.push(`❓ Unknown: ${unknown}`);
      });

      // Add next steps
      response.next_steps.forEach(step => {
        reasons.push(`→ ${step}`);
      });

      // Determine eligibility based on answer and confidence
      const isEligible = response.answer.toLowerCase().includes('eligible') && 
                        !response.answer.toLowerCase().includes('not eligible') &&
                        response.confidence >= 0.6;

      setResult({
        isEligible,
        fullName: data.fullName,
        reasons,
        eligibilityPercentage: Math.round(response.confidence * 100),
        ufacResponse: response, // Store full response for detailed view
      });

    } catch (err) {
      console.error('Assessment failed:', err);
      setResult({
        isEligible: false,
        fullName: data.fullName,
        reasons: [
          `❌ Error: ${error || 'Failed to connect to assessment service'}`,
          '→ Please ensure the backend API is running on http://localhost:8000',
          '→ Check your internet connection and try again'
        ],
        eligibilityPercentage: 0,
      });
    }
  };

  const handleNewCheck = () => {
    setResult(null);
    setFullName('');
  };

  return (
    <LayoutWrapper>
      <div className="min-h-screen py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          {/* Header */}
          <motion.div
            className="text-center mb-12"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              PM-KISAN Eligibility Checker
            </h1>
            <p className="text-lg text-foreground/70 max-w-2xl mx-auto">
              Enter your details below to check your eligibility for the Pradhan Mantri Kisan
              Samman Nidhi Yojana scheme.
            </p>
          </motion.div>

          {result ? (
            // Results View
            <motion.div
              className="max-w-3xl mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <EligibilityResults result={result} onNewCheck={handleNewCheck} />
            </motion.div>
          ) : (
            // Form View
            <div className="grid lg:grid-cols-3 gap-8">
              {/* Form Column */}
              <motion.div
                className="lg:col-span-2"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
                <div className="p-8 rounded-lg border border-border bg-card">
                  <h2 className="text-2xl font-bold text-foreground mb-6">
                    Farmer Information
                  </h2>
                  <EligibilityForm onSubmit={checkEligibility} isLoading={isLoading} />
                </div>
              </motion.div>

              {/* Info Column */}
              <motion.div
                className="space-y-6"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <div className="p-6 rounded-lg bg-card border border-border">
                  <h3 className="font-semibold text-foreground mb-4">Eligibility Criteria</h3>
                  <ul className="space-y-3 text-sm text-foreground/70">
                    <li className="flex items-start gap-2">
                      <span className="text-accent mt-1">✓</span>
                      <span>Age: 18 years or above</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-accent mt-1">✓</span>
                      <span>Land holding: 0.01 to 2 hectares</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-accent mt-1">✓</span>
                      <span>Annual income: Up to ₹5,00,000</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-accent mt-1">✓</span>
                      <span>Active farmer engaged in agriculture</span>
                    </li>
                  </ul>
                </div>

                <div className="p-6 rounded-lg bg-accent/10 border border-accent/20">
                  <h3 className="font-semibold text-foreground mb-4">Annual Benefits</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-foreground/70">Total Annual Support:</span>
                      <span className="font-bold text-accent">₹6,000</span>
                    </div>
                    <div className="h-px bg-border"></div>
                    <div className="space-y-2 text-sm text-foreground/70">
                      <p>Paid in 3 installments:</p>
                      <ul className="space-y-1 ml-2">
                        <li>• Installment 1: ₹2,000</li>
                        <li>• Installment 2: ₹2,000</li>
                        <li>• Installment 3: ₹2,000</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          )}
        </div>
      </div>
    </LayoutWrapper>
  );
}
