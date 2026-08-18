import type { ReactNode } from 'react'
import { SidebarTrigger } from '@/components/ui/sidebar'
import { Separator } from '@/components/ui/separator'

export function PageHeader({
  title,
  description,
  actions,
}: {
  title: string
  description?: string
  actions?: ReactNode
}) {
  return (
    <header className="sticky top-0 z-10 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="flex items-center gap-3 px-4 py-3 md:px-6">
        <SidebarTrigger className="md:hidden" />
        <Separator orientation="vertical" className="h-5 md:hidden" />
        <div className="min-w-0 flex-1">
          <h1 className="truncate text-lg font-semibold text-foreground">{title}</h1>
          {description && (
            <p className="truncate text-sm text-muted-foreground">{description}</p>
          )}
        </div>
        {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
      </div>
    </header>
  )
}
