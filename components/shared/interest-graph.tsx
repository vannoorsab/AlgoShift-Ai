'use client'

import { useMemo, useState } from 'react'
import { cn } from '@/lib/utils'
import type { InterestGraph as Graph, InterestGraphNode } from '@/lib/types'
import { ConfidenceBadge } from './badges'
import { Sparkles } from 'lucide-react'

export function InterestGraph({ graph }: { graph: Graph }) {
  // Only place the top-level nodes (connected to root) radially; keep it clean.
  const rootChildren = useMemo(
    () => graph.edges.filter((e) => e.from === 'root').map((e) => e.to),
    [graph.edges],
  )
  const nodes = useMemo(
    () => graph.nodes.filter((n) => rootChildren.includes(n.id)),
    [graph.nodes, rootChildren],
  )
  const [selectedId, setSelectedId] = useState<string>(nodes[0]?.id ?? '')
  const selected: InterestGraphNode | undefined =
    graph.nodes.find((n) => n.id === selectedId) ?? nodes[0]

  const positions = useMemo(() => {
    const n = nodes.length
    return nodes.map((node, i) => {
      const angle = (i / n) * Math.PI * 2 - Math.PI / 2
      const radius = 42 // percent
      return {
        node,
        left: 50 + radius * Math.cos(angle),
        top: 50 + radius * Math.sin(angle),
      }
    })
  }, [nodes])

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="relative aspect-square w-full max-w-[520px] justify-self-center rounded-2xl border border-border bg-gradient-to-b from-muted/30 to-card">
        <svg className="absolute inset-0 h-full w-full" aria-hidden="true">
          {positions.map((p) => (
            <line
              key={p.node.id}
              x1="50%"
              y1="50%"
              x2={`${p.left}%`}
              y2={`${p.top}%`}
              className={cn(
                'stroke-border transition-colors',
                p.node.id === selectedId && 'stroke-primary/60',
              )}
              strokeWidth={p.node.id === selectedId ? 2 : 1}
            />
          ))}
        </svg>

        {/* Root */}
        <div className="absolute left-1/2 top-1/2 flex size-20 -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full border border-primary/40 bg-primary/15 text-center">
          <Sparkles className="size-4 text-primary" />
          <span className="mt-0.5 text-xs font-semibold text-primary">{graph.root}</span>
        </div>

        {/* Nodes */}
        {positions.map((p) => {
          const active = p.node.id === selectedId
          return (
            <button
              key={p.node.id}
              type="button"
              onClick={() => setSelectedId(p.node.id)}
              style={{ left: `${p.left}%`, top: `${p.top}%` }}
              className={cn(
                'absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full border text-center transition-all',
                'size-16 hover:scale-105',
                active
                  ? 'border-primary bg-primary/20 ring-4 ring-primary/20'
                  : 'border-border bg-card hover:border-primary/40',
              )}
            >
              <span
                className={cn(
                  'px-1 text-[10px] font-medium leading-tight',
                  active ? 'text-primary' : 'text-foreground',
                )}
              >
                {p.node.label}
              </span>
              <span className="font-mono text-[10px] text-muted-foreground">{p.node.score}%</span>
            </button>
          )
        })}
      </div>

      {/* Detail panel */}
      {selected && (
        <div className="rounded-2xl border border-border bg-card p-5">
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-xs uppercase tracking-wide text-muted-foreground">Interest</p>
              <h3 className="text-lg font-semibold text-foreground">{selected.label}</h3>
            </div>
            <div className="text-right">
              <p className="text-xs text-muted-foreground">Score</p>
              <p className="font-mono text-2xl font-semibold text-primary">{selected.score}%</p>
            </div>
          </div>
          <div className="mt-3">
            <ConfidenceBadge value={selected.confidence} />
          </div>
          <div className="mt-4">
            <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Related topics
            </p>
            <div className="flex flex-wrap gap-1.5">
              {selected.relatedTopics.map((t) => (
                <span
                  key={t}
                  className="rounded-md bg-secondary px-2 py-0.5 text-xs text-secondary-foreground"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
          <div className="mt-4">
            <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Recent activity
            </p>
            <ul className="space-y-1">
              {selected.recentActivity.map((a) => (
                <li key={a} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-primary/60" />
                  {a}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
