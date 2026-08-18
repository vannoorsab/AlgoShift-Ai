'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { CategoryBadge, ConfidenceBadge, DifficultyBadge } from './badges'
import { FeedbackButtons } from './feedback-buttons'
import { ScoreBreakdownCard } from './score-breakdown-card'
import { InterestBridge } from './interest-bridge'
import { Button } from '@/components/ui/button'
import type { AnalyzeResponse, Recommendation } from '@/lib/types'
import { Compass, Sparkles, RefreshCw, Play, Pause, Volume2, Maximize2, Video } from 'lucide-react'

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
  const [isPlaying, setIsPlaying] = useState(false)
  const result = analyzeResponse?.result
  const evidence = analyzeResponse?.evidence

  const title = result?.recommendedTechReel.title ?? rec?.title ?? 'REST APIs Explained: Design & Best Practices'
  const category = result?.category ?? rec?.category ?? 'Cloud'
  const difficulty = result?.difficulty ?? rec?.difficulty ?? 'Intermediate'
  const confidence = result?.confidence ?? rec?.confidence ?? 'High'
  const why = result?.whyThisRecommendation ?? rec?.why ?? 'Expands Software Engineering interests into backend and API concepts.'
  const candidateId = result?.recommendedTechReel.candidateId ?? rec?.id ?? 'CAND_TECH003'

  return (
    <Card className="border-2 border-emerald-500/30 bg-gradient-to-b from-emerald-500/[0.04] via-card to-card shadow-md overflow-hidden">
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
        {/* REEL VIDEO PLAYER FRAME */}
        <div className="relative group rounded-2xl overflow-hidden border border-emerald-500/30 bg-slate-950 aspect-video flex flex-col justify-between p-4 shadow-inner">
          {/* TOP OVERLAY BADGES */}
          <div className="flex items-center justify-between z-10">
            <div className="flex items-center gap-2 bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-full text-[11px] font-medium text-emerald-400 border border-emerald-500/30">
              <Video className="size-3.5 animate-pulse" />
              <span>1080p HD Reel Video</span>
            </div>
            <span className="bg-slate-900/80 backdrop-blur-md px-2 py-0.5 rounded font-mono text-[10px] text-slate-300">
              0:45
            </span>
          </div>

          {/* CENTER PLAY/PAUSE TRIGGER */}
          <div className="absolute inset-0 flex items-center justify-center bg-slate-950/40 group-hover:bg-slate-950/20 transition-all">
            <button
              type="button"
              onClick={() => setIsPlaying(!isPlaying)}
              aria-label={isPlaying ? 'Pause Reel Video' : 'Play Reel Video'}
              className="flex items-center justify-center size-14 rounded-full bg-emerald-500 text-slate-950 shadow-lg hover:scale-105 active:scale-95 transition-transform"
            >
              {isPlaying ? <Pause className="size-6 fill-current" /> : <Play className="size-6 fill-current ml-0.5" />}
            </button>
          </div>

          {/* BOTTOM OVERLAY CAPTIONS & CONTROLS */}
          <div className="z-10 space-y-2">
            {/* LIVE TRANSCRIPT PREVIEW CAPTION */}
            <div className="bg-slate-900/90 backdrop-blur-md p-2.5 rounded-xl border border-slate-800 text-xs text-slate-200">
              <p className="font-semibold text-emerald-400 text-[10px] uppercase tracking-wider mb-0.5">Live Transcript</p>
              <p className="line-clamp-1 italic">&ldquo;Understanding REST API endpoints, HTTP methods, status codes, and JSON payload architecture...&rdquo;</p>
            </div>

            {/* VIDEO CONTROL BAR */}
            <div className="flex items-center justify-between text-slate-400 text-xs pt-1">
              <div className="flex items-center gap-3">
                <button type="button" onClick={() => setIsPlaying(!isPlaying)} className="hover:text-white transition-colors">
                  {isPlaying ? <Pause className="size-4" /> : <Play className="size-4" />}
                </button>
                <Volume2 className="size-4 hover:text-white transition-colors cursor-pointer" />
                <span className="font-mono text-[11px]">{isPlaying ? '0:18 / 0:45' : '0:00 / 0:45'}</span>
              </div>
              <Maximize2 className="size-3.5 hover:text-white transition-colors cursor-pointer" />
            </div>
            {/* VIDEO PROGRESS BAR */}
            <div className="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
              <div className={`bg-emerald-500 h-full transition-all duration-300 ${isPlaying ? 'w-[40%]' : 'w-0'}`} />
            </div>
          </div>
        </div>

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
