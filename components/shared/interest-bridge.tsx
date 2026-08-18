'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { GitBranch, ArrowRight } from 'lucide-react'

interface InterestBridgeProps {
  interestPath?: string[]
}

export function InterestBridge({ interestPath }: InterestBridgeProps) {
  const defaultPath = ['Java', 'Programming', 'Software Engineering', 'Backend', 'APIs']
  const path = interestPath && interestPath.length > 0 ? interestPath : defaultPath

  return (
    <Card className="border border-border bg-card shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center gap-2">
          <GitBranch className="size-4 text-primary" />
          <CardTitle className="text-sm font-semibold">Interest Bridge & Semantic Path</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <div className="flex flex-wrap items-center gap-2 rounded-xl border border-primary/20 bg-primary/5 p-4">
          {path.map((step, idx) => {
            const isLast = idx === path.length - 1
            const isFirst = idx === 0

            return (
              <div key={idx} className="flex items-center gap-2">
                <div
                  className={`rounded-lg px-3 py-1.5 text-xs font-semibold shadow-xs transition-colors ${
                    isLast
                      ? 'bg-emerald-500 text-white font-bold ring-2 ring-emerald-500/30'
                      : isFirst
                        ? 'bg-muted text-foreground border border-border'
                        : 'bg-primary/10 text-primary border border-primary/20'
                  }`}
                >
                  {step}
                </div>
                {!isLast && <ArrowRight className="size-3.5 text-muted-foreground shrink-0" />}
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
