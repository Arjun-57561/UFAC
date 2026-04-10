import { z } from "zod";

// ─── Zod Schema ───────────────────────────────────────────────────────────────
export const eligibilitySchema = z.object({
  occupation: z.string().min(1, "Occupation is required"),
  land_ownership: z.enum(["yes", "no"]).optional(),
  aadhaar_linked: z.boolean().optional(),
  aadhaar_ekyc_done: z.boolean().optional(),
  bank_account: z.boolean().optional(),
  annual_income: z.number().optional(),
  income_tax_payer: z.boolean().optional(),
  govt_employee: z.boolean().optional(),
  pension_above_10k: z.boolean().optional(),
  practicing_professional: z.boolean().optional(),
  constitutional_post_holder: z.boolean().optional(),
  state: z.string().optional(),
  district: z.string().optional(),
});

export type EligibilityFormData = z.infer<typeof eligibilitySchema>;

// ─── Response Types ────────────────────────────────────────────────────────────
export interface AgentResult {
  agent: string;
  status: string;
  reasoning: string;
  confidence: number;
}

export interface UFACResponse {
  eligible: boolean;
  confidence: number;
  final_decision: string;
  summary: string;
  agents: AgentResult[];
  disqualifiers: string[];
  recommendations: string[];
  rag_sources?: string[];
}

// ─── Error Class ──────────────────────────────────────────────────────────────
export class APIError extends Error {
  constructor(public message: string, public status: number) {
    super(message);
    this.name = "APIError";
  }
}

// ─── API Base URL ─────────────────────────────────────────────────────────────
const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// ─── checkEligibility ─────────────────────────────────────────────────────────
export async function checkEligibility(
  data: EligibilityFormData
): Promise<{ data: UFACResponse; responseTime: number }> {
  const start = Date.now();
  try {
    // CORRECT
  const res = await fetch(`${API_BASE}/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const responseTime = Date.now() - start;
    if (!res.ok) {
      const text = await res.text().catch(() => res.statusText);
      throw new APIError(text, res.status);
    }
    const json: UFACResponse = await res.json();
    return { data: json, responseTime };
  } catch (err) {
    if (err instanceof APIError) throw err;
    throw new APIError("Network error – could not reach backend", 0);
  }
}

// ─── RAG Status Types ─────────────────────────────────────────────────────────
export interface RAGStatus {
  status: "ok" | "degraded" | "offline";
  documents: number;
  message: string;
}

export async function getRagStatus(): Promise<RAGStatus> {
  try {
    const res = await fetch(`${API_BASE}/rag-status`, { cache: "no-store" });
    if (!res.ok) return { status: "degraded", documents: 0, message: "Degraded" };
    return res.json();
  } catch {
    return { status: "offline", documents: 0, message: "Offline" };
  }
}
