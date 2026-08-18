// ============================================================================
// AlgoShift AI — Domain types
// Maps 1:1 to FastAPI backend models & responses.
// ============================================================================

export type Confidence = 'Low' | 'Medium' | 'High'
export type Difficulty = 'Beginner' | 'Intermediate' | 'Advanced'
export type InterestTrend = 'primary' | 'growing' | 'stable' | 'emerging' | 'declining'

export type Category =
  | 'AI'
  | 'DSA'
  | 'Java'
  | 'HLD'
  | 'Cybersecurity'
  | 'Cloud'
  | 'Hardware'
  | 'Career'
  | 'Backend'
  | 'Programming'
  | 'Other'

export type InputMode = 'dataset' | 'upload' | 'url'

export interface AnalyzeRequest {
  userId: string
  inputMode: InputMode
  url?: string
  reelId?: string
}

export interface ChallengeOutputResult {
  currentReel: {
    reelId: string
    title: string
  }
  interestDetected: {
    topic: string
    confidence: string
  }
  why: string
  recommendedTechReel: {
    candidateId: string
    title: string
  }
  category: Category
  whyThisRecommendation: string
  difficulty: Difficulty
  confidence: Confidence
}

export interface EvidenceTransparency {
  interestPath: string[]
  selectionFactors: string[]
}

export interface WorkflowError {
  step: string
  code: string
  message: string
}

export interface AnalyzeResponse {
  success: boolean
  runId: string
  result?: ChallengeOutputResult
  evidence?: EvidenceTransparency
  workflow: {
    status: string
    stepsCompleted?: number
    failedStep?: string
  }
  error?: WorkflowError
}

export interface RecommendationFeedbackPayload {
  userId: string
  reelId: string
  watchPercentage?: number
  liked?: boolean
  saved?: boolean
  shared?: boolean
  rewatched?: boolean
  skipped?: boolean
  completed?: boolean
}

export interface InterestTopicChange {
  topic: string
  oldScore: number
  newScore: number
  change: number
}

export interface RecommendationFeedbackResponse {
  success: boolean
  updatedInterests: InterestTopicChange[]
  message: string
}

// Legacy types retained for components
export interface Reel {
  id: string
  title: string
  thumbnailUrl?: string
  topic: string
  broaderInterest: string
  context: string
}

export interface ReelAnalysis {
  reelId: string
  title: string
  primaryTopic: string
  broaderDomain: string
  subtopics: string[]
  context: string
  intent: string
  educationalValue: number
  careerRelevance: number
  technicalDepth: number
  entertainmentValue: number
  hypeScore: number
  difficulty: Difficulty
  confidence: Confidence
  reasoning: string
}

export interface Interest {
  id: string
  name: string
  score: number
  confidence: Confidence
  trend: InterestTrend
  relatedTopics: string[]
  recentActivity: string[]
}

export interface InterestInference {
  primaryInterest: string
  supportingSignals: string[]
  note: string
}

export interface InterestGraphNode {
  id: string
  label: string
  score: number
  confidence: Confidence
  relatedTopics: string[]
  recentActivity: string[]
}

export interface InterestGraphEdge {
  from: string
  to: string
}

export interface InterestGraph {
  root: string
  nodes: InterestGraphNode[]
  edges: InterestGraphEdge[]
}

export interface InterestTimelinePoint {
  date: string
  [interestName: string]: number | string
}

export interface RecommendationScoreBreakdown {
  interestMatch: number
  educationalValue: number
  practicalUsefulness: number
  novelty: number
  interestExpansion: number
  difficultyFit: number
  careerRelevance?: number
  diversity?: number
  qualityScore?: number
}

export interface Recommendation {
  id: string
  title: string
  category: Category
  difficulty: Difficulty
  confidence: Confidence
  relevance: number
  educationalValue: number
  why: string
  recentSignals: string[]
  underlyingInterest: string
  recommendationPath: string[]
  scoreBreakdown: RecommendationScoreBreakdown
}

export interface RejectedContent {
  id: string
  title: string
  hypeScore: number
  clickbaitScore?: number
  educationalValue: number
  evidenceQuality: number
  status: 'REJECTED' | 'FILTERED'
  reason: string
}

export interface Interaction {
  reelId: string
  type: 'like' | 'watch' | 'skip' | 'save'
  timestamp: string
}

export interface FeedbackPayload {
  recommendationId: string
  feedback: 'useful' | 'more_like_this' | 'not_interested'
}

export interface HistoryEvent {
  id: string
  kind: 'reel' | 'interaction' | 'recommendation' | 'feedback' | 'interest_change'
  title: string
  description: string
  timestamp: string
}

export interface KpiSummary {
  recommendationsGenerated: number
  recommendationsAccepted: number
  usefulContentPct: number
  hypeContentRejected: number
  topInterest: string
}

export interface Analytics {
  kpis: KpiSummary
  interestEvolution: InterestTimelinePoint[]
  recommendationAcceptance: { label: string; accepted: number; rejected: number }[]
  categoryDistribution: { category: string; value: number }[]
  educationalValue: { label: string; value: number }[]
  hypeRejectionRate: { label: string; rejected: number; approved: number }[]
  difficultyDistribution: { difficulty: string; value: number }[]
}

export type AgentStatus = 'completed' | 'processing' | 'waiting' | 'rejected'

export interface AgentRun {
  id: string
  name: string
  status: AgentStatus
  summary: string
  detail: string
  durationMs?: number
}

export interface AgentPipeline {
  runId: string
  startedAt: string
  agents: AgentRun[]
}

export interface UserSettings {
  preferredDifficulty: Difficulty
  contentPreferences: Category[]
  recommendationControls: {
    moreEducational: number
    moreCareerFocused: number
    moreTechnical: number
    moreDiverse: number
  }
  hypeSensitivity: number
}
