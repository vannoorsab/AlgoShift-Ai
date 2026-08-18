import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ScanLine, Sparkles, Database } from 'lucide-react'

interface HeroSectionProps {
  onTryDemo?: () => void
}

export function HeroSection({ onTryDemo }: HeroSectionProps) {
  return (
    <section className="relative overflow-hidden rounded-3xl border border-border bg-gradient-to-br from-primary/[0.08] via-card to-card p-8 md:p-12">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-16 -top-16 size-64 rounded-full bg-primary/10 blur-3xl"
      />
      <div className="relative max-w-2xl">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/25 bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
          <Sparkles className="size-3.5" />
          AI-powered content curation
        </span>
        <h2 className="mt-4 text-pretty text-3xl font-semibold leading-tight text-foreground md:text-4xl">
          Make every scroll a little more useful.
        </h2>
        <p className="mt-3 text-pretty text-base leading-relaxed text-muted-foreground md:text-lg">
          AI understands what you&apos;re naturally interested in and discovers technology content
          worth your time.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          {onTryDemo && (
            <Button
              size="lg"
              onClick={onTryDemo}
              className="gap-2 bg-gradient-to-r from-primary to-accent text-primary-foreground font-medium shadow-md"
            >
              <Database className="size-4" />
              Try Challenge Demo
            </Button>
          )}
          <Link href="/reel-analysis">
            <Button size="lg" variant="outline" className="gap-2">
              <ScanLine className="size-4" />
              Analyze My Reels
            </Button>
          </Link>
        </div>
      </div>
    </section>
  )
}
