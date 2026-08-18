import { cn } from '@/lib/utils'
import type { AgentRun, AgentStatus as Status } from '@/lib/types'
import { Check, Loader2, Clock, X } from 'lucide-react'

const config: Record<
  Status,
  { label: string; icon: typeof Check; dot: string; text: string; ring: string }
> = {
  completed: {
    label: 'Completed',
    icon: Check,
    dot: 'bg-success text-success-foreground',
    text: 'text-success',
    ring: 'border-success/30',
  },
  processing: {
    label: 'Processing',
    icon: Loader2,
    dot: 'bg-primary text-primary-foreground',
    text: 'text-primary',
    ring: 'border-primary/40',
  },
  waiting: {
    label: 'Waiting',
    icon: Clock,
    dot: 'bg-muted text-muted-foreground',
    text: 'text-muted-foreground',
    ring: 'border-border',
  },
  rejected: {
    label: 'Filtered',
    icon: X,
    dot: 'bg-warning text-warning-foreground',
    text: 'text-warning',
    ring: 'border-warning/30',
  },
}

export function AgentStatusBadge({ status }: { status: Status }) {
  const c = config[status]
  const Icon = c.icon
  return (
    <span
      className={cn(
        'inline-flex h-6 items-center gap-1 rounded-full border px-2 text-xs font-medium',
        c.ring,
        c.text,
      )}
    >
      <Icon className={cn('size-3', status === 'processing' && 'animate-spin')} />
      {c.label}
    </span>
  )
}

export function AgentStatus({ agent, isLast }: { agent: AgentRun; isLast?: boolean }) {
  const c = config[agent.status]
  const Icon = c.icon
  return (
    <div className="flex gap-4">
      <div className="flex flex-col items-center">
        <div
          className={cn(
            'flex size-8 shrink-0 items-center justify-center rounded-full',
            c.dot,
          )}
        >
          <Icon className={cn('size-4', agent.status === 'processing' && 'animate-spin')} />
        </div>
        {!isLast && <div className="mt-1 w-px flex-1 bg-border" />}
      </div>
      <div className={cn('flex-1 pb-6', isLast && 'pb-0')}>
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-mono text-sm font-semibold text-foreground">{agent.name}</span>
          <AgentStatusBadge status={agent.status} />
          {typeof agent.durationMs === 'number' && (
            <span className="text-xs text-muted-foreground">{agent.durationMs}ms</span>
          )}
        </div>
        <p className={cn('mt-1 text-sm font-medium', c.text)}>{agent.summary}</p>
        <p className="mt-0.5 text-sm text-muted-foreground">{agent.detail}</p>
      </div>
    </div>
  )
}
