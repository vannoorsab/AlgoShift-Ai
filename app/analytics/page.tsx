'use client'

import { useState, useEffect } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { LoadingState } from '@/components/shared/states'
import { api } from '@/lib/api-client'
import type { Analytics } from '@/lib/types'
import { BarChart3, ShieldCheck, Award, Sparkles, CheckCircle2 } from 'lucide-react'

export default function AnalyticsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [analytics, setAnalytics] = useState<Analytics | null>(null)

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const data = await api.getAnalytics('student_001')
        setAnalytics(data)
      } catch {
        // Fallback
      } finally {
        setIsLoading(false)
      }
    }
    loadAnalytics()
  }, [])

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Learning & System Analytics"
        description="Metrics on educational curation, quality filtering ratio, and interest evolution"
      />
      <div className="mx-auto w-full max-w-5xl flex-1 space-y-6 p-4 md:p-6">
        {isLoading || !analytics ? (
          <LoadingState rows={2} />
        ) : (
          <div className="space-y-6">
            {/* KPI GRID */}
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <Card className="border-primary/20 bg-primary/5">
                <CardHeader className="pb-2">
                  <p className="text-xs font-semibold text-primary uppercase">Useful Content Pct</p>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-3xl font-bold text-foreground">{analytics.kpis.usefulContentPct}%</span>
                    <Sparkles className="size-6 text-primary" />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-emerald-500/20 bg-emerald-500/5">
                <CardHeader className="pb-2">
                  <p className="text-xs font-semibold text-emerald-500 uppercase">Recommendations Accepted</p>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-3xl font-bold text-foreground">{analytics.kpis.recommendationsAccepted}</span>
                    <CheckCircle2 className="size-6 text-emerald-500" />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-destructive/20 bg-destructive/5">
                <CardHeader className="pb-2">
                  <p className="text-xs font-semibold text-destructive uppercase">Hype Content Filtered</p>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-3xl font-bold text-foreground">{analytics.kpis.hypeContentRejected}</span>
                    <ShieldCheck className="size-6 text-destructive" />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-amber-500/20 bg-amber-500/5">
                <CardHeader className="pb-2">
                  <p className="text-xs font-semibold text-amber-500 uppercase">Top Technical Domain</p>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-lg font-bold text-foreground truncate">{analytics.kpis.topInterest}</span>
                    <Award className="size-6 text-amber-500 shrink-0" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* BREAKDOWN CARDS */}
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <BarChart3 className="size-5 text-primary" />
                    <CardTitle className="text-base">Category Distribution</CardTitle>
                  </div>
                  <CardDescription>Recommended technology domains</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {analytics.categoryDistribution.map((item, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-xs font-medium">
                        <span>{item.category}</span>
                        <span className="font-mono text-muted-foreground">{item.value}%</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                        <div
                          className="h-full bg-primary rounded-full transition-all"
                          style={{ width: `${item.value}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="size-5 text-emerald-500" />
                    <CardTitle className="text-base">Educational Depth Ratio</CardTitle>
                  </div>
                  <CardDescription>Educational content vs hype score</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {analytics.educationalValue.map((item, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-xs font-medium">
                        <span>{item.label}</span>
                        <span className="font-mono text-muted-foreground">{item.value}%</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full transition-all"
                          style={{ width: `${item.value}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
