import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

export function KpiCard({
  label,
  value,
  hint,
  icon,
  accent,
}: {
  label: string
  value: string | number
  hint?: string
  icon?: ReactNode
  accent?: boolean
}) {
  return (
    <Card className={cn(accent && 'border-primary/30 bg-gradient-to-b from-primary/[0.05] to-card')}>
      <CardContent className="flex items-start justify-between gap-3 py-5">
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            {label}
          </p>
          <p className="mt-1.5 font-mono text-2xl font-semibold tabular-nums text-foreground">
            {value}
          </p>
          {hint && <p className="mt-1 truncate text-xs text-muted-foreground">{hint}</p>}
        </div>
        {icon && (
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
            {icon}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export function ChartCard({
  title,
  description,
  children,
  className,
}: {
  title: string
  description?: string
  children: ReactNode
  className?: string
}) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  )
}
