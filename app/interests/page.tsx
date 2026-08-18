'use client'

import { PageHeader } from '@/components/shared/page-header'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { api } from '@/lib/api-client'
import { useApi } from '@/hooks/use-api'
import type { Interest, InterestGraph as Graph } from '@/lib/types'
import { InterestProgress } from '@/components/shared/interest-progress'
import { InterestGraph } from '@/components/shared/interest-graph'
import { ConfidenceBadge } from '@/components/shared/badges'
import { LoadingState, ErrorState } from '@/components/shared/states'
import { Network, ListTree } from 'lucide-react'

const USER_ID = 'me'

export default function InterestsPage() {
  const interests = useApi<Interest[]>('interests', () => api.getInterests(USER_ID))
  const graph = useApi<Graph>('interest-graph', () => api.getInterestGraph(USER_ID))

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Interest Profile"
        description="What the agent believes you're genuinely trying to learn"
      />
      <div className="mx-auto w-full max-w-6xl flex-1 space-y-6 p-4 md:p-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Network className="size-4 text-primary" />
              Interest graph
            </CardTitle>
          </CardHeader>
          <CardContent>
            {graph.isLoading && <LoadingState rows={1} />}
            {graph.error && <ErrorState onRetry={() => graph.mutate()} />}
            {graph.data && <InterestGraph graph={graph.data} />}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <ListTree className="size-4 text-primary" />
              Inferred interests
            </CardTitle>
          </CardHeader>
          <CardContent>
            {interests.isLoading && <LoadingState rows={3} />}
            {interests.error && <ErrorState onRetry={() => interests.mutate()} />}
            {interests.data && (
              <div className="grid gap-4 md:grid-cols-2">
                {interests.data.map((it, i) => (
                  <div key={it.id} className="rounded-xl border border-border bg-muted/20 p-4">
                    <InterestProgress name={it.name} score={it.score} trend={it.trend} index={i} />
                    <div className="mt-3 flex items-center justify-between">
                      <ConfidenceBadge value={it.confidence} />
                    </div>
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {it.relatedTopics.map((t) => (
                        <span
                          key={t}
                          className="rounded-md bg-secondary px-2 py-0.5 text-xs text-secondary-foreground"
                        >
                          {t}
                        </span>
                      ))}
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
