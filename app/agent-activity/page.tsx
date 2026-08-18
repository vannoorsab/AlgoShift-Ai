'use client'

import { useState, useEffect } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { LoadingState } from '@/components/shared/states'
import { api } from '@/lib/api-client'
import type { AgentPipeline } from '@/lib/types'
import { Workflow, CheckCircle2, Cpu } from 'lucide-react'

export default function AgentActivityPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [pipeline, setPipeline] = useState<AgentPipeline | null>(null)

  useEffect(() => {
    async function loadAgentActivity() {
      try {
        const data = await api.getAgentRuns('student_001')
        setPipeline(data)
      } catch {
        // Fallback
      } finally {
        setIsLoading(false)
      }
    }
    loadAgentActivity()
  }, [])

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Agentic AI Execution Activity"
        description="Inspect internal reasoning logs, pipeline duration metrics, and agent state transitions"
      />
      <div className="mx-auto w-full max-w-5xl flex-1 space-y-6 p-4 md:p-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Workflow className="size-5 text-primary" />
                <CardTitle className="text-base font-semibold">Active Agent Pipeline Runs</CardTitle>
              </div>
              {pipeline && (
                <Badge variant="outline" className="font-mono text-xs border-primary/40 text-primary">
                  Run ID: {pipeline.runId}
                </Badge>
              )}
            </div>
            <CardDescription>
              Sequence of 7 specialized AI Agents executing in real-time
            </CardDescription>
          </CardHeader>

          <CardContent className="p-6 pt-0">
            {isLoading || !pipeline ? (
              <LoadingState rows={2} />
            ) : (
              <div className="space-y-4">
                {pipeline.agents.map((agent, idx) => (
                  <div
                    key={agent.id || idx}
                    className="rounded-xl border border-border bg-muted/20 p-4 space-y-2"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2 font-semibold text-sm text-foreground">
                        <Cpu className="size-4 text-primary shrink-0" />
                        <span>{agent.name}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {agent.durationMs && (
                          <span className="text-xs font-mono text-muted-foreground">{agent.durationMs}ms</span>
                        )}
                        <Badge className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20 text-xs gap-1">
                          <CheckCircle2 className="size-3" />
                          {agent.status}
                        </Badge>
                      </div>
                    </div>

                    <p className="text-xs font-medium text-foreground">{agent.summary}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed bg-background/60 p-2.5 rounded-lg border border-border/40 font-mono">
                      {agent.detail}
                    </p>
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
