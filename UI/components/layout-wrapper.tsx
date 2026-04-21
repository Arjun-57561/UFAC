'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Navbar } from './navbar';
import { Footer } from './footer';

interface LayoutWrapperProps {
  children: ReactNode;
  hideNavFooter?: boolean;
}

export function LayoutWrapper({ children, hideNavFooter = false }: LayoutWrapperProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="flex flex-col min-h-screen"
    >
      {!hideNavFooter && <Navbar />}
      <main className="flex-1">
        {children}
      </main>
      {!hideNavFooter && <Footer />}
    </motion.div>
  );
}
