import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { RejectedContent } from '@/lib/types'
import { ShieldAlert, XCircle } from 'lucide-react'
import { cn } from '@/lib/utils'

function Metric({ label, value, danger }: { label: string; value: number; danger?: boolean }) {
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className={cn('font-mono font-semibold tabular-nums', danger ? 'text-destructive' : 'text-foreground')}>
          {value}%
        </span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
        <div
          className={cn('h-full rounded-full', danger ? 'bg-destructive' : 'bg-muted-foreground/50')}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  )
}

export function QualityScoreCard({ item }: { item: RejectedContent }) {
  return (
    <Card className="border-destructive/25 bg-destructive/[0.03]">
      <CardHeader className="gap-2">
        <div className="flex items-center justify-between">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-destructive/30 bg-destructive/10 px-2.5 py-1 text-xs font-semibold text-destructive">
            <XCircle className="size-3.5" />
            {item.status}
          </span>
          <ShieldAlert className="size-5 text-destructive/70" />
        </div>
        <CardTitle className="text-pretty text-base leading-snug line-through decoration-destructive/40">
          {item.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <Metric label="Hype Score" value={item.hypeScore} danger />
          <Metric label="Educational Value" value={item.educationalValue} />
          <Metric label="Evidence Quality" value={item.evidenceQuality} />
        </div>
        <div className="rounded-lg border border-destructive/20 bg-background/50 p-3">
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Reason</p>
          <p className="mt-1 text-sm text-foreground/90">{item.reason}</p>
        </div>
      </CardContent>
    </Card>
  )
}
