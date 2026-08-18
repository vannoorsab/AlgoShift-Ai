import Link from 'next/link'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ConfidenceBadge, ScorePill } from '@/components/shared/badges'
import { Play, ArrowRight } from 'lucide-react'
import type { ReelAnalysis } from '@/lib/types'

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</p>
      <p className="mt-0.5 text-sm font-medium text-foreground">{value}</p>
    </div>
  )
}

export function CurrentReelCard({ analysis }: { analysis: ReelAnalysis }) {
  return (
    <Card className="overflow-hidden">
      <CardHeader className="gap-3">
        <span className="text-xs font-semibold uppercase tracking-widest text-primary">
          Current Reel
        </span>
        <div className="flex items-start gap-4">
          <div className="flex aspect-[3/4] h-24 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-secondary to-muted">
            <Play className="size-6 text-muted-foreground" />
          </div>
          <div className="min-w-0">
            <h3 className="text-pretty text-lg font-semibold leading-snug text-foreground">
              {analysis.title}
            </h3>
            <div className="mt-2">
              <ConfidenceBadge value={analysis.confidence} />
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
          <Field label="Topic" value={analysis.primaryTopic} />
          <Field label="Broader Interest" value={analysis.broaderDomain} />
          <Field label="Context" value={analysis.context} />
        </div>
        <div className="flex gap-8 border-t border-border pt-4">
          <ScorePill label="Educational Value" value={analysis.educationalValue} />
          <ScorePill label="Career Relevance" value={analysis.careerRelevance} />
        </div>
        <Button variant="outline" className="w-full" render={<Link href="/reel-analysis" />}>
          View Analysis
          <ArrowRight className="size-4" />
        </Button>
      </CardContent>
    </Card>
  )
}
