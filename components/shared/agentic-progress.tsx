'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { CheckCircle2, Loader2, Sparkles } from 'lucide-react'

const STAGES = [
  { id: 1, label: 'Understanding Reels', agent: 'Agent 1 — Reel Understanding' },
  { id: 2, label: 'Inferring interests', agent: 'Agent 2 — Interest Inference' },
  { id: 3, label: 'Exploring interest frontier', agent: 'Agent 3 — Candidate Generation' },
  { id: 4, label: 'Evaluating content quality', agent: 'Agent 4 — Hype Shield' },
  { id: 5, label: 'Ranking recommendations', agent: 'Agent 5 — Recommendation Ranking' },
  { id: 6, label: 'Generating explanation', agent: 'Agent 6 — Explanation Engine' },
]

interface AgenticProgressProps {
  isLoading: boolean
}

export function AgenticProgress({ isLoading }: AgenticProgressProps) {
  const [currentStage, setCurrentStage] = useState(1)

  useEffect(() => {
    if (!isLoading) {
      setCurrentStage(6)
      return
    }

    setCurrentStage(1)
    const interval = setInterval(() => {
      setCurrentStage((prev) => (prev < 6 ? prev + 1 : 6))
    }, 250)

    return () => clearInterval(interval)
  }, [isLoading])

  if (!isLoading) return null

  const progressPct = Math.round((currentStage / 6) * 100)

  return (
    <Card className="border border-primary/20 bg-gradient-to-br from-card via-card to-primary/5 shadow-md animate-pulse">
      <CardContent className="p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
            <Sparkles className="size-4 text-primary animate-spin" />
            Agentic AI Pipeline Execution
          </div>
          <span className="text-xs font-mono text-primary">{progressPct}% Complete</span>
        </div>

        <Progress value={progressPct} className="h-2" />

        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3 pt-2">
          {STAGES.map((s) => {
            const isDone = s.id < currentStage
            const isCurrent = s.id === currentStage

            return (
              <div
                key={s.id}
                className={`flex items-center gap-2.5 rounded-lg border p-2.5 transition-colors ${
                  isDone
                    ? 'border-emerald-500/30 bg-emerald-500/5 text-emerald-500'
                    : isCurrent
                      ? 'border-primary/40 bg-primary/10 text-primary font-medium'
                      : 'border-border/50 bg-muted/20 text-muted-foreground opacity-60'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 className="size-4 shrink-0 text-emerald-500" />
                ) : isCurrent ? (
                  <Loader2 className="size-4 shrink-0 text-primary animate-spin" />
                ) : (
                  <div className="size-4 rounded-full border border-current opacity-40 shrink-0" />
                )}
                <div className="overflow-hidden text-xs">
                  <p className="truncate font-medium">{s.id}. {s.label}</p>
                  <p className="truncate text-[10px] opacity-70">{s.agent}</p>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
