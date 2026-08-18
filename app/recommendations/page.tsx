'use client'

import { useState, useEffect } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { ChallengeOutputCard } from '@/components/shared/challenge-output-card'
import { RecommendationCard } from '@/components/shared/recommendation-card'
import { HypeShieldCard } from '@/components/shared/hype-shield-card'
import { LoadingState } from '@/components/shared/states'
import { api } from '@/lib/api-client'
import type { AnalyzeResponse, RejectedContent } from '@/lib/types'
import { Compass } from 'lucide-react'

export default function RecommendationsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [isNextLoading, setIsNextLoading] = useState(false)
  const [analyzeResponse, setAnalyzeResponse] = useState<AnalyzeResponse | null>(null)
  const [rejectedList, setRejectedList] = useState<RejectedContent[]>([])

  useEffect(() => {
    loadRecommendations()
  }, [])

  async function loadRecommendations() {
    setIsLoading(true)
    try {
      const [res, rej] = await Promise.all([
        api.analyze({ userId: 'student_001', inputMode: 'dataset' }),
        api.getRejectedContent('student_001'),
      ])
      setAnalyzeResponse(res)
      setRejectedList(rej)
    } catch {
      // Fallback handled by API client
    } finally {
      setIsLoading(false)
    }
  }

  async function handleDiscoverNext() {
    setIsNextLoading(true)
    try {
      const res = await api.analyzeNext('student_001')
      setAnalyzeResponse(res)
    } catch {
      // Fallback
    } finally {
      setIsNextLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Recommendations"
        description="Personalized technology reels discovered by AlgoShift AI Agents"
      />
      <div className="mx-auto w-full max-w-5xl flex-1 space-y-6 p-4 md:p-6">
        {isLoading ? (
          <LoadingState rows={2} />
        ) : (
          analyzeResponse?.result && (
            <div className="space-y-6">
              <ChallengeOutputCard result={analyzeResponse.result} />

              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Compass className="size-5 text-primary" />
                  <h2 className="text-xl font-semibold text-foreground">Selected Tech Reel Winner</h2>
                </div>
                <RecommendationCard
                  analyzeResponse={analyzeResponse}
                  onDiscoverNext={handleDiscoverNext}
                  isNextLoading={isNextLoading}
                  featured
                />
              </div>

              <HypeShieldCard rejectedItems={rejectedList} />
            </div>
          )
        )}
      </div>
    </div>
  )
}
