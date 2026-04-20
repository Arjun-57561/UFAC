"use client";

import { motion, useInView } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Brain, Zap, Activity } from "lucide-react";
import { PageTransition } from "@/components/PageTransition";
import { useCountUp } from "@/hooks/useCountUp";
import { useRef, useState, useEffect } from "react";

function FloatingParticles() {
  const [particles, setParticles] = useState<
    { id: number; size: number; left: string; top: string; duration: number; delay: number }[]
  >([]);

  useEffect(() => {
    setParticles(
      Array.from({ length: 15 }, (_, i) => ({
        id: i,
        size: Math.random() * 40 + 20,
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        duration: Math.random() * 4 + 8,
        delay: Math.random() * 2,
      }))
    );
  }, []);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="particle absolute"
          style={{
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            left: particle.left,
            top: particle.top,
            animationDuration: `${particle.duration}s`,
            animationDelay: `${particle.delay}s`,
          }}
        />
      ))}
    </div>
  );
}

function StatCard({
  icon: Icon,
  value,
  label,
}: {
  icon: any;
  value: number;
  label: string;
}) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });
  const count = useCountUp(isInView ? value : 0, 1500);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center gap-3 p-6 rounded-xl bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))]"
    >
      <Icon className="w-8 h-8 text-[hsl(var(--accent))]" />
      <div className="text-3xl font-bold text-[hsl(var(--text-primary))]">
        {count}
      </div>
      <div className="text-sm text-[hsl(var(--text-muted))]">{label}</div>
    </motion.div>
  );
}

export default function HomePage() {
  return (
    <PageTransition>
      <div className="relative min-h-[calc(100vh-4rem)] flex items-center justify-center overflow-hidden">
        <FloatingParticles />

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full border-2 border-[hsl(var(--accent))] bg-[hsl(var(--accent)/0.1)]"
            >
              <motion.span
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="text-2xl"
              >
                🌾
              </motion.span>
              <span className="text-sm font-medium text-[hsl(var(--accent))]">
                PM-KISAN Eligibility Engine
              </span>
            </motion.div>

            {/* Main Title */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold tracking-tight"
              style={{
                background:
                  "linear-gradient(to right, hsl(var(--accent)), hsl(142 71% 65%))",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              Uncertainity First Agent Coucil
            </motion.h1>

            {/* Subtitle */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="flex items-center justify-center gap-3 text-xl md:text-2xl text-[hsl(var(--text-secondary))]"
            >
              <span>Unknown</span>
              <motion.span
                animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="text-[hsl(var(--accent))]"
              >
                ·
              </motion.span>
              <span>Fact</span>
              <motion.span
                animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                className="text-[hsl(var(--accent))]"
              >
                ·
              </motion.span>
              <span>Assumption</span>
              <motion.span
                animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity, delay: 1 }}
                className="text-[hsl(var(--accent))]"
              >
                ·
              </motion.span>
              <span>Confidence</span>
            </motion.div>

            {/* Description with typewriter effect */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="text-lg text-[hsl(var(--text-muted))] max-w-2xl mx-auto"
            >
              AI-powered multi-agent reasoning for PM-KISAN agricultural
              eligibility assessment. Get instant clarity on your eligibility
              status.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Link href="/check">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="group px-8 py-4 rounded-lg bg-[hsl(var(--accent))] text-white font-semibold flex items-center gap-2 shadow-lg hover:shadow-[0_0_30px_hsl(var(--accent-glow)/0.3)] transition-shadow"
                >
                  Check My Eligibility
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </motion.button>
              </Link>
              <Link href="/flow">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-8 py-4 rounded-lg border-2 border-[hsl(var(--accent))] text-[hsl(var(--accent))] font-semibold hover:bg-[hsl(var(--accent)/0.1)] transition-colors"
                >
                  View Agent Flow
                </motion.button>
              </Link>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.8 }}
              className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-16"
            >
              <StatCard icon={Brain} value={5} label="AI Agents" />
              <StatCard icon={Zap} value={15} label="LLM Calls" />
              <StatCard icon={Activity} value={100} label="Real-time Analysis" />
            </motion.div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
