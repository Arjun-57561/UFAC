"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Sprout, Menu, X, Github } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";
import { BackendStatus } from "./BackendStatus";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/check", label: "Check Eligibility" },
  { href: "/flow", label: "Agent Flow" },
  { href: "/about", label: "About" },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[hsl(var(--bg-primary))] border-b border-[hsl(var(--border))]"
          : "bg-[hsl(var(--bg-primary)/0.8)] backdrop-blur-md border-b border-[hsl(var(--border)/0.5)]"
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Left: Logo + Status */}
          <Link href="/" className="flex items-center gap-3 group">
            <Sprout className="w-6 h-6 text-[hsl(var(--accent))] group-hover:rotate-12 transition-transform" />
            <span className="font-bold text-lg text-[hsl(var(--text-primary))]">
              UFAC Engine
            </span>
            <BackendStatus />
          </Link>

          {/* Center: Desktop Nav Links */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className="relative text-sm font-medium transition-colors hover:text-[hsl(var(--accent))]"
                  style={{
                    color: isActive
                      ? "hsl(var(--accent))"
                      : "hsl(var(--text-secondary))",
                  }}
                >
                  {link.label}
                  {isActive && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="absolute -bottom-[21px] left-0 right-0 h-0.5 bg-[hsl(var(--accent))]"
                      transition={{ type: "spring", stiffness: 380, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>

          {/* Right: Theme Toggle + GitHub */}
          <div className="hidden md:flex items-center gap-3">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 rounded-lg bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] flex items-center justify-center hover:bg-[hsl(var(--bg-secondary))] transition-colors"
              aria-label="GitHub"
            >
              <Github className="w-5 h-5 text-[hsl(var(--text-secondary))]" />
            </a>
            <ThemeToggle />
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden w-10 h-10 rounded-lg bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] flex items-center justify-center"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="w-5 h-5 text-[hsl(var(--text-secondary))]" />
            ) : (
              <Menu className="w-5 h-5 text-[hsl(var(--text-secondary))]" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-[hsl(var(--border))] bg-[hsl(var(--bg-primary))]"
          >
            <div className="container mx-auto px-4 py-4 space-y-3">
              {navLinks.map((link) => {
                const isActive = pathname === link.href;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-4 py-2 rounded-lg transition-colors"
                    style={{
                      backgroundColor: isActive
                        ? "hsl(var(--accent) / 0.1)"
                        : "transparent",
                      color: isActive
                        ? "hsl(var(--accent))"
                        : "hsl(var(--text-secondary))",
                    }}
                  >
                    {link.label}
                  </Link>
                );
              })}
              <div className="flex items-center gap-3 px-4 pt-3 border-t border-[hsl(var(--border))]">
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-lg bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] flex items-center justify-center"
                  aria-label="GitHub"
                >
                  <Github className="w-5 h-5 text-[hsl(var(--text-secondary))]" />
                </a>
                <ThemeToggle />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
