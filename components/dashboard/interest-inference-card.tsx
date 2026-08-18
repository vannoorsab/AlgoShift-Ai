import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Plus, ArrowDown, Sparkles } from 'lucide-react'
import type { InterestInference } from '@/lib/types'

export function InterestInferenceCard({ inference }: { inference: InterestInference }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">What We Think You&apos;re Interested In</CardTitle>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="flex flex-wrap items-center justify-center gap-x-2 gap-y-3">
          {inference.supportingSignals.map((signal, i) => (
            <div key={signal} className="flex items-center gap-2">
              <span className="rounded-lg border border-border bg-secondary px-3 py-1.5 text-sm font-medium text-secondary-foreground">
                {signal}
              </span>
              {i < inference.supportingSignals.length - 1 && (
                <Plus className="size-4 text-muted-foreground" />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-center">
          <ArrowDown className="size-5 text-primary" />
        </div>
        <div className="flex justify-center">
          <div className="inline-flex items-center gap-2 rounded-xl border border-primary/30 bg-primary/10 px-5 py-3">
            <Sparkles className="size-4 text-primary" />
            <span className="text-lg font-semibold text-primary">{inference.primaryInterest}</span>
          </div>
        </div>
        <p className="text-center text-sm text-muted-foreground">{inference.note}</p>
      </CardContent>
    </Card>
  )
}
