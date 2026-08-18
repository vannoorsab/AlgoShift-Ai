'use client'

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { Check, ArrowRight } from 'lucide-react'

export function ReasoningPanel({
  recentSignals,
  underlyingInterest,
  recommendationPath,
  defaultOpen = false,
}: {
  recentSignals: string[]
  underlyingInterest: string
  recommendationPath: string[]
  defaultOpen?: boolean
}) {
  return (
    <Accordion
      openMultiple={false}
      defaultValue={defaultOpen ? ['why'] : []}
      className="rounded-xl border border-border bg-muted/30 px-4"
    >
      <AccordionItem value="why" className="border-none">
        <AccordionTrigger className="text-sm font-medium hover:no-underline">
          Why am I seeing this?
        </AccordionTrigger>
        <AccordionContent className="space-y-4 pb-4">
          <div>
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Recent signals
            </p>
            <ul className="grid gap-1.5 sm:grid-cols-2">
              {recentSignals.map((s) => (
                <li key={s} className="flex items-center gap-2 text-sm text-foreground">
                  <Check className="size-3.5 shrink-0 text-success" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Underlying interest
            </p>
            <p className="text-sm font-semibold text-primary">{underlyingInterest}</p>
          </div>
          <div>
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Recommendation path
            </p>
            <div className="flex flex-wrap items-center gap-2">
              {recommendationPath.map((step, i) => (
                <div key={step} className="flex items-center gap-2">
                  <span className="rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
                    {step}
                  </span>
                  {i < recommendationPath.length - 1 && (
                    <ArrowRight className="size-3.5 text-muted-foreground" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  )
}
