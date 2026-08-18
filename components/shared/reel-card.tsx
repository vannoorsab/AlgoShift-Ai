'use client'

import { cn } from '@/lib/utils'
import type { Reel } from '@/lib/types'
import { Play } from 'lucide-react'

export function ReelCard({
  reel,
  selected,
  onSelect,
}: {
  reel: Reel
  selected?: boolean
  onSelect?: (reel: Reel) => void
}) {
  return (
    <button
      type="button"
      onClick={() => onSelect?.(reel)}
      className={cn(
        'group flex w-full items-center gap-3 rounded-xl border p-3 text-left transition-colors',
        selected
          ? 'border-primary/50 bg-primary/10'
          : 'border-border bg-card hover:border-border/80 hover:bg-muted/50',
      )}
    >
      <div className="flex aspect-[3/4] h-16 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-secondary to-muted">
        <Play className="size-4 text-muted-foreground group-hover:text-primary" />
      </div>
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium text-foreground">{reel.title}</p>
        <p className="mt-0.5 text-xs text-muted-foreground">
          {reel.topic} · {reel.context}
        </p>
        <p className="mt-1 text-xs text-primary/80">{reel.broaderInterest}</p>
      </div>
    </button>
  )
}
