"use client";

import { useState, useEffect } from "react";
import { getHealthStatus, type HealthStatus } from "@/lib/api";

export type BackendStatus = "online" | "offline" | "checking";

export function useBackendStatus() {
  const [status, setStatus] = useState<BackendStatus>("checking");
  const [healthData, setHealthData] = useState<HealthStatus | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await getHealthStatus();
        setHealthData(data);
        setStatus("online");
      } catch {
        setHealthData(null);
        setStatus("offline");
      }
    };

    // Initial check
    checkHealth();

    // Poll every 30 seconds
    const interval = setInterval(checkHealth, 30000);

    return () => clearInterval(interval);
  }, []);

  return { status, healthData };
}
