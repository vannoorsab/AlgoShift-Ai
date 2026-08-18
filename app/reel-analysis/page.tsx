'use client'

import { useState } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { InputModeSelector } from '@/components/dashboard/input-mode-selector'
import { AgenticProgress } from '@/components/shared/agentic-progress'
import { ChallengeOutputCard } from '@/components/shared/challenge-output-card'
import { RecommendationCard } from '@/components/shared/recommendation-card'
import { api } from '@/lib/api-client'
import type { AnalyzeResponse, InputMode } from '@/lib/types'

export default function ReelAnalysisPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [resultResponse, setResultResponse] = useState<AnalyzeResponse | null>(null)

  async function handleAnalyze(mode: InputMode, url?: string, file?: File) {
    setIsLoading(true)
    setErrorMessage(null)
    setResultResponse(null)

    try {
      let res: AnalyzeResponse
      if (mode === 'upload' && file) {
        res = await api.analyzeUpload(file, 'student_001')
      } else {
        res = await api.analyze({ userId: 'student_001', inputMode: mode, url })
      }

      setResultResponse(res)
      if (!res.success && res.error) {
        setErrorMessage(res.error.message || 'Unable to retrieve this Reel. Please upload the video instead.')
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Unable to retrieve this Reel. Please upload the video instead.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Reel Analysis"
        description="Break down any reel into topics, intent, quality signals, and recommendations"
      />
      <div className="mx-auto w-full max-w-5xl flex-1 space-y-6 p-4 md:p-6">
        <InputModeSelector
          onAnalyze={handleAnalyze}
          onTryDemo={() => handleAnalyze('dataset')}
          isLoading={isLoading}
          errorMessage={errorMessage}
        />

        <AgenticProgress isLoading={isLoading} />

        {resultResponse?.result && (
          <div className="space-y-6 pt-4">
            <ChallengeOutputCard result={resultResponse.result} />
            <RecommendationCard analyzeResponse={resultResponse} />
          </div>
        )}
      </div>
    </div>
  )
}
