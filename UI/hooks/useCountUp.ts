"use client"
import { useState, useEffect, useRef } from "react"

export function useCountUp(target: number, duration: number = 1500) {
  const [current, setCurrent] = useState(0)
  const frameRef = useRef<number>()
  const startRef = useRef<number>()

  useEffect(() => {
    setCurrent(0)
    const animate = (timestamp: number) => {
      if (!startRef.current) startRef.current = timestamp
      const progress = Math.min(
        (timestamp - startRef.current) / duration, 1
      )
      const eased = 1 - Math.pow(1 - progress, 3)  // ease-out-cubic
      setCurrent(Math.round(eased * target))
      if (progress < 1) frameRef.current = requestAnimationFrame(animate)
    }
    frameRef.current = requestAnimationFrame(animate)
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
      startRef.current = undefined
    }
  }, [target, duration])

  return current
}
