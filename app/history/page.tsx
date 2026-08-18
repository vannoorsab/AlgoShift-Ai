'use client'

import { useState, useEffect } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { LoadingState } from '@/components/shared/states'
import { api } from '@/lib/api-client'
import type { HistoryEvent } from '@/lib/types'
import { History, Film, ThumbsUp, Sparkles, Workflow } from 'lucide-react'

export default function HistoryPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [historyEvents, setHistoryEvents] = useState<HistoryEvent[]>([])

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await api.getHistory('student_001')
        setHistoryEvents(data)
      } catch {
        // Fallback
      } finally {
        setIsLoading(false)
      }
    }
    loadHistory()
  }, [])

  function getKindIcon(kind: string) {
    switch (kind) {
      case 'reel':
        return <Film className="size-4 text-primary" />
      case 'interaction':
        return <ThumbsUp className="size-4 text-emerald-500" />
      case 'interest_change':
        return <Sparkles className="size-4 text-amber-500" />
      default:
        return <Workflow className="size-4 text-accent" />
    }
  }

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Activity History"
        description="Chronological log of reel ingestions, agent runs, and profile adaptations"
      />
      <div className="mx-auto w-full max-w-5xl flex-1 space-y-6 p-4 md:p-6">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <History className="size-5 text-primary" />
              <CardTitle className="text-base font-semibold">Workflow & Interaction Timeline</CardTitle>
            </div>
            <CardDescription>
              Recent events processed by AlgoShift AI Agents
            </CardDescription>
          </CardHeader>

          <CardContent className="p-6 pt-0">
            {isLoading ? (
              <LoadingState rows={2} />
            ) : (
              <div className="space-y-4">
                {historyEvents.map((evt) => (
                  <div
                    key={evt.id}
                    className="flex flex-col gap-2 rounded-xl border border-border bg-muted/20 p-4 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 rounded-lg border border-border p-2 bg-background">
                        {getKindIcon(evt.kind)}
                      </div>
                      <div className="space-y-0.5">
                        <p className="text-sm font-semibold text-foreground">{evt.title}</p>
                        <p className="text-xs text-muted-foreground">{evt.description}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 sm:self-center">
                      <Badge variant="outline" className="text-[11px] font-mono capitalize">
                        {evt.kind.replace('_', ' ')}
                      </Badge>
                      <span className="text-[11px] text-muted-foreground">{evt.timestamp}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
