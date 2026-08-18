'use client'

import { useState, useEffect } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { HeroSection } from '@/components/dashboard/hero-section'
import { InputModeSelector } from '@/components/dashboard/input-mode-selector'
import { AgenticProgress } from '@/components/shared/agentic-progress'
import { ChallengeOutputCard } from '@/components/shared/challenge-output-card'
import { RecommendationCard } from '@/components/shared/recommendation-card'
import { HypeShieldCard } from '@/components/shared/hype-shield-card'
import { InterestProgress } from '@/components/shared/interest-progress'
import { InterestInferenceCard } from '@/components/dashboard/interest-inference-card'
import { InterestGraph } from '@/components/shared/interest-graph'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { LoadingState } from '@/components/shared/states'
import { api } from '@/lib/api-client'
import type { AnalyzeResponse, InputMode, RejectedContent, Interest, InterestInference } from '@/lib/types'
import { ShieldCheck, Compass } from 'lucide-react'

export default function DashboardPage() {
  const [userId] = useState('student_001')
  const [isLoading, setIsLoading] = useState(false)
  const [isNextLoading, setIsNextLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const [analyzeResponse, setAnalyzeResponse] = useState<AnalyzeResponse | null>(null)
  const [rejectedList, setRejectedList] = useState<RejectedContent[]>([])
  const [interests, setInterests] = useState<Interest[]>([])
  const [inference, setInference] = useState<InterestInference | null>(null)

  // Run initial default dataset analysis on load
  useEffect(() => {
    runAnalysis('dataset')
    fetchAuxiliaryData()
  }, [])

  async function fetchAuxiliaryData() {
    try {
      const [ints, inf, rej] = await Promise.all([
        api.getInterests(userId),
        api.getInterestInference(userId),
        api.getRejectedContent(userId),
      ])
      setInterests(ints)
      setInference(inf)
      setRejectedList(rej)
    } catch {
      // Keep fallbacks
    }
  }

  async function runAnalysis(mode: InputMode, url?: string, file?: File) {
    setIsLoading(true)
    setErrorMessage(null)

    try {
      let res: AnalyzeResponse
      if (mode === 'upload' && file) {
        res = await api.analyzeUpload(file, userId)
      } else {
        res = await api.analyze({ userId, inputMode: mode, url })
      }

      setAnalyzeResponse(res)
      if (!res.success && res.error) {
        setErrorMessage(res.error.message)
      } else {
        await fetchAuxiliaryData()
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to execute recommendation workflow.')
    } finally {
      setIsLoading(false)
    }
  }

  async function handleDiscoverNext() {
    setIsNextLoading(true)
    setErrorMessage(null)

    try {
      const res = await api.analyzeNext(userId)
      setAnalyzeResponse(res)
      if (!res.success && res.error) {
        setErrorMessage(res.error.message)
      } else {
        await fetchAuxiliaryData()
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to generate next recommendation.')
    } finally {
      setIsNextLoading(false)
    }
  }

  return (
    <>
      <PageHeader title="Dashboard" description="Your personalized agentic recommendation feed" />
      <div className="mx-auto w-full max-w-6xl space-y-8 p-4 md:p-6">
        <HeroSection onTryDemo={() => runAnalysis('dataset')} />

        {/* INPUT MODE SELECTOR */}
        <InputModeSelector
          onAnalyze={(mode, url, file) => runAnalysis(mode, url, file)}
          onTryDemo={() => runAnalysis('dataset')}
          isLoading={isLoading}
          errorMessage={errorMessage}
        />

        {/* AGENTIC PROGRESS UI */}
        <AgenticProgress isLoading={isLoading} />

        {/* EXACT REQUIRED CHALLENGE OUTPUT */}
        {analyzeResponse?.result && (
          <div className="space-y-6">
            <ChallengeOutputCard result={analyzeResponse.result} />

            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Compass className="size-5 text-primary" />
                <h2 className="text-xl font-semibold text-foreground">Recommended Tech Reel</h2>
              </div>
              <RecommendationCard
                analyzeResponse={analyzeResponse}
                onDiscoverNext={handleDiscoverNext}
                isNextLoading={isNextLoading}
                featured
              />
            </div>
          </div>
        )}

        {/* HYPE SHIELD CARD */}
        <HypeShieldCard rejectedItems={rejectedList} />

        <div className="grid gap-6 lg:grid-cols-2">
          {/* INTEREST PROFILE */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Primary & Inferred Interests</CardTitle>
              <CardDescription>Inferred from your interactions</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {interests.length === 0 ? (
                <LoadingState rows={1} />
              ) : (
                interests.map((interest, i) => (
                  <InterestProgress
                    key={interest.id || i}
                    name={interest.name}
                    score={interest.score}
                    trend={interest.trend}
                    index={i}
                  />
                ))
              )}
            </CardContent>
          </Card>

          {/* INTEREST INFERENCE CARD */}
          {inference ? (
            <InterestInferenceCard inference={inference} />
          ) : (
            <LoadingState rows={1} />
          )}
        </div>
      </div>
    </>
  )
}
