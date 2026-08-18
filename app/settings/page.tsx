'use client'

import { useState, useEffect } from 'react'
import { PageHeader } from '@/components/shared/page-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Slider } from '@/components/ui/slider'
import { LoadingState } from '@/components/shared/states'
import { api } from '@/lib/api-client'
import type { UserSettings } from '@/lib/types'
import { Settings, ShieldCheck, CheckCircle2, Save } from 'lucide-react'

export default function SettingsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [settings, setSettings] = useState<UserSettings | null>(null)

  useEffect(() => {
    async function loadSettings() {
      try {
        const data = await api.getSettings('student_001')
        setSettings(data)
      } catch {
        // Fallback
      } finally {
        setIsLoading(false)
      }
    }
    loadSettings()
  }, [])

  async function handleSave() {
    if (!settings) return
    setIsSaving(true)
    setSaveSuccess(false)
    try {
      await api.updateSettings('student_001', settings)
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch {
      // Fallback
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="flex min-h-svh flex-col">
      <PageHeader
        title="Settings & Curation Controls"
        description="Configure recommendation weighting, difficulty preferences, and Hype Shield sensitivity"
      />
      <div className="mx-auto w-full max-w-5xl flex-1 space-y-6 p-4 md:p-6">
        {isLoading || !settings ? (
          <LoadingState rows={2} />
        ) : (
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Settings className="size-5 text-primary" />
                <CardTitle className="text-base font-semibold">Curation Preference Controls</CardTitle>
              </div>
              <CardDescription>
                Customize how Agent 4 (Quality) and Agent 5 (Ranking) curate your feed
              </CardDescription>
            </CardHeader>

            <CardContent className="p-6 space-y-6">
              {/* PREFERRED DIFFICULTY */}
              <div className="space-y-2">
                <label className="text-sm font-semibold text-foreground">Preferred Technical Difficulty</label>
                <div className="flex flex-wrap gap-2">
                  {['Beginner', 'Intermediate', 'Advanced'].map((diff) => (
                    <Badge
                      key={diff}
                      variant={settings.preferredDifficulty === diff ? 'default' : 'outline'}
                      className="cursor-pointer px-4 py-1.5 text-xs font-medium"
                      onClick={() => setSettings({ ...settings, preferredDifficulty: diff as any })}
                    >
                      {diff}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* HYPE SENSITIVITY SLIDER */}
              <div className="space-y-3 rounded-xl border border-border p-4 bg-muted/20">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <ShieldCheck className="size-4 text-destructive" />
                    Hype Shield Sensitivity
                  </div>
                  <span className="text-xs font-mono font-bold text-destructive">
                    {Math.round(settings.hypeSensitivity * 100)}%
                  </span>
                </div>
                <Slider
                  value={[settings.hypeSensitivity * 100]}
                  onValueChange={(val) =>
                    setSettings({ ...settings, hypeSensitivity: (val[0] ?? 80) / 100 })
                  }
                  max={100}
                  step={5}
                />
                <p className="text-xs text-muted-foreground">
                  Higher sensitivity strictly filters promotional titles and viral clickbait.
                </p>
              </div>

              {saveSuccess && (
                <div className="flex items-center gap-2 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-xs text-emerald-500 font-semibold">
                  <CheckCircle2 className="size-4" />
                  Your settings were saved successfully.
                </div>
              )}

              <Button
                type="button"
                onClick={handleSave}
                disabled={isSaving}
                className="gap-2 bg-primary text-primary-foreground"
              >
                <Save className="size-4" />
                {isSaving ? 'Saving Settings...' : 'Save Settings'}
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
