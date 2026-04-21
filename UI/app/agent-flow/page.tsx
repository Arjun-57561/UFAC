'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutWrapper } from '@/components/layout-wrapper';
import { AgentFlowVisualization } from '@/components/agent-flow-visualization';
import { useUFACAssessment, type AssessmentInput } from '@/hooks/useUFACAssessment';
import { UFAC_AGENTS } from '@/lib/constants';

export default function AgentFlowPage() {
  const { response, isLoading, error, assess, reset } = useUFACAssessment();
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  const handleRunDemo = async () => {
    const demoInput: AssessmentInput = {
      occupation: 'farmer',
      land_ownership: 'yes',
      aadhaar_linked: true,
      aadhaar_ekyc_done: true,
      bank_account: true,
      annual_income: 200000,
      income_tax_payer: false,
      govt_employee: false,
      pension_above_10k: false,
      practicing_professional: false,
      constitutional_post_holder: false,
      state: 'Punjab',
      district: 'Ludhiana',
    };

    try {
      await assess(demoInput);
    } catch (err) {
      console.error('Assessment failed:', err);
    }
  };

  const getAgentData = (agentId: string) => {
    return UFAC_AGENTS.find((a) => a.id === agentId);
  };

  const getAgentResult = (agentId: string) => {
    if (!response) return null;

    const agentKey = agentId.split('-')[0];
    switch (agentKey) {
      case 'fact':
        return {
          title: 'Known Facts',
          items: response.known_facts,
          consensus: response.fact_consensus,
        };
      case 'assumption':
        return {
          title: 'Assumptions',
          items: response.assumptions,
          consensus: response.assumption_consensus,
        };
      case 'unknown':
        return {
          title: 'Unknowns',
          items: response.unknowns,
          consensus: response.unknown_consensus,
        };
      case 'confidence':
        return {
          title: 'Confidence Analysis',
          items: [
            `Confidence Score: ${response.confidence}/100`,
            `Risk Level: ${response.risk_level}`,
            `Consensus: ${(response.confidence_consensus * 100).toFixed(0)}%`,
          ],
          consensus: response.confidence_consensus,
        };
      case 'decision':
        return {
          title: 'Next Steps',
          items: response.next_steps,
          consensus: response.decision_consensus,
        };
      default:
        return null;
    }
  };

  return (
    <LayoutWrapper>
      <div className="min-h-screen py-8 px-4">
        {/* Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            UFAC Agent Architecture
          </h1>
          <p className="text-lg text-foreground/70 max-w-2xl mx-auto">
            Visualize how 5 AI agents work in parallel to assess PM-KISAN eligibility with
            consensus voting and confidence scoring.
          </p>
        </motion.div>

        {/* Main Grid */}
        <div className="grid lg:grid-cols-4 gap-6 mb-8">
          {/* Flow Visualization */}
          <motion.div
            className="lg:col-span-3 h-[600px]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <AgentFlowVisualization response={response} isLoading={isLoading} />
          </motion.div>

          {/* Details Panel */}
          <motion.div
            className="lg:col-span-1 space-y-4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            {/* Control Panel */}
            <div className="p-6 rounded-lg bg-card border border-border">
              <h3 className="font-semibold text-foreground mb-4">Assessment Control</h3>
              <button
                onClick={handleRunDemo}
                disabled={isLoading}
                className="w-full px-4 py-2 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {isLoading ? 'Processing...' : 'Run Demo Assessment'}
              </button>
              {response && (
                <button
                  onClick={reset}
                  className="w-full mt-2 px-4 py-2 bg-border text-foreground rounded-lg font-medium hover:bg-border/80 transition-all"
                >
                  Reset
                </button>
              )}
            </div>

            {/* Agent List */}
            <div className="p-6 rounded-lg bg-card border border-border">
              <h3 className="font-semibold text-foreground mb-4">5 Agents</h3>
              <div className="space-y-2">
                {UFAC_AGENTS.map((agent) => (
                  <button
                    key={agent.id}
                    onClick={() => setSelectedAgent(agent.id)}
                    className={`w-full p-3 rounded-lg text-left transition-all ${
                      selectedAgent === agent.id
                        ? 'bg-accent text-accent-foreground'
                        : 'bg-border/50 text-foreground/70 hover:bg-border'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{agent.icon}</span>
                      <div className="flex-1">
                        <div className="font-medium text-sm">{agent.name}</div>
                        <div className="text-xs opacity-75">Batch {agent.batch}</div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Selected Agent Details */}
            {selectedAgent && (
              <motion.div
                className="p-6 rounded-lg bg-accent/10 border border-accent/20"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                {(() => {
                  const agent = getAgentData(selectedAgent);
                  const result = getAgentResult(selectedAgent);

                  if (!agent) return null;

                  return (
                    <>
                      <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                        <span className="text-2xl">{agent.icon}</span>
                        {agent.name}
                      </h4>
                      <p className="text-sm text-foreground/70 mb-4">{agent.description}</p>

                      <div className="mb-4">
                        <p className="text-xs font-semibold text-foreground/60 mb-2">
                          Responsibilities:
                        </p>
                        <ul className="space-y-1">
                          {agent.responsibilities.map((resp, idx) => (
                            <li key={idx} className="text-xs text-foreground/60 flex gap-2">
                              <span>•</span>
                              <span>{resp}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {result && response && (
                        <div className="mt-4 pt-4 border-t border-accent/20">
                          <p className="text-xs font-semibold text-foreground/60 mb-2">
                            {result.title}
                          </p>
                          <ul className="space-y-1">
                            {result.items.slice(0, 3).map((item, idx) => (
                              <li key={idx} className="text-xs text-foreground/70 flex gap-2">
                                <span>✓</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                          <div className="mt-2 text-xs text-accent font-semibold">
                            Consensus: {(result.consensus * 100).toFixed(0)}%
                          </div>
                        </div>
                      )}
                    </>
                  );
                })()}
              </motion.div>
            )}

            {/* Error Display */}
            {error && (
              <motion.div
                className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-600 text-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <p className="font-semibold mb-1">Error</p>
                <p>{error}</p>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Results Section */}
        {response && (
          <motion.div
            className="grid md:grid-cols-2 gap-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            {/* Main Result */}
            <div className="p-6 rounded-lg bg-card border border-border">
              <h3 className="font-semibold text-foreground mb-4">Eligibility Assessment</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-foreground/60 mb-2">Decision</p>
                  <p className="text-lg font-bold text-accent">{response.answer}</p>
                </div>
                <div>
                  <p className="text-sm text-foreground/60 mb-2">Confidence Score</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 bg-border rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-accent h-full transition-all"
                        style={{ width: `${response.confidence}%` }}
                      />
                    </div>
                    <span className="font-bold text-accent">{response.confidence}%</span>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-foreground/60 mb-2">Risk Level</p>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      response.risk_level === 'LOW'
                        ? 'bg-green-500/20 text-green-600'
                        : response.risk_level === 'MEDIUM'
                          ? 'bg-yellow-500/20 text-yellow-600'
                          : 'bg-red-500/20 text-red-600'
                    }`}
                  >
                    {response.risk_level}
                  </span>
                </div>
              </div>
            </div>

            {/* Consensus Scores */}
            <div className="p-6 rounded-lg bg-card border border-border">
              <h3 className="font-semibold text-foreground mb-4">Agent Consensus Scores</h3>
              <div className="space-y-3">
                {[
                  { name: 'Fact Agent', score: response.fact_consensus },
                  { name: 'Assumption Agent', score: response.assumption_consensus },
                  { name: 'Unknown Agent', score: response.unknown_consensus },
                  { name: 'Confidence Agent', score: response.confidence_consensus },
                  { name: 'Decision Agent', score: response.decision_consensus },
                ].map((item) => (
                  <div key={item.name}>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm text-foreground/70">{item.name}</span>
                      <span className="text-sm font-semibold text-accent">
                        {(item.score * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="bg-border rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-accent h-full transition-all"
                        style={{ width: `${item.score * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* Architecture Info */}
        <motion.div
          className="mt-12 p-6 rounded-lg bg-card border border-border"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h3 className="font-semibold text-foreground mb-4">UFAC Architecture</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-foreground mb-3">Batch 1 (Parallel)</h4>
              <ul className="space-y-2">
                {UFAC_AGENTS.filter((a) => a.batch === 1).map((agent) => (
                  <li key={agent.id} className="text-sm text-foreground/70 flex gap-2">
                    <span>{agent.icon}</span>
                    <span>{agent.name}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-3">Batch 2 (Parallel)</h4>
              <ul className="space-y-2">
                {UFAC_AGENTS.filter((a) => a.batch === 2).map((agent) => (
                  <li key={agent.id} className="text-sm text-foreground/70 flex gap-2">
                    <span>{agent.icon}</span>
                    <span>{agent.name}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <p className="text-sm text-foreground/60 mt-4">
            Each agent runs 3 times with different parameters. Results are aggregated using majority
            voting to produce consensus scores. This ensures robust and reliable eligibility
            assessments.
          </p>
        </motion.div>
      </div>
    </LayoutWrapper>
  );
}
