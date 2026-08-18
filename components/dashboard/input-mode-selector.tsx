'use client'

import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import type { InputMode } from '@/lib/types'
import { Sparkles, Upload, Link as LinkIcon, Database, AlertCircle, FileVideo, Eye, ChevronDown, ChevronUp } from 'lucide-react'

export interface DatasetItem {
  id: string
  name: string
  targetDomain: string
  description: string
  badge: string
  reels: { id: string; title: string; topic: string; category: string; hashtags: string[] }[]
}

export const DATASETS: DatasetItem[] = [
  {
    id: 'student_001',
    name: 'Software Engineering & Java Trap',
    targetDomain: 'Software Engineering',
    badge: 'Official Competition Baseline',
    description: "Infers student_001's underlying Software Engineering interest across Java memes, SWE lifestyle, and developer hardware reels, while filtering out AI hype traps.",
    reels: [
      { id: 'R001', title: 'Java Developers at 2 AM', topic: 'Java', category: 'Java', hashtags: ['java', 'humor'] },
      { id: 'R002', title: 'Software Engineer Lifestyle', topic: 'Software Engineering', category: 'Career', hashtags: ['swe', 'wfh'] },
      { id: 'R003', title: 'Coding Interview Joke', topic: 'Coding Interviews', category: 'DSA', hashtags: ['dsa', 'interview'] },
      { id: 'R004', title: 'Laptop Comparison for Developers', topic: 'Developer Hardware', category: 'Hardware', hashtags: ['macbook', 'xps'] },
      { id: 'R010', title: '10 AI Tools That Will Get You A Job', topic: 'AI Hype Trap', category: 'Career', hashtags: ['clickbait', 'hype'] },
    ]
  },
  {
    id: 'student_002',
    name: 'Cloud Architecture & DevOps',
    targetDomain: 'Cloud',
    badge: 'Infrastructure Focus',
    description: "Infers student_002's underlying Cloud interest across AWS ECS, Kubernetes containerization, Docker thermals, and cloud network deployment.",
    reels: [
      { id: 'R007', title: 'Cloud Computing AWS ECS & Fargate', topic: 'Cloud Architecture', category: 'Cloud', hashtags: ['aws', 'kubernetes'] },
      { id: 'R004', title: 'Docker Container Compile Benchmarks', topic: 'Developer Hardware', category: 'Hardware', hashtags: ['docker', 'benchmarks'] },
      { id: 'R001', title: 'Java Production Deployment Crash', topic: 'Java', category: 'Java', hashtags: ['production', 'devops'] },
    ]
  },
  {
    id: 'student_003',
    name: 'AI Agents & Machine Learning',
    targetDomain: 'AI',
    badge: 'Generative AI Focus',
    description: "Infers student_003's underlying AI interest across autonomous agent loops, vector embeddings, LLM tool calling, and RAG architectures.",
    reels: [
      { id: 'R006', title: 'AI Agents Architecture & Tool Calling', topic: 'AI Agents', category: 'AI', hashtags: ['llm', 'ai'] },
      { id: 'R009', title: 'Two Pointer Pattern in DSA', topic: 'DSA Patterns', category: 'DSA', hashtags: ['algorithms', 'leetcode'] },
      { id: 'R003', title: 'LeetCode Hard vs Real Life', topic: 'Coding Interviews', category: 'DSA', hashtags: ['dsa', 'interview'] },
    ]
  },
  {
    id: 'student_004',
    name: 'Cybersecurity & Network Defense',
    targetDomain: 'Cybersecurity',
    badge: 'Security Focus',
    description: "Infers student_004's underlying Cybersecurity interest across TLS 1.3 encryption, network packet handshakes, CTF challenges, and threat detection.",
    reels: [
      { id: 'R008', title: 'Technology News & TLS 1.3 Encryption', topic: 'Cybersecurity', category: 'Cybersecurity', hashtags: ['security', 'tls'] },
      { id: 'R002', title: 'Software Engineer Lifestyle & Security Syncs', topic: 'Software Engineering', category: 'Career', hashtags: ['swe', 'security'] },
      { id: 'R007', title: 'Cloud Security & Application Load Balancers', topic: 'Cloud', category: 'Cloud', hashtags: ['aws', 'security'] },
    ]
  }
]

interface InputModeSelectorProps {
  onAnalyze: (mode: InputMode, urlOrId?: string, file?: File, selectedStudentId?: string) => void
  onTryDemo: () => void
  isLoading: boolean
  errorMessage?: string | null
  activeStudentId?: string
}

export function InputModeSelector({
  onAnalyze,
  onTryDemo,
  isLoading,
  errorMessage,
  activeStudentId = 'student_001',
}: InputModeSelectorProps) {
  const [activeTab, setActiveTab] = useState<InputMode>('dataset')
  const [selectedDatasetId, setSelectedDatasetId] = useState<string>(activeStudentId)
  const [showReelsPreview, setShowReelsPreview] = useState(false)

  const [urlInput, setUrlInput] = useState('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [fileError, setFileError] = useState<string | null>(null)

  const currentDataset = DATASETS.find(d => d.id === selectedDatasetId) || DATASETS[0]

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFileError(null)
    const file = e.target.files?.[0]
    if (!file) return

    const ext = file.name.split('.').pop()?.toLowerCase()
    if (ext !== 'mp4' && ext !== 'mov') {
      setFileError('Invalid file format. Please select an .mp4 or .mov file.')
      setSelectedFile(null)
      return
    }

    if (file.size > 50 * 1024 * 1024) {
      setFileError('File size exceeds maximum limit of 50MB.')
      setSelectedFile(null)
      return
    }

    setSelectedFile(file)
  }

  return (
    <Card className="border border-border bg-card shadow-sm">
      <CardContent className="p-4 md:p-6 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="space-y-1">
            <h3 className="text-lg font-semibold text-foreground">Select Analysis Input Mode</h3>
            <p className="text-xs text-muted-foreground">
              Run AlgoShift AI pipeline in competition dataset mode, upload video, or inspect reel URL.
            </p>
          </div>
          <Button
            type="button"
            variant="default"
            size="sm"
            onClick={onTryDemo}
            disabled={isLoading}
            className="gap-2 bg-gradient-to-r from-primary to-accent text-primary-foreground font-medium shadow"
          >
            <Sparkles className="size-4" />
            Try Challenge Demo
          </Button>
        </div>

        <Tabs value={activeTab} onValueChange={(val) => setActiveTab(val as InputMode)}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="dataset" className="gap-2 text-xs sm:text-sm">
              <Database className="size-4" />
              Dataset
            </TabsTrigger>
            <TabsTrigger value="upload" className="gap-2 text-xs sm:text-sm">
              <Upload className="size-4" />
              Upload Reel
            </TabsTrigger>
            <TabsTrigger value="url" className="gap-2 text-xs sm:text-sm">
              <LinkIcon className="size-4" />
              Reel URL
            </TabsTrigger>
          </TabsList>

          {/* 1. DATASET MODE */}
          <TabsContent value="dataset" className="mt-4 space-y-4">
            {/* DATASET DROPDOWN SELECTOR */}
            <div className="space-y-2">
              <label htmlFor="dataset-select" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider block">
                Select Student Interaction Dataset:
              </label>
              <div className="relative">
                <select
                  id="dataset-select"
                  value={selectedDatasetId}
                  onChange={(e) => {
                    const newId = e.target.value
                    setSelectedDatasetId(newId)
                    onAnalyze('dataset', undefined, undefined, newId)
                  }}
                  className="w-full h-11 px-3.5 pr-10 rounded-xl border border-primary/40 bg-card text-foreground text-xs sm:text-sm font-medium shadow-sm focus:outline-none focus:ring-2 focus:ring-primary transition-all cursor-pointer appearance-none"
                >
                  {DATASETS.map((ds) => (
                    <option key={ds.id} value={ds.id} className="bg-card text-foreground py-1">
                      {ds.name} ({ds.id}) — {ds.badge}
                    </option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 size-4 text-primary pointer-events-none" />
              </div>
            </div>

            {/* ACTIVE DATASET SUMMARY CARD */}
            <div className="rounded-xl border border-primary/30 bg-primary/5 p-4 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-primary">
                  <Database className="size-4" />
                  {currentDataset.name} ({currentDataset.id})
                </div>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setShowReelsPreview(!showReelsPreview)}
                  className="h-7 text-xs gap-1.5 border-primary/30 text-primary hover:bg-primary/10"
                >
                  <Eye className="size-3.5" />
                  {showReelsPreview ? 'Hide Reels' : 'Inspect Reels'} ({currentDataset.reels.length})
                  {showReelsPreview ? <ChevronUp className="size-3" /> : <ChevronDown className="size-3" />}
                </Button>
              </div>

              <p className="text-xs text-muted-foreground">{currentDataset.description}</p>

              {/* INSPECT REELS PREVIEW PANEL */}
              {showReelsPreview && (
                <div className="mt-3 pt-3 border-t border-primary/20 space-y-2">
                  <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
                    Reel Feed Items in this Dataset:
                  </p>
                  <div className="grid gap-2 sm:grid-cols-2">
                    {currentDataset.reels.map((reel) => (
                      <div key={reel.id} className="rounded-lg border border-border/80 bg-background/80 p-2.5 space-y-1 text-xs">
                        <div className="flex items-center justify-between font-medium">
                          <span className="text-foreground truncate">{reel.title}</span>
                          <span className="font-mono text-[10px] text-muted-foreground">{reel.id}</span>
                        </div>
                        <div className="flex flex-wrap gap-1 text-[10px]">
                          <span className="px-1.5 py-0.5 rounded bg-primary/10 text-primary font-medium">{reel.topic}</span>
                          <span className="px-1.5 py-0.5 rounded bg-muted text-muted-foreground">{reel.category}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <Button
              type="button"
              onClick={() => onAnalyze('dataset', undefined, undefined, selectedDatasetId)}
              disabled={isLoading}
              className="w-full gap-2 font-medium"
            >
              <Sparkles className="size-4" />
              {isLoading ? `Analyzing ${currentDataset.name}...` : `Analyze Feed (${currentDataset.name})`}
            </Button>
          </TabsContent>

          {/* 2. UPLOAD MODE */}
          <TabsContent value="upload" className="mt-4 space-y-3">
            <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-border p-6 text-center hover:border-primary/50 transition-colors">
              <FileVideo className="size-8 text-muted-foreground mb-2" />
              <p className="text-sm font-medium text-foreground">Select .mp4 or .mov video file</p>
              <p className="text-xs text-muted-foreground mt-1">Maximum file size: 50MB</p>
              <label htmlFor="file-upload-input" className="sr-only">Upload Video File</label>
              <Input
                id="file-upload-input"
                type="file"
                accept=".mp4,.mov"
                onChange={handleFileChange}
                className="mt-3 max-w-xs cursor-pointer text-xs focus-visible:ring-2 focus-visible:ring-primary"
              />
              {selectedFile && (
                <p className="mt-2 text-xs font-medium text-primary">
                  Selected: {selectedFile.name} ({(selectedFile.size / (1024 * 1024)).toFixed(1)}MB)
                </p>
              )}
            </div>

            {fileError && (
              <div className="flex items-center gap-2 rounded-md bg-destructive/10 p-3 text-xs text-destructive">
                <AlertCircle className="size-4" />
                {fileError}
              </div>
            )}

            <Button
              type="button"
              onClick={() => selectedFile && onAnalyze('upload', undefined, selectedFile, selectedDatasetId)}
              disabled={isLoading || !selectedFile}
              className="w-full gap-2 focus-visible:ring-2 focus-visible:ring-primary"
            >
              <Upload className="size-4" />
              {isLoading ? 'Uploading & Analyzing...' : 'Upload & Analyze Video'}
            </Button>
          </TabsContent>

          {/* 3. URL MODE */}
          <TabsContent value="url" className="mt-4 space-y-3">
            <div className="relative">
              <LinkIcon className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <label htmlFor="reel-url-input" className="sr-only">Reel URL</label>
              <Input
                id="reel-url-input"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://instagram.com/reel/..."
                className="pl-9 text-xs sm:text-sm focus-visible:ring-2 focus-visible:ring-primary"
              />
            </div>
            <Button
              type="button"
              onClick={() => urlInput.trim() && onAnalyze('url', urlInput.trim(), undefined, selectedDatasetId)}
              disabled={isLoading || !urlInput.trim()}
              className="w-full gap-2"
            >
              <Sparkles className="size-4" />
              {isLoading ? 'Retrieving Reel...' : 'Analyze Reel URL'}
            </Button>
          </TabsContent>
        </Tabs>

        {errorMessage && (
          <div className="flex items-start gap-2.5 rounded-lg border border-amber-500/30 bg-amber-500/10 p-3 text-xs text-amber-500">
            <AlertCircle className="size-4 shrink-0 mt-0.5" />
            <div className="space-y-0.5">
              <p className="font-medium">Analysis Note</p>
              <p>{errorMessage}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
