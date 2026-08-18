'use client'

import { cn } from '@/lib/utils'
import type { InterestTrend } from '@/lib/types'

const trendLabel: Record<InterestTrend, string> = {
  primary: 'Primary Interest',
  growing: 'Growing',
  stable: 'Stable',
  emerging: 'Emerging',
  declining: 'Declining',
}

const trendTone: Record<InterestTrend, string> = {
  primary: 'text-primary',
  growing: 'text-success',
  stable: 'text-muted-foreground',
  emerging: 'text-chart-2',
  declining: 'text-destructive',
}

export function InterestProgress({
  name,
  score,
  trend,
  index = 0,
}: {
  name: string
  score: number
  trend?: InterestTrend
  index?: number
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-sm font-medium text-foreground">{name}</span>
        <div className="flex items-center gap-2">
          {trend && (
            <span className={cn('text-xs font-medium', trendTone[trend])}>{trendLabel[trend]}</span>
          )}
          <span className="font-mono text-sm font-semibold tabular-nums text-foreground">
            {score}%
          </span>
        </div>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
        <div
          className="animate-grow-bar h-full rounded-full bg-gradient-to-r from-primary/70 to-primary"
          style={{ width: `${score}%`, animationDelay: `${index * 80}ms` }}
        />
      </div>
    </div>
  )
}
