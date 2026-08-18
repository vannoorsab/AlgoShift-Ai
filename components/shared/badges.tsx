import { cn } from '@/lib/utils'
import type { Confidence, Difficulty, Category } from '@/lib/types'
import { ShieldCheck, Signal, TrendingUp } from 'lucide-react'

export function ConfidenceBadge({ value, className }: { value: Confidence; className?: string }) {
  const styles: Record<Confidence, string> = {
    High: 'bg-success/15 text-success border-success/25',
    Medium: 'bg-warning/15 text-warning border-warning/25',
    Low: 'bg-muted text-muted-foreground border-border',
  }
  return (
    <span
      className={cn(
        'inline-flex h-6 w-fit items-center gap-1 rounded-full border px-2 text-xs font-medium',
        styles[value],
        className,
      )}
    >
      <Signal className="size-3" />
      {value} confidence
    </span>
  )
}

export function DifficultyBadge({ value, className }: { value: Difficulty; className?: string }) {
  const styles: Record<Difficulty, string> = {
    Beginner: 'bg-chart-3/15 text-chart-3 border-chart-3/25',
    Intermediate: 'bg-chart-2/15 text-chart-2 border-chart-2/25',
    Advanced: 'bg-chart-5/15 text-chart-5 border-chart-5/25',
  }
  return (
    <span
      className={cn(
        'inline-flex h-6 w-fit items-center gap-1 rounded-full border px-2 text-xs font-medium',
        styles[value],
        className,
      )}
    >
      <TrendingUp className="size-3" />
      {value}
    </span>
  )
}

export function CategoryBadge({ value, className }: { value: Category | string; className?: string }) {
  return (
    <span
      className={cn(
        'inline-flex h-6 w-fit items-center gap-1 rounded-full border border-primary/25 bg-primary/10 px-2 text-xs font-medium text-primary',
        className,
      )}
    >
      {value}
    </span>
  )
}

export function ScorePill({
  label,
  value,
  className,
}: {
  label: string
  value: number
  className?: string
}) {
  const tone =
    value >= 80
      ? 'text-success'
      : value >= 55
        ? 'text-primary'
        : value >= 35
          ? 'text-warning'
          : 'text-muted-foreground'
  return (
    <div className={cn('flex flex-col gap-0.5', className)}>
      <span className="text-xs text-muted-foreground">{label}</span>
      <span className={cn('font-mono text-lg font-semibold tabular-nums', tone)}>{value}%</span>
    </div>
  )
}

export function QualityFlag({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        'inline-flex h-6 w-fit items-center gap-1 rounded-full border border-success/25 bg-success/15 px-2 text-xs font-medium text-success',
        className,
      )}
    >
      <ShieldCheck className="size-3" />
      Quality checked
    </span>
  )
}
