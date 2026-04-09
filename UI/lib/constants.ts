export const SITE_NAME = "UFAC";
export const SITE_DESCRIPTION =
  "Unified Farmer Assistance Checker — AI-powered PM-KISAN eligibility assessment";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const NAV_LINKS = [
  { label: "Home", href: "/" },
  { label: "Check Eligibility", href: "/check" },
  { label: "About", href: "/about" },
] as const;

export const AGENT_NAMES = [
  "Eligibility Agent",
  "Document Agent",
  "Income Agent",
  "Land Agent",
  "Compliance Agent",
] as const;

export const UFAC_AGENTS = [
  {
    id: "fact-agent",
    name: "Fact Agent",
    icon: "📋",
    batch: 1,
    description: "Extracts and verifies known facts from the input data.",
    responsibilities: [
      "Parse submitted farmer data",
      "Identify verifiable facts",
      "Cross-check with eligibility criteria",
    ],
  },
  {
    id: "assumption-agent",
    name: "Assumption Agent",
    icon: "🔍",
    batch: 1,
    description: "Identifies and evaluates assumptions based on partial data.",
    responsibilities: [
      "Flag missing information",
      "Make reasonable assumptions",
      "Assign confidence to each assumption",
    ],
  },
  {
    id: "unknown-agent",
    name: "Unknown Agent",
    icon: "❓",
    batch: 1,
    description: "Surfaces unknowns that could affect eligibility.",
    responsibilities: [
      "Identify data gaps",
      "Estimate impact of unknowns",
      "Request clarification items",
    ],
  },
  {
    id: "confidence-agent",
    name: "Confidence Agent",
    icon: "📊",
    batch: 2,
    description: "Calculates an overall confidence score for the assessment.",
    responsibilities: [
      "Aggregate fact, assumption, and unknown scores",
      "Compute weighted confidence",
      "Determine risk level",
    ],
  },
  {
    id: "decision-agent",
    name: "Decision Agent",
    icon: "⚖️",
    batch: 2,
    description: "Produces the final eligibility decision and next steps.",
    responsibilities: [
      "Apply PM-KISAN rules",
      "Generate decision rationale",
      "Recommend next steps",
    ],
  },
] as const;
