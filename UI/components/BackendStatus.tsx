"use client"
import { useBackendStatus } from "@/hooks/useBackendStatus"

export function BackendStatus() {
  const { status, ragActive } = useBackendStatus()

  const colors = {
    online: "#22c55e",
    offline: "#ef4444",
    checking: "#f59e0b"
  }

  const labels = {
    online: "Backend Online",
    offline: "Backend Offline",
    checking: "Checking..."
  }

  return (
    <div className="flex items-center gap-2 text-xs"
         title={`${labels[status]} | RAG: ${ragActive ? "Active" : "Inactive"}`}>
      <span
        style={{ backgroundColor: colors[status] }}
        className={`w-2 h-2 rounded-full ${status === "checking" ? "animate-pulse" : ""}`}
      />
      <span style={{ color: "hsl(var(--text-muted))" }} className="hidden sm:block">
        {labels[status]}
      </span>
    </div>
  )
}
