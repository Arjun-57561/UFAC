"use client";

import { CheckCircle, XCircle, HelpCircle } from "lucide-react";
import { motion } from "framer-motion";

interface AnswerBannerProps {
  answer: string;
}

export function AnswerBanner({ answer }: AnswerBannerProps) {
  const answerLower = answer.toLowerCase();
  const isEligible =
    answerLower.includes("eligible") && !answerLower.includes("not eligible");
  const isIneligible = answerLower.includes("ineligible");

  const config = isEligible
    ? {
        bg: "bg-green-500/10",
        border: "border-green-500",
        text: "text-green-500",
        icon: CheckCircle,
        label: "ELIGIBLE",
      }
    : isIneligible
    ? {
        bg: "bg-red-500/10",
        border: "border-red-500",
        text: "text-red-500",
        icon: XCircle,
        label: "INELIGIBLE",
      }
    : {
        bg: "bg-amber-500/10",
        border: "border-amber-500",
        text: "text-amber-500",
        icon: HelpCircle,
        label: "UNCERTAIN",
      };

  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className={`p-6 rounded-xl ${config.bg} border-2 ${config.border}`}
    >
      <div className="flex items-center gap-4">
        <Icon className={`w-12 h-12 ${config.text}`} />
        <div className="flex-1">
          <div className={`text-2xl font-bold ${config.text} mb-1`}>
            {config.label}
          </div>
          <div className="text-[hsl(var(--text-primary))]">{answer}</div>
        </div>
      </div>
    </motion.div>
  );
}
