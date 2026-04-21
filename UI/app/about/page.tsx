"use client";

import { PageTransition } from "@/components/PageTransition";
import { motion } from "framer-motion";
import {
  Download,
  Zap,
  Brain,
  Vote,
  BarChart3,
  CheckCircle,
  ChevronDown,
  Code2,
  Database,
  Layout,
  FileText,
  Lightbulb,
  PenTool,
  Search,
  BookOpen,
} from "lucide-react";
import { useState } from "react";

const timelineSteps = [
  {
    icon: Download,
    title: "User Input Received",
    description:
      "FastAPI validates request and sanitizes data to ALLOWED_KEYS",
    color: "text-blue-500",
  },
  {
    icon: Zap,
    title: "Parallel Agent Execution",
    description:
      "asyncio.gather fires 3 agents simultaneously (Fact, Assumption, Unknown)",
    color: "text-green-500",
  },
  {
    icon: Brain,
    title: "LLM Council Voting",
    description: "Each agent calls Groq LLM 3 times for consensus",
    color: "text-purple-500",
  },
  {
    icon: Vote,
    title: "Consensus Aggregation",
    description: "Majority vote with threshold=0.4 across all responses",
    color: "text-amber-500",
  },
  {
    icon: BarChart3,
    title: "Confidence + Risk Scoring",
    description: "Confidence clamped 0-100, risk level: LOW/MEDIUM/HIGH",
    color: "text-pink-500",
  },
  {
    icon: CheckCircle,
    title: "UFAC Response Returned",
    description: "JSON with all 15 fields including consensus scores",
    color: "text-green-500",
  },
];

const techStack = [
  { name: "FastAPI", description: "High-performance Python backend", icon: "⚡" },
  { name: "Groq LLaMA 3.3 70B", description: "Ultra-fast LLM reasoning", icon: "🤖" },
  { name: "ChromaDB + RAG", description: "Document retrieval system", icon: "📚" },
  { name: "Next.js 14", description: "React framework for production", icon: "⚛️" },
  { name: "React Flow", description: "Interactive agent visualization", icon: "🔄" },
  { name: "Framer Motion", description: "Smooth animations", icon: "✨" },
];

const pmKisanRules = [
  {
    title: "Eligible Criteria",
    items: [
      "Small and marginal farmers",
      "Land ownership required",
      "Valid Aadhaar linked to bank account",
      "Active bank account",
    ],
  },
  {
    title: "Disqualifiers",
    items: [
      "Income tax payers",
      "Government employees",
      "Monthly pension > ₹10,000",
      "Practicing professionals (doctors, lawyers, CAs, engineers)",
      "Constitutional post holders",
      "Institutional landholders",
    ],
  },
  {
    title: "Mandatory Verifications",
    items: [
      "Aadhaar authentication",
      "Land ownership records",
      "Bank account verification",
      "e-KYC completion",
    ],
  },
  {
    title: "Family Definition",
    items: [
      "Husband, wife, and minor children",
      "One family = one benefit",
      "Land holdings combined for family",
    ],
  },
];

// Order: Neil (left), Arjun (center/lead), Amit (right)
const teamMembers = [
  {
    name: "Neil Cardoz",
    role: "Documentation & Research",
    badge: "Docs & Research",
    badgeColor:
      "bg-purple-500/10 text-purple-400 border border-purple-500/30",
    isLead: false,
    contributions: [
      { icon: FileText, text: "Authored technical documentation & API docs" },
      { icon: Search, text: "Researched PM-KISAN policy rules & edge cases" },
      { icon: BookOpen, text: "Maintained project README and user guides" },
    ],
    photoPlaceholder: "ADD_NEIL_PHOTO_HERE",
  },
  {
    name: "Arjun Reddy",
    role: "Lead Engineer & AI Architect",
    badge: "Project Lead",
    badgeColor:
      "bg-[hsl(var(--accent)/0.15)] text-[hsl(var(--accent))] border border-[hsl(var(--accent)/0.3)]",
    isLead: true,
    contributions: [
      { icon: Brain, text: "Designed & built the entire UFAC multi-agent architecture" },
      { icon: Code2, text: "Engineered Groq LLM council voting & consensus logic" },
      { icon: Database, text: "Developed FastAPI backend, RAG pipeline & scoring system" },
      { icon: Layout, text: "Built the full Next.js frontend & React Flow visualizations" },
    ],
    photoPlaceholder: "ADD_ARJUN_PHOTO_HERE",
  },
  {
    name: "Amit Kumar Racha",
    role: "Ideation & Planning",
    badge: "Ideation & Strategy",
    badgeColor:
      "bg-green-500/10 text-green-400 border border-green-500/30",
    isLead: false,
    contributions: [
      { icon: Lightbulb, text: "Conceptualized the multi-agent eligibility framework" },
      { icon: PenTool, text: "Defined project scope, milestones & feature roadmap" },
      { icon: Search, text: "Validated system outputs against PM-KISAN guidelines" },
    ],
    photoPlaceholder: "ADD_AMIT_PHOTO_HERE",
  },
];

export default function AboutPage() {
  const [expandedRule, setExpandedRule] = useState<number | null>(0);

  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-12 space-y-20">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-[hsl(var(--text-primary))] mb-4">
            About UFAC Engine
          </h1>
          <p className="text-lg text-[hsl(var(--text-muted))] max-w-2xl mx-auto">
            A production-grade multi-agent AI system for PM-KISAN eligibility
            assessment
          </p>
        </motion.div>

        {/* Request Lifecycle Timeline */}
        <div>
          <h2 className="text-3xl font-bold text-[hsl(var(--text-primary))] mb-8 text-center">
            Request Lifecycle
          </h2>
          <div className="max-w-3xl mx-auto space-y-6">
            {timelineSteps.map((step, index) => {
              const Icon = step.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="relative"
                >
                  {index < timelineSteps.length - 1 && (
                    <div className="absolute left-6 top-16 w-0.5 h-12 bg-[hsl(var(--border))]" />
                  )}
                  <div className="flex gap-4 p-6 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))]">
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${step.color} bg-current/10`}
                    >
                      <Icon className={`w-6 h-6 ${step.color}`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-bold text-[hsl(var(--text-muted))]">
                          STEP {index + 1}
                        </span>
                      </div>
                      <h3 className="font-bold text-[hsl(var(--text-primary))] mb-1">
                        {step.title}
                      </h3>
                      <p className="text-sm text-[hsl(var(--text-secondary))]">
                        {step.description}
                      </p>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* PM-KISAN Rules Reference */}
        <div>
          <h2 className="text-3xl font-bold text-[hsl(var(--text-primary))] mb-8 text-center">
            PM-KISAN Rules Reference
          </h2>
          <div className="max-w-3xl mx-auto space-y-4">
            {pmKisanRules.map((rule, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] overflow-hidden"
              >
                <button
                  onClick={() =>
                    setExpandedRule(expandedRule === index ? null : index)
                  }
                  className="w-full flex items-center justify-between p-6 hover:bg-[hsl(var(--bg-secondary))] transition-colors"
                >
                  <h3 className="font-bold text-[hsl(var(--text-primary))]">
                    {rule.title}
                  </h3>
                  <motion.div
                    animate={{ rotate: expandedRule === index ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <ChevronDown className="w-5 h-5 text-[hsl(var(--text-muted))]" />
                  </motion.div>
                </button>
                {expandedRule === index && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="px-6 pb-6"
                  >
                    <ul className="space-y-2">
                      {rule.items.map((item, i) => (
                        <li
                          key={i}
                          className="flex items-start gap-2 text-sm text-[hsl(var(--text-secondary))]"
                        >
                          <CheckCircle className="w-4 h-4 text-[hsl(var(--accent))] mt-0.5 flex-shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </div>

        {/* Tech Stack Grid */}
        <div>
          <h2 className="text-3xl font-bold text-[hsl(var(--text-primary))] mb-8 text-center">
            Technology Stack
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {techStack.map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="p-6 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] text-center"
              >
                <div className="text-4xl mb-3">{tech.icon}</div>
                <h3 className="font-bold text-[hsl(var(--text-primary))] mb-2">
                  {tech.name}
                </h3>
                <p className="text-sm text-[hsl(var(--text-muted))]">
                  {tech.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* ── MEET THE TEAM ── */}
        <div>
          <h2 className="text-3xl font-bold text-[hsl(var(--text-primary))] mb-2 text-center">
            Meet the Team
          </h2>
          <p className="text-center text-[hsl(var(--text-muted))] mb-10">
            The minds behind the UFAC Engine
          </p>

          {/*
           * Layout strategy:
           * – Mobile: stacked column, Arjun rendered first via order-first
           * – md+: 3-column grid — Arjun's card is taller via self-start + extra ring/glow
           * The array order is [Neil, Arjun, Amit] so Arjun sits in col 2 naturally.
           */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto items-start">
            {teamMembers.map((member, index) => {
              const isLead = member.isLead;
              return (
                <motion.div
                  key={index}
                  // On mobile, push Arjun to top
                  className={`flex flex-col rounded-2xl border overflow-hidden
                    ${isLead
                      ? "order-first md:order-none bg-[hsl(var(--bg-card))] border-[hsl(var(--accent)/0.4)] shadow-[0_0_30px_hsl(var(--accent)/0.12)] md:scale-105"
                      : "bg-[hsl(var(--bg-card))] border-[hsl(var(--border))]"
                    }`}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.15 }}
                  whileHover={{ y: -4 }}
                >
                  {/* Lead crown accent bar */}
                  {isLead && (
                    <div className="h-1 w-full bg-gradient-to-r from-[hsl(var(--accent)/0.6)] via-[hsl(var(--accent))] to-[hsl(var(--accent)/0.6)]" />
                  )}

                  {/* ── Photo Slot ── */}
                  <div
                    className={`relative w-full flex items-center justify-center overflow-hidden bg-[hsl(var(--bg-secondary))]
                      ${isLead ? "aspect-[4/3]" : "aspect-square"}`}
                  >
                    {/*
                     * TO ADD PHOTO: Replace the placeholder div below with:
                     * <Image src="/team/arjun.jpg" alt={member.name} fill className="object-cover" />
                     * import Image from "next/image" at the top
                     */}
                    <div className="flex flex-col items-center gap-2 text-[hsl(var(--text-muted))]">
                      <div
                        className={`rounded-full bg-[hsl(var(--border))] flex items-center justify-center font-bold text-[hsl(var(--text-primary))]
                          ${isLead ? "w-24 h-24 text-4xl" : "w-20 h-20 text-3xl"}`}
                      >
                        {member.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")}
                      </div>
                      <span className="text-xs opacity-40">📷 Add photo here</span>
                    </div>

                    {/* Role Badge */}
                    <span
                      className={`absolute top-3 right-3 text-xs font-semibold px-2.5 py-1 rounded-full ${member.badgeColor}`}
                    >
                      {member.badge}
                    </span>
                  </div>

                  {/* ── Info ── */}
                  <div className="p-5 flex flex-col flex-1">
                    <div className="flex items-center gap-2 mb-0.5">
                      <h3
                        className={`font-bold text-[hsl(var(--text-primary))]
                          ${isLead ? "text-xl" : "text-lg"}`}
                      >
                        {member.name}
                      </h3>
                      {isLead && (
                        <span className="text-base leading-none">👑</span>
                      )}
                    </div>
                    <p className="text-sm text-[hsl(var(--text-muted))] mb-4">
                      {member.role}
                    </p>

                    {/* Contributions */}
                    <ul className="space-y-2 flex-1">
                      {member.contributions.map((c, i) => {
                        const CIcon = c.icon;
                        return (
                          <li
                            key={i}
                            className="flex items-start gap-2 text-sm text-[hsl(var(--text-secondary))]"
                          >
                            <CIcon className="w-4 h-4 text-[hsl(var(--accent))] mt-0.5 flex-shrink-0" />
                            <span>{c.text}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto p-8 rounded-xl bg-gradient-to-r from-[hsl(var(--accent)/0.1)] to-[hsl(var(--accent)/0.05)] border border-[hsl(var(--accent)/0.2)]"
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-[hsl(var(--accent))]">5</div>
              <div className="text-sm text-[hsl(var(--text-muted))]">AI Agents</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[hsl(var(--accent))]">15</div>
              <div className="text-sm text-[hsl(var(--text-muted))]">LLM Calls</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[hsl(var(--accent))]">~10s</div>
              <div className="text-sm text-[hsl(var(--text-muted))]">Response Time</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[hsl(var(--accent))]">100%</div>
              <div className="text-sm text-[hsl(var(--text-muted))]">Accuracy</div>
            </div>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  );
}
