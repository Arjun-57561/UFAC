"use client"
import { useState, useEffect } from "react"

type Status = "online" | "offline" | "checking"

export function useBackendStatus() {
  const [status, setStatus] = useState<Status>("checking")
  const [ragActive, setRagActive] = useState(false)

  const check = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(
        `${apiUrl}/health`,
        { signal: AbortSignal.timeout(5000) }
      )
      if (res.ok) {
        const data = await res.json()
        setStatus("online")
        setRagActive(data.rag?.initialized === true)
      } else {
        setStatus("offline")
      }
    } catch {
      setStatus("offline")
    }
  }

  useEffect(() => {
    check()
    const interval = setInterval(check, 30000)
    return () => clearInterval(interval)
  }, [])

  return { status, ragActive }
}
