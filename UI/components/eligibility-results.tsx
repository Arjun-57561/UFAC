'use client';

import { motion } from 'framer-motion';

export interface EligibilityResult {
  isEligible: boolean;
  fullName: string;
  reasons: string[];
  eligibilityPercentage: number;
  ufacResponse?: any;
}

interface EligibilityResultsProps {
  result: EligibilityResult;
  onNewCheck: () => void;
}

export function EligibilityResults({ result, onNewCheck }: EligibilityResultsProps) {
  return (
    <div className="p-8 rounded-lg border border-border bg-card">
      <div className="text-center mb-8">
        <div className={`text-6xl mb-4`}>{result.isEligible ? '✅' : '❌'}</div>
        <h2 className="text-3xl font-bold text-foreground mb-2">
          {result.isEligible ? 'Eligible!' : 'Not Eligible'}
        </h2>
        <p className="text-foreground/70">
          Assessment result for <strong>{result.fullName}</strong>
        </p>
        <div className="mt-4 text-2xl font-bold text-accent">
          {result.eligibilityPercentage}% Confidence
        </div>
      </div>
      <div className="space-y-2 mb-8">
        {result.reasons.map((reason, i) => (
          <div key={i} className="text-sm text-foreground/80 p-2 rounded bg-muted">
            {reason}
          </div>
        ))}
      </div>
      <button
        onClick={onNewCheck}
        className="w-full py-3 px-6 rounded-lg bg-primary text-primary-foreground font-semibold hover:opacity-90 transition-opacity"
      >
        Check Another
      </button>
    </div>
  );
}
