"use client";

import { motion } from "framer-motion";

interface TogglePillProps {
  value: boolean | undefined;
  onChange: (value: boolean) => void;
  yesLabel?: string;
  noLabel?: string;
}

export function TogglePill({
  value,
  onChange,
  yesLabel = "YES",
  noLabel = "NO",
}: TogglePillProps) {
  return (
    <div className="flex gap-2">
      <motion.button
        type="button"
        onClick={() => onChange(true)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className={`px-6 py-2 rounded-full font-medium transition-all ${
          value === true
            ? "bg-green-500 text-white border-2 border-green-500"
            : "border-2 border-[hsl(var(--border))] text-[hsl(var(--text-muted))] hover:border-[hsl(var(--accent))]"
        }`}
      >
        {yesLabel}
      </motion.button>
      <motion.button
        type="button"
        onClick={() => onChange(false)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className={`px-6 py-2 rounded-full font-medium transition-all ${
          value === false
            ? "bg-red-500 text-white border-2 border-red-500"
            : "border-2 border-[hsl(var(--border))] text-[hsl(var(--text-muted))] hover:border-[hsl(var(--accent))]"
        }`}
      >
        {noLabel}
      </motion.button>
    </div>
  );
}
