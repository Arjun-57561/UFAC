"use client";

import { motion } from "framer-motion";
import { UFACResponse } from "@/lib/api";
import { AnswerBanner } from "./AnswerBanner";
import { ConfidenceRing } from "./ConfidenceRing";
import { ConsensusBar } from "./ConsensusBar";
import { StaggerList } from "./StaggerList";
import {
  CheckCircle,
  AlertTriangle,
  HelpCircle,
  ListOrdered,
  Shield,
  AlertOctagon,
  ShieldCheck,
  Clock,
} from "lucide-react";
import { useState } from "react";

interface ResultsPanelProps {
  response: UFACResponse;
  responseTime: number;
}

export function ResultsPanel({ response, responseTime }: ResultsPanelProps) {
  const [expandedSections, setExpandedSections] = useState({
    facts: true,
    assumptions: true,
    unknowns: true,
    steps: true,
  });

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  const totalFields = 13;
  const submittedFields =
    (response.known_facts?.length || 0) +
    (response.assumptions?.length || 0);
  const dataCompleteness = Math.min(
    Math.round((submittedFields / totalFields) * 100),
    100
  );

  const riskConfig = {
    LOW: {
      bg: "bg-green-500/10",
      text: "text-green-500",
      icon: ShieldCheck,
      pulse: false,
    },
    MEDIUM: {
      bg: "bg-amber-500/10",
      text: "text-amber-500",
      icon: AlertTriangle,
      pulse: false,
    },
    HIGH: {
      bg: "bg-red-500/10",
      text: "text-red-500",
      icon: AlertOctagon,
      pulse: true,
    },
  };

  const risk = riskConfig[response.risk_level];
  const RiskIcon = risk.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: 30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Real-time Status Indicator */}
      <div className="flex items-center justify-end gap-4 text-xs text-[hsl(var(--text-muted))]">
        <div className="flex items-center gap-1">
          <Clock className="w-3 h-3" />
          Response time: {(responseTime / 1000).toFixed(2)}s
        </div>
        <div>🤖 Model: llama-3.3-70b-versatile</div>
        <div>📚 RAG: Active</div>
      </div>

      {/* Answer Banner */}
      <AnswerBanner answer={response.answer} />

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Confidence Score */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="flex items-center justify-center p-6 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))]"
        >
          <ConfidenceRing confidence={response.confidence} />
        </motion.div>

        {/* Risk Level */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className={`flex flex-col items-center justify-center p-6 rounded-xl ${risk.bg} border border-[hsl(var(--border))]`}
        >
          <motion.div
            animate={risk.pulse ? { scale: [1, 1.1, 1] } : {}}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <RiskIcon className={`w-12 h-12 ${risk.text} mb-2`} />
          </motion.div>
          <div className={`text-2xl font-bold ${risk.text}`}>
            {response.risk_level}
          </div>
          <div className="text-xs text-[hsl(var(--text-muted))]">Risk Level</div>
        </motion.div>

        {/* Data Completeness */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="flex flex-col justify-center p-6 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))]"
        >
          <div className="text-3xl font-bold text-[hsl(var(--text-primary))] mb-2">
            {dataCompleteness}%
          </div>
          <div className="text-xs text-[hsl(var(--text-muted))] mb-3">
            Data Completeness
          </div>
          <div className="h-2 bg-[hsl(var(--border))] rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-[hsl(var(--accent))] rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${dataCompleteness}%` }}
              transition={{ duration: 1, delay: 0.5 }}
            />
          </div>
        </motion.div>
      </div>

      {/* Results Accordion */}
      <div className="space-y-4">
        {/* Known Facts */}
        <div className="rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] overflow-hidden">
          <button
            onClick={() => toggleSection("facts")}
            className="w-full flex items-center justify-between p-4 hover:bg-[hsl(var(--bg-secondary))] transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-1 h-8 bg-green-500 rounded-full" />
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="font-semibold text-[hsl(var(--text-primary))]">
                Known Facts
              </span>
              <span className="px-2 py-1 rounded-full bg-green-500/10 text-green-500 text-xs font-medium">
                {response.known_facts.length}
              </span>
            </div>
            <motion.div
              animate={{ rotate: expandedSections.facts ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              ▼
            </motion.div>
          </button>
          {expandedSections.facts && (
            <div className="p-4 pt-0">
              <StaggerList className="space-y-2">
                {response.known_facts.map((fact, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-[hsl(var(--text-secondary))]">
                      {fact}
                    </span>
                  </div>
                ))}
              </StaggerList>
            </div>
          )}
        </div>

        {/* Assumptions */}
        <div className="rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] overflow-hidden">
          <button
            onClick={() => toggleSection("assumptions")}
            className="w-full flex items-center justify-between p-4 hover:bg-[hsl(var(--bg-secondary))] transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-1 h-8 bg-amber-500 rounded-full" />
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              <span className="font-semibold text-[hsl(var(--text-primary))]">
                Assumptions Made
              </span>
              <span className="px-2 py-1 rounded-full bg-amber-500/10 text-amber-500 text-xs font-medium">
                {response.assumptions.length}
              </span>
            </div>
            <motion.div
              animate={{ rotate: expandedSections.assumptions ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              ▼
            </motion.div>
          </button>
          {expandedSections.assumptions && (
            <div className="p-4 pt-0">
              <StaggerList className="space-y-2">
                {response.assumptions.map((assumption, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-[hsl(var(--text-secondary))]">
                      {assumption}
                    </span>
                  </div>
                ))}
              </StaggerList>
            </div>
          )}
        </div>

        {/* Missing Information */}
        <div className="rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] overflow-hidden">
          <button
            onClick={() => toggleSection("unknowns")}
            className="w-full flex items-center justify-between p-4 hover:bg-[hsl(var(--bg-secondary))] transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-1 h-8 bg-red-500 rounded-full" />
              <HelpCircle className="w-5 h-5 text-red-500" />
              <span className="font-semibold text-[hsl(var(--text-primary))]">
                Missing Information
              </span>
              <span className="px-2 py-1 rounded-full bg-red-500/10 text-red-500 text-xs font-medium">
                {response.unknowns.length}
              </span>
            </div>
            <motion.div
              animate={{ rotate: expandedSections.unknowns ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              ▼
            </motion.div>
          </button>
          {expandedSections.unknowns && (
            <div className="p-4 pt-0">
              {response.unknowns.length === 0 ? (
                <div className="flex items-center gap-2 text-green-500">
                  <CheckCircle className="w-4 h-4" />
                  <span className="text-sm">✨ No missing information!</span>
                </div>
              ) : (
                <StaggerList className="space-y-2">
                  {response.unknowns.map((unknown, i) => (
                    <div key={i} className="flex items-start gap-2">
                      <HelpCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-[hsl(var(--text-secondary))]">
                        {unknown}
                      </span>
                    </div>
                  ))}
                </StaggerList>
              )}
            </div>
          )}
        </div>

        {/* Next Steps */}
        <div className="rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] overflow-hidden">
          <button
            onClick={() => toggleSection("steps")}
            className="w-full flex items-center justify-between p-4 hover:bg-[hsl(var(--bg-secondary))] transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-1 h-8 bg-blue-500 rounded-full" />
              <ListOrdered className="w-5 h-5 text-blue-500" />
              <span className="font-semibold text-[hsl(var(--text-primary))]">
                Recommended Next Steps
              </span>
              <span className="px-2 py-1 rounded-full bg-blue-500/10 text-blue-500 text-xs font-medium">
                {response.next_steps.length}
              </span>
            </div>
            <motion.div
              animate={{ rotate: expandedSections.steps ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              ▼
            </motion.div>
          </button>
          {expandedSections.steps && (
            <div className="p-4 pt-0">
              <StaggerList className="space-y-3">
                {response.next_steps.map((step, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 p-3 rounded-lg bg-[hsl(var(--bg-secondary))] border border-[hsl(var(--border))]"
                  >
                    <div className="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold flex-shrink-0">
                      {i + 1}
                    </div>
                    <span className="text-sm text-[hsl(var(--text-secondary))]">
                      {step}
                    </span>
                  </div>
                ))}
              </StaggerList>
            </div>
          )}
        </div>
      </div>

      {/* Agent Consensus Panel */}
      <div className="rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] p-6 space-y-4">
        <div>
          <h3 className="font-semibold text-[hsl(var(--text-primary))] mb-1">
            AI Agent Consensus Scores
          </h3>
          <p className="text-sm text-[hsl(var(--text-muted))]">
            How strongly each agent agreed on its output
          </p>
        </div>
        <div className="space-y-4">
          <ConsensusBar
            label="Fact Agent"
            value={response.fact_consensus}
            color="hsl(var(--success))"
            icon="🔍"
            delay={0}
          />
          <ConsensusBar
            label="Assumption Agent"
            value={response.assumption_consensus}
            color="hsl(32 95% 44%)"
            icon="💭"
            delay={150}
          />
          <ConsensusBar
            label="Unknown Agent"
            value={response.unknown_consensus}
            color="hsl(0 72% 51%)"
            icon="❓"
            delay={300}
          />
          <ConsensusBar
            label="Confidence Agent"
            value={response.confidence_consensus}
            color="hsl(217 91% 60%)"
            icon="📊"
            delay={450}
          />
          <ConsensusBar
            label="Decision Agent"
            value={response.decision_consensus}
            color="hsl(271 91% 65%)"
            icon="🎯"
            delay={600}
          />
        </div>
      </div>
    </motion.div>
  );
}
