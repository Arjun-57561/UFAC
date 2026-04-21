"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

interface StaggerListProps {
  children: ReactNode[];
  className?: string;
}

export function StaggerList({ children, className }: StaggerListProps) {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.08,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, x: -10 },
    show: { opacity: 1, x: 0 },
  };

  return (
    <motion.ul
      variants={container}
      initial="hidden"
      animate="show"
      className={className}
    >
      {children.map((child, index) => (
        <motion.li key={index} variants={item}>
          {child}
        </motion.li>
      ))}
    </motion.ul>
  );
}
