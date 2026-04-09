"use client";

import Link from "next/link";
import { Sprout } from "lucide-react";
import { useBackendStatus } from "@/hooks/useBackendStatus";
import { useEffect, useState } from "react";
import { getRagStatus, type RAGStatus } from "@/lib/api";

export function Footer() {
  const { status } = useBackendStatus();
  const [ragStatus, setRagStatus] = useState<RAGStatus | null>(null);

  const collectionCount = ragStatus?.rag?.collection_count;

  useEffect(() => {
    const fetchRagStatus = async () => {
      try {
        const data = await getRagStatus();
        setRagStatus(data);
      } catch {
        setRagStatus(null);
      }
    };

    if (status === "online") {
      fetchRagStatus();
    }
  }, [status]);

  return (
    <footer className="border-t border-[hsl(var(--border))] bg-[hsl(var(--bg-secondary))] mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Left: Logo + Tagline */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Sprout className="w-6 h-6 text-[hsl(var(--accent))]" />
              <span className="font-bold text-lg text-[hsl(var(--text-primary))]">
                UFAC Engine
              </span>
            </div>
            <p className="text-sm text-[hsl(var(--text-muted))]">
              Multi-agent AI for PM-KISAN eligibility assessment
            </p>
          </div>

          {/* Center: Quick Links */}
          <div>
            <h3 className="font-semibold text-[hsl(var(--text-primary))] mb-3">
              Quick Links
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/"
                  className="text-sm text-[hsl(var(--text-muted))] hover:text-[hsl(var(--accent))] transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/check"
                  className="text-sm text-[hsl(var(--text-muted))] hover:text-[hsl(var(--accent))] transition-colors"
                >
                  Check Eligibility
                </Link>
              </li>
              <li>
                <Link
                  href="/flow"
                  className="text-sm text-[hsl(var(--text-muted))] hover:text-[hsl(var(--accent))] transition-colors"
                >
                  Agent Flow
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-sm text-[hsl(var(--text-muted))] hover:text-[hsl(var(--accent))] transition-colors"
                >
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Right: Backend Status */}
          <div>
            <h3 className="font-semibold text-[hsl(var(--text-primary))] mb-3">
              System Status
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    status === "online"
                      ? "bg-green-500"
                      : status === "offline"
                      ? "bg-red-500"
                      : "bg-amber-500"
                  }`}
                />
                <span className="text-[hsl(var(--text-muted))]">
                  {status === "online"
                    ? "API Online"
                    : status === "offline"
                    ? "API Offline"
                    : "Checking..."}
                </span>
              </div>
              {ragStatus?.rag && (
                <div className="text-[hsl(var(--text-muted))]">
                  📚 RAG: {collectionCount?.toLocaleString() ?? "unknown"} chunks indexed
                </div>
              )}
              <div className="text-[hsl(var(--text-muted))]">
                ⚡ Avg response: ~10s
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t border-[hsl(var(--border))] text-center text-sm text-[hsl(var(--text-muted))]">
          © 2026 UFAC Engine · BTech AIML PBL-2 Project
        </div>
      </div>
    </footer>
  );
}
