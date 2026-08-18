'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ScoreBreakdownCard } from './score-breakdown-card'
import { InterestBridge } from './interest-bridge'
import { FeedbackButtons } from './feedback-buttons'
import type { ChallengeOutputResult, Evidence } from '@/lib/types'
import { Sparkles, Film, Lightbulb, Compass, Award, Tag, Gauge, CheckCircle, Video, Play, Pause, Volume2, Maximize2, RefreshCw } from 'lucide-react'

interface ChallengeOutputCardProps {
  result: ChallengeOutputResult
  evidence?: Evidence
  onDiscoverNext?: () => void
  isNextLoading?: boolean
}

export function ChallengeOutputCard({
  result,
  evidence,
  onDiscoverNext,
  isNextLoading = false,
}: ChallengeOutputCardProps) {
  const [isPlaying, setIsPlaying] = useState(false)

  return (
    <Card className="border border-primary/30 bg-card shadow-lg overflow-hidden">
      <CardHeader className="border-b border-border/50 bg-gradient-to-r from-primary/10 via-card to-card pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="size-5 text-primary" />
            <CardTitle className="text-lg">Recommendation Output</CardTitle>
          </div>
          <Badge variant="outline" className="border-primary/40 text-primary font-mono text-xs">
            Agentic AI Verification
          </Badge>
        </div>
        <CardDescription>
          Structured 8-field agentic recommendation output
        </CardDescription>
      </CardHeader>

      <CardContent className="p-6 space-y-6" aria-live="polite" aria-atomic="true">
        <div className="grid gap-4 md:grid-cols-2">
          {/* 1. CURRENT REEL */}
          <div className="space-y-1.5 rounded-xl border border-border p-4 bg-muted/20">
            <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              <Film className="size-4 text-primary" />
              CURRENT REEL
            </div>
            <p className="text-base font-semibold text-foreground">
              {result.currentReel.title}
            </p>
            <span className="text-xs font-mono text-muted-foreground">ID: {result.currentReel.reelId}</span>
          </div>

          {/* 2. INTEREST DETECTED */}
          <div className="space-y-1.5 rounded-xl border border-primary/30 p-4 bg-primary/5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase tracking-wider">
                <Lightbulb className="size-4 text-primary" />
                INTEREST DETECTED
              </div>
              <Badge className="bg-primary/20 text-primary hover:bg-primary/30 text-xs">
                {result.interestDetected.confidence} Confidence
              </Badge>
            </div>
            <p className="text-xl font-bold text-foreground">
              {result.interestDetected.topic}
            </p>
          </div>
        </div>

        {/* 3. WHY */}
        <div className="space-y-2 rounded-xl border border-border p-4 bg-muted/10">
          <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            <Award className="size-4 text-primary" />
            WHY
          </div>
          <p className="text-sm leading-relaxed text-foreground/90">
            {result.why}
          </p>
        </div>

        {/* 4. RECOMMENDED TECH REEL & VIDEO PLAYER */}
        <div className="space-y-4 rounded-xl border-2 border-emerald-500/40 p-4 bg-emerald-500/5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-500 uppercase tracking-wider">
              <Compass className="size-4 text-emerald-500" />
              RECOMMENDED TECH REEL
            </div>
            <Badge className="bg-emerald-500/20 text-emerald-500 hover:bg-emerald-500/30 text-xs">
              Selected Winner
            </Badge>
          </div>
          <p className="text-lg font-bold text-foreground">
            {result.recommendedTechReel.title}
          </p>
          <span className="text-xs font-mono text-muted-foreground block">Candidate ID: {result.recommendedTechReel.candidateId}</span>

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
              <div className="bg-slate-900/90 backdrop-blur-md p-2.5 rounded-xl border border-slate-800 text-xs text-slate-200">
                <p className="font-semibold text-emerald-400 text-[10px] uppercase tracking-wider mb-0.5">Live Transcript</p>
                <p className="line-clamp-1 italic">&ldquo;Understanding technical concepts step-by-step for high educational relevance...&rdquo;</p>
              </div>

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
              <div className="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                <div className={`bg-emerald-500 h-full transition-all duration-300 ${isPlaying ? 'w-[40%]' : 'w-0'}`} />
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          {/* 5. CATEGORY */}
          <div className="space-y-1.5 rounded-xl border border-border p-3.5 bg-muted/20">
            <div className="flex items-center gap-2 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
              <Tag className="size-3.5 text-primary" />
              CATEGORY
            </div>
            <p className="text-base font-bold text-foreground">
              {result.category}
            </p>
          </div>

          {/* 7. DIFFICULTY */}
          <div className="space-y-1.5 rounded-xl border border-border p-3.5 bg-muted/20">
            <div className="flex items-center gap-2 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
              <Gauge className="size-3.5 text-amber-500" />
              DIFFICULTY
            </div>
            <p className="text-base font-bold text-foreground">
              {result.difficulty}
            </p>
          </div>

          {/* 8. CONFIDENCE */}
          <div className="space-y-1.5 rounded-xl border border-border p-3.5 bg-muted/20">
            <div className="flex items-center gap-2 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
              <CheckCircle className="size-3.5 text-emerald-500" />
              CONFIDENCE
            </div>
            <p className="text-base font-bold text-foreground">
              {result.confidence}
            </p>
          </div>
        </div>

        {/* 6. WHY THIS RECOMMENDATION */}
        <div className="space-y-2 rounded-xl border border-border p-4 bg-muted/10">
          <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            <Sparkles className="size-4 text-primary" />
            WHY THIS RECOMMENDATION
          </div>
          <p className="text-sm leading-relaxed text-foreground/90">
            {result.whyThisRecommendation}
          </p>
        </div>

        {/* INTEREST BRIDGE & SCORE BREAKDOWN */}
        <InterestBridge interestPath={evidence?.interestPath ?? ['Programming', 'Software Engineering', 'Backend', 'APIs']} />
        <ScoreBreakdownCard selectionFactors={evidence?.selectionFactors} />

        {/* FEEDBACK & DISCOVER NEXT ACTION BAR */}
        <div className="pt-2 border-t border-border/50 flex flex-wrap items-center justify-between gap-4">
          <FeedbackButtons reelId={result.recommendedTechReel.candidateId} />

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
