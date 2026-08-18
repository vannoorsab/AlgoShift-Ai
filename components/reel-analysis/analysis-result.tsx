import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import type { ReelAnalysis } from '@/lib/types'
import { ConfidenceBadge, DifficultyBadge } from '@/components/shared/badges'
import { Brain, Sparkles } from 'lucide-react'

function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-mono font-semibold tabular-nums text-foreground">{value}%</span>
      </div>
      <Progress value={value} className="h-2" />
    </div>
  )
}

export function AnalysisResult({ analysis }: { analysis: ReelAnalysis }) {
  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <Card className="lg:col-span-2">
        <CardHeader className="gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <DifficultyBadge value={analysis.difficulty} />
            <ConfidenceBadge value={analysis.confidence} />
          </div>
          <CardTitle className="text-pretty text-xl leading-tight">{analysis.title}</CardTitle>
          <div className="flex flex-wrap gap-2 text-sm">
            <span className="rounded-md bg-primary/10 px-2 py-1 font-medium text-primary">
              {analysis.primaryTopic}
            </span>
            <span className="rounded-md bg-secondary px-2 py-1 text-secondary-foreground">
              {analysis.broaderDomain}
            </span>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Subtopics detected
            </p>
            <div className="flex flex-wrap gap-2">
              {analysis.subtopics.map((s) => (
                <span
                  key={s}
                  className="rounded-full border border-border bg-muted/40 px-2.5 py-1 text-xs text-foreground"
                >
                  {s}
                </span>
              ))}
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border border-border bg-muted/20 p-4">
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Context</p>
              <p className="mt-1 text-sm text-foreground/90">{analysis.context}</p>
            </div>
            <div className="rounded-lg border border-border bg-muted/20 p-4">
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Intent</p>
              <p className="mt-1 text-sm text-foreground/90">{analysis.intent}</p>
            </div>
          </div>
          <div className="flex items-start gap-3 rounded-lg border border-primary/20 bg-primary/[0.04] p-4">
            <Brain className="mt-0.5 size-5 shrink-0 text-primary" />
            <div>
              <p className="text-sm font-semibold text-foreground">Model reasoning</p>
              <p className="mt-1 text-sm text-muted-foreground">{analysis.reasoning}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="size-4 text-primary" />
            Signal breakdown
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <ScoreBar label="Educational value" value={analysis.educationalValue} />
          <ScoreBar label="Career relevance" value={analysis.careerRelevance} />
          <ScoreBar label="Technical depth" value={analysis.technicalDepth} />
          <ScoreBar label="Entertainment value" value={analysis.entertainmentValue} />
          <div className="rounded-lg border border-warning/25 bg-warning/[0.06] p-3">
            <ScoreBar label="Hype score" value={analysis.hypeScore} />
            <p className="mt-2 text-xs text-muted-foreground">
              Higher hype lowers a reel&apos;s recommendation priority.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
