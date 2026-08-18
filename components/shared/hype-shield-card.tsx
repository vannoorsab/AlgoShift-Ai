'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'
import type { RejectedContent } from '@/lib/types'
import { ShieldAlert, AlertOctagon } from 'lucide-react'

interface HypeShieldCardProps {
  rejectedItems?: RejectedContent[]
}

export function HypeShieldCard({ rejectedItems }: HypeShieldCardProps) {
  const defaultRejected: RejectedContent = {
    id: 'REJ_HYPETRAP_01',
    title: '10 AI Tools That Will Get You A Job',
    hypeScore: 92,
    clickbaitScore: 88,
    educationalValue: 25,
    evidenceQuality: 20,
    status: 'FILTERED',
    reason: 'Filtered by Agent 4 (Content Quality / Hype Shield) due to excessive hype score (92%) and low technical depth.',
  }

  const items = rejectedItems && rejectedItems.length > 0 ? rejectedItems : [defaultRejected]

  return (
    <Card className="border border-destructive/30 bg-gradient-to-br from-card via-card to-destructive/5 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="size-5 text-destructive" />
            <CardTitle className="text-base font-semibold">Hype Shield & Quality Gate</CardTitle>
          </div>
          <Badge className="bg-destructive/10 text-destructive border-destructive/20 text-xs">
            {items.length} Reels Filtered
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <Accordion className="w-full">
          <AccordionItem value="hype-shield" className="border-none">
            <AccordionTrigger className="hover:no-underline py-2 text-sm font-medium text-foreground">
              <span className="flex items-center gap-2">
                <AlertOctagon className="size-4 text-amber-500" />
                Why we filtered another Reel
              </span>
            </AccordionTrigger>
            <AccordionContent className="pt-2 space-y-4">
              {items.map((item, idx) => (
                <div key={idx} className="rounded-xl border border-destructive/20 bg-muted/20 p-4 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <p className="text-sm font-bold text-foreground">{item.title}</p>
                    <Badge variant="destructive" className="font-mono text-xs uppercase">
                      {item.status || 'FILTERED'}
                    </Badge>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="rounded-lg border border-border p-2 bg-muted/30">
                      <p className="text-muted-foreground text-[10px]">Hype</p>
                      <p className="font-bold text-destructive text-sm">{item.hypeScore}%</p>
                    </div>
                    <div className="rounded-lg border border-border p-2 bg-muted/30">
                      <p className="text-muted-foreground text-[10px]">Clickbait</p>
                      <p className="font-bold text-amber-500 text-sm">{item.clickbaitScore ?? 88}%</p>
                    </div>
                    <div className="rounded-lg border border-border p-2 bg-muted/30">
                      <p className="text-muted-foreground text-[10px]">Edu Value</p>
                      <p className="font-bold text-muted-foreground text-sm">{item.educationalValue}%</p>
                    </div>
                  </div>

                  <p className="text-xs text-muted-foreground leading-relaxed bg-background/50 p-2.5 rounded-lg border border-border/40">
                    {item.reason}
                  </p>
                </div>
              ))}
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>
  )
}
