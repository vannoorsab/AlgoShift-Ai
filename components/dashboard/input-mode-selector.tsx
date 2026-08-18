'use client'

import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import type { InputMode } from '@/lib/types'
import { Sparkles, Upload, Link as LinkIcon, Database, AlertCircle, FileVideo } from 'lucide-react'

interface InputModeSelectorProps {
  onAnalyze: (mode: InputMode, urlOrId?: string, file?: File) => void
  onTryDemo: () => void
  isLoading: boolean
  errorMessage?: string | null
}

export function InputModeSelector({
  onAnalyze,
  onTryDemo,
  isLoading,
  errorMessage,
}: InputModeSelectorProps) {
  const [activeTab, setActiveTab] = useState<InputMode>('dataset')
  const [urlInput, setUrlInput] = useState('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [fileError, setFileError] = useState<string | null>(null)

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
          <TabsContent value="dataset" className="mt-4 space-y-3">
            <div className="rounded-lg border border-primary/20 bg-primary/5 p-4 space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-primary">
                <Database className="size-4" />
                Challenge Dataset (student_001)
              </div>
              <p className="text-xs text-muted-foreground">
                Infers student_001&apos;s underlying Software Engineering interest across Java memes, SWE lifestyle, and developer hardware reels, while filtering out AI hype traps.
              </p>
            </div>
            <Button
              type="button"
              onClick={() => onAnalyze('dataset')}
              disabled={isLoading}
              className="w-full gap-2"
            >
              <Sparkles className="size-4" />
              {isLoading ? 'Analyzing Feed...' : 'Analyze Feed (Dataset Mode)'}
            </Button>
          </TabsContent>

          {/* 2. UPLOAD MODE */}
          <TabsContent value="upload" className="mt-4 space-y-3">
            <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-border p-6 text-center hover:border-primary/50 transition-colors">
              <FileVideo className="size-8 text-muted-foreground mb-2" />
              <p className="text-sm font-medium text-foreground">Select .mp4 or .mov video file</p>
              <p className="text-xs text-muted-foreground mt-1">Maximum file size: 50MB</p>
              <Input
                type="file"
                accept=".mp4,.mov"
                onChange={handleFileChange}
                className="mt-3 max-w-xs cursor-pointer text-xs"
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
              onClick={() => selectedFile && onAnalyze('upload', undefined, selectedFile)}
              disabled={isLoading || !selectedFile}
              className="w-full gap-2"
            >
              <Upload className="size-4" />
              {isLoading ? 'Uploading & Analyzing...' : 'Upload & Analyze Video'}
            </Button>
          </TabsContent>

          {/* 3. URL MODE */}
          <TabsContent value="url" className="mt-4 space-y-3">
            <div className="relative">
              <LinkIcon className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://instagram.com/reel/..."
                className="pl-9 text-xs sm:text-sm"
              />
            </div>
            <Button
              type="button"
              onClick={() => urlInput.trim() && onAnalyze('url', urlInput.trim())}
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
