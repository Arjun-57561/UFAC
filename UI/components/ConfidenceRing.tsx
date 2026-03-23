"use client"
import { useCountUp } from "@/hooks/useCountUp"

interface Props { value: number }

export function ConfidenceRing({ value }: Props) {
  const animated = useCountUp(value, 1500)
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (animated / 100) * circumference

  const color = value >= 70
    ? "hsl(var(--success))"
    : value >= 40
    ? "hsl(var(--warning))"
    : "hsl(var(--danger))"

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="128" height="128" viewBox="0 0 128 128">
        <circle cx="64" cy="64" r={radius} fill="none"
          stroke="hsl(var(--border))" strokeWidth="10" />
        <circle cx="64" cy="64" r={radius} fill="none"
          stroke={color} strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 64 64)"
          style={{ transition: "stroke-dashoffset 0.05s linear" }}
        />
        <text x="64" y="64" textAnchor="middle" dominantBaseline="central"
          fontSize="24" fontWeight="bold" fill={color}>
          {animated}
        </text>
        <text x="64" y="82" textAnchor="middle"
          fontSize="11" fill="hsl(var(--text-muted))">
          /100
        </text>
      </svg>
      <span style={{ color: "hsl(var(--text-secondary))" }}
             className="text-sm font-medium">
        Confidence
      </span>
    </div>
  )
}
