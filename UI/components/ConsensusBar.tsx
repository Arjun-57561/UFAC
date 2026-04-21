"use client";

import { motion } from "framer-motion";
import { useCountUp } from "@/hooks/useCountUp";
import { useEffect, useState } from "react";

interface ConsensusBarProps {
  label: string;
  value: number; // 0-1
  color: string;
  icon: string;
  delay?: number;
}

export function ConsensusBar({
  label,
  value,
  color,
  icon,
  delay = 0,
}: ConsensusBarProps) {
  const [mounted, setMounted] = useState(false);
  const percentage = Math.round(value * 100);
  const count = useCountUp(mounted ? percentage : 0, 1000);

  useEffect(() => {
    const timer = setTimeout(() => setMounted(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">{icon}</span>
          <span className="text-sm font-medium text-[hsl(var(--text-primary))]">
            {label}
          </span>
        </div>
        <span className="text-sm font-bold text-[hsl(var(--text-primary))]">
          {count}%
        </span>
      </div>
      <div className="h-2 bg-[hsl(var(--border))] rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, delay: delay / 1000, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
