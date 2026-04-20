'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface LayoutWrapperProps {
  children: ReactNode;
}

export function LayoutWrapper({ children }: LayoutWrapperProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
