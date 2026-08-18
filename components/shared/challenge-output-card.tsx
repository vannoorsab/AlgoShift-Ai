'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { ChallengeOutputResult } from '@/lib/types'
import { Sparkles, Film, Lightbulb, Compass, Award, Tag, Gauge, CheckCircle } from 'lucide-react'

interface ChallengeOutputCardProps {
  result: ChallengeOutputResult
}

export function ChallengeOutputCard({ result }: ChallengeOutputCardProps) {
  return (
    <Card className="border border-primary/30 bg-card shadow-lg">
      <CardHeader className="border-b border-border/50 bg-gradient-to-r from-primary/10 via-card to-card pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="size-5 text-primary" />
            <CardTitle className="text-lg">Required Challenge Output</CardTitle>
          </div>
          <Badge variant="outline" className="border-primary/40 text-primary font-mono text-xs">
            Agentic AI Verification
          </Badge>
        </div>
        <CardDescription>
          Exact 8-field structured challenge recommendation output
        </CardDescription>
      </CardHeader>

      <CardContent className="p-6 space-y-6">
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

        {/* 4. RECOMMENDED TECH REEL */}
        <div className="space-y-2 rounded-xl border-2 border-emerald-500/40 p-4 bg-emerald-500/5">
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
          <span className="text-xs font-mono text-muted-foreground">Candidate ID: {result.recommendedTechReel.candidateId}</span>
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
      </CardContent>
    </Card>
  )
}
