'use client';

import { useState, useCallback } from 'react';

export interface UFACResponse {
  answer: string;
  confidence: number;
  known_facts: string[];
  assumptions: string[];
  unknowns: string[];
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  next_steps: string[];
  fact_consensus: number;
  assumption_consensus: number;
  unknown_consensus: number;
  confidence_consensus: number;
  decision_consensus: number;
}

export interface AssessmentInput {
  occupation?: string;
  land_ownership?: string;
  aadhaar_linked?: boolean;
  aadhaar_ekyc_done?: boolean;
  bank_account?: boolean;
  annual_income?: number;
  income_tax_payer?: boolean;
  govt_employee?: boolean;
  pension_above_10k?: boolean;
  practicing_professional?: boolean;
  constitutional_post_holder?: boolean;
  state?: string;
  district?: string;
}

export function useUFACAssessment() {
  const [response, setResponse] = useState<UFACResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const assess = useCallback(async (input: AssessmentInput) => {
    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(input),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data: UFACResponse = await response.json();
      setResponse(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      console.error('UFAC Assessment Error:', errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResponse(null);
    setError(null);
  }, []);

  return {
    response,
    isLoading,
    error,
    assess,
    reset,
  };
}
