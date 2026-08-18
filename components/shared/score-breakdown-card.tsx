'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'
import { Award, Trophy, CheckCircle2 } from 'lucide-react'

interface ScoreBreakdownCardProps {
  selectionFactors?: string[]
}

export function ScoreBreakdownCard({ selectionFactors }: ScoreBreakdownCardProps) {
  const defaultFactors = [
    'Strong Software Engineering interest match (25% weight)',
    'High educational depth (20% weight)',
    'Practical usefulness and architectural relevance (15% weight)',
    'Novelty & low repetition penalty (10% weight)',
    'Expansion along Interest Frontier: APIs & Backend (10% weight)',
    'Intermediate difficulty fit (5% weight)',
    'Low hype and clean Quality Gate score (5% weight)',
  ]

  const factors = selectionFactors && selectionFactors.length > 0 ? selectionFactors : defaultFactors

  return (
    <Card className="border border-emerald-500/30 bg-gradient-to-br from-card via-card to-emerald-500/5 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Trophy className="size-5 text-emerald-500" />
            <CardTitle className="text-base font-semibold">Recommendation Score Factors</CardTitle>
          </div>
          <Badge className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20 text-xs">
            Agent 5 Winner
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="p-4 pt-0">
        <Accordion className="w-full">
          <AccordionItem value="score-breakdown" className="border-none">
            <AccordionTrigger className="hover:no-underline py-2 text-sm font-medium text-foreground">
              <span className="flex items-center gap-2">
                <Award className="size-4 text-emerald-500" />
                Why this Reel won
              </span>
            </AccordionTrigger>
            <AccordionContent className="pt-2 space-y-3">
              <div className="space-y-2">
                {factors.map((factor, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 rounded-lg border border-border/50 bg-muted/20 p-2.5 text-xs text-foreground">
                    <CheckCircle2 className="size-4 shrink-0 text-emerald-500" />
                    <span>{factor}</span>
                  </div>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>
  )
}
