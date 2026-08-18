'use client'

import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { CategoryBadge, ConfidenceBadge, DifficultyBadge, ScorePill } from './badges'
import { FeedbackButtons } from './feedback-buttons'
import { ScoreBreakdownCard } from './score-breakdown-card'
import { InterestBridge } from './interest-bridge'
import { Button } from '@/components/ui/button'
import type { AnalyzeResponse, Recommendation } from '@/lib/types'
import { ArrowRight, Compass, Sparkles, RefreshCw } from 'lucide-react'

interface RecommendationCardProps {
  rec?: Recommendation
  analyzeResponse?: AnalyzeResponse
  featured?: boolean
  onDiscoverNext?: () => void
  isNextLoading?: boolean
}

export function RecommendationCard({
  rec,
  analyzeResponse,
  featured = true,
  onDiscoverNext,
  isNextLoading = false,
}: RecommendationCardProps) {
  const result = analyzeResponse?.result
  const evidence = analyzeResponse?.evidence

  const title = result?.recommendedTechReel.title ?? rec?.title ?? 'REST APIs Explained: Design & Best Practices'
  const category = result?.category ?? rec?.category ?? 'Cloud'
  const difficulty = result?.difficulty ?? rec?.difficulty ?? 'Intermediate'
  const confidence = result?.confidence ?? rec?.confidence ?? 'High'
  const why = result?.whyThisRecommendation ?? rec?.why ?? 'Expands Software Engineering interests into backend and API concepts.'
  const candidateId = result?.recommendedTechReel.candidateId ?? rec?.id ?? 'CAND_TECH003'

  return (
    <Card className="border-2 border-emerald-500/30 bg-gradient-to-b from-emerald-500/[0.04] via-card to-card shadow-md">
      <CardHeader className="gap-3 pb-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <CategoryBadge value={category} />
            <DifficultyBadge value={difficulty} />
            <ConfidenceBadge value={confidence} />
          </div>
          <span className="text-xs font-mono text-muted-foreground">{candidateId}</span>
        </div>

        <div className="space-y-1">
          <span className="text-xs font-semibold text-emerald-500 uppercase tracking-wider flex items-center gap-1.5">
            <Compass className="size-3.5" />
            RECOMMENDED TECH REEL
          </span>
          <h3 className="text-xl font-bold leading-snug text-foreground">
            {title}
          </h3>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4 space-y-1">
          <p className="text-xs font-semibold uppercase tracking-wide text-emerald-500">
            WHY THIS RECOMMENDATION
          </p>
          <p className="text-sm leading-relaxed text-foreground/90">{why}</p>
        </div>

        <InterestBridge interestPath={evidence?.interestPath ?? ['Programming', 'Software Engineering', 'Backend', 'APIs']} />

        <ScoreBreakdownCard selectionFactors={evidence?.selectionFactors} />

        <div className="pt-2 border-t border-border/50 flex flex-wrap items-center justify-between gap-4">
          <FeedbackButtons reelId={candidateId} />

          {onDiscoverNext && (
            <Button
              type="button"
              onClick={onDiscoverNext}
              disabled={isNextLoading}
              className="gap-2 bg-gradient-to-r from-primary to-accent text-primary-foreground font-medium shadow"
            >
              {isNextLoading ? (
                <RefreshCw className="size-4 animate-spin" />
              ) : (
                <Sparkles className="size-4" />
              )}
              {isNextLoading ? 'Discovering Next...' : 'Discover Next'}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
