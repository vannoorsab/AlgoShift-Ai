'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import { api } from '@/lib/api-client'
import type { InterestTopicChange } from '@/lib/types'
import { ThumbsUp, Bookmark, Eye, SkipForward, CheckCircle2, TrendingUp, Loader2 } from 'lucide-react'

interface FeedbackButtonsProps {
  reelId?: string
  userId?: string
  onFeedbackComplete?: (updated: InterestTopicChange[]) => void
}

export function FeedbackButtons({
  reelId = 'TECH003',
  userId = 'student_001',
  onFeedbackComplete,
}: FeedbackButtonsProps) {
  const [loadingAction, setLoadingAction] = useState<string | null>(null)
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null)
  const [topicChanges, setTopicChanges] = useState<InterestTopicChange[]>([])

  async function handleFeedback(action: 'like' | 'save' | 'watch' | 'skip') {
    setLoadingAction(action)
    setFeedbackMessage(null)

    const payload = {
      userId,
      reelId,
      watchPercentage: action === 'skip' ? 15.0 : 96.0,
      liked: action === 'like',
      saved: action === 'save',
      skipped: action === 'skip',
      completed: action === 'watch' || action === 'like',
    }

    try {
      const res = await api.sendFeedback(payload)
      if (res.success) {
        setFeedbackMessage(res.message || 'Your interest profile was updated.')
        setTopicChanges(res.updatedInterests || [])
        if (onFeedbackComplete) {
          onFeedbackComplete(res.updatedInterests || [])
        }
      }
    } catch (err: any) {
      setFeedbackMessage(err.message || 'Failed to submit feedback.')
    } finally {
      setLoadingAction(null)
    }
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <Button
          size="sm"
          variant="outline"
          className="gap-1.5 border-emerald-500/40 text-emerald-500 hover:bg-emerald-500/10"
          disabled={loadingAction !== null}
          onClick={() => handleFeedback('like')}
        >
          {loadingAction === 'like' ? <Loader2 className="size-3.5 animate-spin" /> : <ThumbsUp className="size-3.5" />}
          Like
        </Button>

        <Button
          size="sm"
          variant="outline"
          className="gap-1.5 border-primary/40 text-primary hover:bg-primary/10"
          disabled={loadingAction !== null}
          onClick={() => handleFeedback('save')}
        >
          {loadingAction === 'save' ? <Loader2 className="size-3.5 animate-spin" /> : <Bookmark className="size-3.5" />}
          Save
        </Button>

        <Button
          size="sm"
          variant="outline"
          className="gap-1.5"
          disabled={loadingAction !== null}
          onClick={() => handleFeedback('watch')}
        >
          {loadingAction === 'watch' ? <Loader2 className="size-3.5 animate-spin" /> : <Eye className="size-3.5" />}
          Watch (96%)
        </Button>

        <Button
          size="sm"
          variant="ghost"
          className="gap-1.5 text-muted-foreground hover:text-destructive"
          disabled={loadingAction !== null}
          onClick={() => handleFeedback('skip')}
        >
          {loadingAction === 'skip' ? <Loader2 className="size-3.5 animate-spin" /> : <SkipForward className="size-3.5" />}
          Not Interested
        </Button>
      </div>

      {feedbackMessage && (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3 text-xs space-y-2">
          <div className="flex items-center gap-2 text-emerald-500 font-semibold">
            <CheckCircle2 className="size-4" />
            {feedbackMessage}
          </div>

          {topicChanges.length > 0 && (
            <div className="flex flex-wrap gap-2 pt-1">
              {topicChanges.map((change, idx) => (
                <Badge key={idx} variant="outline" className="gap-1 border-emerald-500/40 bg-background text-emerald-500 font-mono text-[11px]">
                  <TrendingUp className="size-3" />
                  {change.topic}: {Math.round(change.oldScore * 100)}% → {Math.round(change.newScore * 100)}%
                </Badge>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
