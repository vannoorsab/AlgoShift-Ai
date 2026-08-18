// ============================================================================
// TEMPORARY MOCK DATA — FOR UI DEVELOPMENT ONLY
// ----------------------------------------------------------------------------
// This entire file is throwaway demo data. When the FastAPI backend is
// connected, delete this file and wire lib/api-client.ts to real endpoints.
// Nothing here should be treated as business logic.
// ============================================================================

import type {
  Reel,
  ReelAnalysis,
  Interest,
  InterestInference,
  InterestGraph,
  InterestTimelinePoint,
  Recommendation,
  RejectedContent,
  HistoryEvent,
  Analytics,
  AgentPipeline,
  UserSettings,
} from './types'

export const MOCK_USER_ID = 'demo-user'

export const mockReels: Reel[] = [
  { id: 'r1', title: 'Java Developers at 2 AM', topic: 'Java', broaderInterest: 'Software Engineering', context: 'Developer Humor' },
  { id: 'r2', title: 'Day in the Life of a Software Engineer', topic: 'SWE Lifestyle', broaderInterest: 'Software Engineering', context: 'Career Vlog' },
  { id: 'r3', title: 'Coding Interview Joke', topic: 'Coding Interviews', broaderInterest: 'Software Engineering', context: 'Developer Humor' },
  { id: 'r4', title: 'Laptop Comparison', topic: 'Developer Hardware', broaderInterest: 'Hardware', context: 'Product Review' },
  { id: 'r5', title: 'Gaming Highlights', topic: 'Gaming', broaderInterest: 'Gaming', context: 'Entertainment' },
  { id: 'r6', title: 'What Is an API?', topic: 'APIs', broaderInterest: 'Backend', context: 'Educational' },
  { id: 'r7', title: 'Cloud Computing Explained', topic: 'Cloud', broaderInterest: 'Cloud', context: 'Educational' },
  { id: 'r8', title: 'Cybersecurity Attack Explained', topic: 'Cybersecurity', broaderInterest: 'Cybersecurity', context: 'Educational' },
  { id: 'r9', title: 'AI Agents Explained', topic: 'AI Agents', broaderInterest: 'AI', context: 'Educational' },
  { id: 'r10', title: 'DSA Interview Pattern', topic: 'DSA', broaderInterest: 'DSA', context: 'Educational' },
  { id: 'r11', title: 'System Design Basics', topic: 'HLD', broaderInterest: 'Backend', context: 'Educational' },
  { id: 'r12', title: 'Python Automation', topic: 'Python', broaderInterest: 'Programming', context: 'Tutorial' },
  { id: 'r13', title: 'Database Indexing', topic: 'Databases', broaderInterest: 'Backend', context: 'Educational' },
  { id: 'r14', title: 'DevOps Deployment', topic: 'DevOps', broaderInterest: 'Cloud', context: 'Tutorial' },
  { id: 'r15', title: 'Generic AI Job Tools', topic: 'AI Hype', broaderInterest: 'AI', context: 'Promotional' },
]

export const mockCurrentReel: Reel = mockReels[0]

export const mockReelAnalysis: ReelAnalysis = {
  reelId: 'r1',
  title: 'Java Developers at 2 AM',
  primaryTopic: 'Java',
  broaderDomain: 'Software Engineering',
  subtopics: ['Debugging', 'Developer Lifestyle', 'Backend'],
  context: 'Developer Humor',
  intent: 'Entertainment with light technical framing',
  educationalValue: 35,
  careerRelevance: 72,
  technicalDepth: 40,
  entertainmentValue: 88,
  hypeScore: 18,
  difficulty: 'Beginner',
  confidence: 'High',
  reasoning:
    'The reel uses Java-specific humor about late-night debugging. While the educational depth is low, the strong engagement with Java content signals a genuine interest in software engineering rather than a one-off joke. Career relevance is high because the humor is rooted in real developer workflows.',
}

export const mockInterests: Interest[] = [
  { id: 'i1', name: 'Software Engineering', score: 92, confidence: 'High', trend: 'primary', relatedTopics: ['Java', 'Backend', 'APIs', 'System Design'], recentActivity: ['Watched SWE lifestyle reel', 'Liked Java humor reel'] },
  { id: 'i2', name: 'Programming', score: 87, confidence: 'High', trend: 'stable', relatedTopics: ['Java', 'Python', 'Clean Code'], recentActivity: ['Watched Python automation reel'] },
  { id: 'i3', name: 'DSA', score: 73, confidence: 'Medium', trend: 'stable', relatedTopics: ['Arrays', 'Graphs', 'Interview Patterns'], recentActivity: ['Watched DSA interview pattern reel'] },
  { id: 'i4', name: 'Cloud', score: 61, confidence: 'Medium', trend: 'growing', relatedTopics: ['AWS', 'DevOps', 'Deployment'], recentActivity: ['Watched cloud computing reel'] },
  { id: 'i5', name: 'AI', score: 57, confidence: 'Medium', trend: 'emerging', relatedTopics: ['AI Agents', 'LLMs', 'Automation'], recentActivity: ['Watched AI agents reel'] },
  { id: 'i6', name: 'Hardware', score: 52, confidence: 'Low', trend: 'stable', relatedTopics: ['Laptops', 'Peripherals'], recentActivity: ['Watched laptop comparison reel'] },
]

export const mockEmergingInterests: Interest[] = [
  { id: 'i4', name: 'Cloud', score: 61, confidence: 'Medium', trend: 'growing', relatedTopics: ['AWS', 'DevOps'], recentActivity: ['Cloud computing reel'] },
  { id: 'i5', name: 'AI Agents', score: 57, confidence: 'Medium', trend: 'emerging', relatedTopics: ['LLMs', 'Automation'], recentActivity: ['AI agents reel'] },
]

export const mockDecliningInterests: Interest[] = [
  { id: 'i7', name: 'Gaming', score: 24, confidence: 'Medium', trend: 'declining', relatedTopics: ['Highlights', 'Esports'], recentActivity: ['Skipped gaming highlight reel'] },
]

export const mockNegativePreferences: Interest[] = [
  { id: 'i8', name: 'Generic AI Hype', score: 8, confidence: 'High', trend: 'declining', relatedTopics: ['Clickbait', 'AI Job Tools'], recentActivity: ['Marked "10 AI tools" reel as not interested'] },
]

export const mockInterestInference: InterestInference = {
  primaryInterest: 'Software Engineering',
  supportingSignals: ['Java', 'Coding Interviews', 'Software Engineer Lifestyle', 'Developer Hardware'],
  note: 'AI inferred a broader interest instead of relying on a single topic.',
}

export const mockInterestGraph: InterestGraph = {
  root: 'Technology',
  nodes: [
    { id: 'se', label: 'Software Engineering', score: 92, confidence: 'High', relatedTopics: ['Java', 'APIs', 'HLD'], recentActivity: ['Liked Java reel', 'Watched SWE vlog'] },
    { id: 'prog', label: 'Programming', score: 87, confidence: 'High', relatedTopics: ['Java', 'Python'], recentActivity: ['Python automation reel'] },
    { id: 'java', label: 'Java', score: 84, confidence: 'High', relatedTopics: ['Spring', 'JVM'], recentActivity: ['Java humor reel'] },
    { id: 'dsa', label: 'DSA', score: 73, confidence: 'Medium', relatedTopics: ['Graphs', 'DP'], recentActivity: ['DSA pattern reel'] },
    { id: 'backend', label: 'Backend', score: 70, confidence: 'Medium', relatedTopics: ['APIs', 'Databases'], recentActivity: ['API reel', 'Indexing reel'] },
    { id: 'cloud', label: 'Cloud', score: 61, confidence: 'Medium', relatedTopics: ['AWS', 'DevOps'], recentActivity: ['Cloud reel'] },
    { id: 'ai', label: 'AI', score: 57, confidence: 'Medium', relatedTopics: ['Agents', 'LLMs'], recentActivity: ['AI agents reel'] },
    { id: 'sec', label: 'Cybersecurity', score: 44, confidence: 'Low', relatedTopics: ['Attacks', 'Defense'], recentActivity: ['Security reel'] },
    { id: 'hw', label: 'Hardware', score: 52, confidence: 'Low', relatedTopics: ['Laptops'], recentActivity: ['Laptop reel'] },
    { id: 'career', label: 'Career', score: 66, confidence: 'Medium', relatedTopics: ['Interviews', 'Growth'], recentActivity: ['Interview reel'] },
  ],
  edges: [
    { from: 'root', to: 'se' },
    { from: 'root', to: 'prog' },
    { from: 'root', to: 'dsa' },
    { from: 'root', to: 'cloud' },
    { from: 'root', to: 'ai' },
    { from: 'root', to: 'sec' },
    { from: 'root', to: 'hw' },
    { from: 'root', to: 'career' },
    { from: 'se', to: 'java' },
    { from: 'se', to: 'backend' },
  ],
}

export const mockInterestTimeline: InterestTimelinePoint[] = [
  { date: 'Wk 1', 'Software Engineering': 60, Cloud: 20, AI: 15, Gaming: 55 },
  { date: 'Wk 2', 'Software Engineering': 68, Cloud: 28, AI: 22, Gaming: 48 },
  { date: 'Wk 3', 'Software Engineering': 74, Cloud: 35, AI: 30, Gaming: 40 },
  { date: 'Wk 4', 'Software Engineering': 81, Cloud: 44, AI: 38, Gaming: 33 },
  { date: 'Wk 5', 'Software Engineering': 87, Cloud: 53, AI: 48, Gaming: 28 },
  { date: 'Wk 6', 'Software Engineering': 92, Cloud: 61, AI: 57, Gaming: 24 },
]

export const mockRecommendations: Recommendation[] = [
  {
    id: 'rec1',
    title: 'How APIs Connect Modern Applications',
    category: 'Backend',
    difficulty: 'Intermediate',
    confidence: 'High',
    relevance: 92,
    educationalValue: 89,
    why: "You've recently engaged with programming, coding interviews, software engineering and developer hardware content. We inferred that your broader interest is Software Engineering. This Reel expands that interest into APIs and backend architecture instead of showing another generic Java Reel.",
    recentSignals: ['Java programming', 'Coding interviews', 'Software engineering', 'Developer hardware'],
    underlyingInterest: 'Software Engineering',
    recommendationPath: ['Programming', 'Backend', 'APIs'],
    scoreBreakdown: { interestMatch: 94, educationalValue: 89, novelty: 78, careerRelevance: 85, difficultyFit: 88, diversity: 72, hypePenalty: 4 },
  },
  {
    id: 'rec2',
    title: 'System Design: Designing a URL Shortener',
    category: 'HLD',
    difficulty: 'Intermediate',
    confidence: 'High',
    relevance: 88,
    educationalValue: 91,
    why: 'Your interest in backend and coding interviews suggests high-level design is a natural next step for interview preparation and deeper engineering understanding.',
    recentSignals: ['Coding interviews', 'Backend', 'Databases'],
    underlyingInterest: 'Software Engineering',
    recommendationPath: ['Backend', 'System Design', 'HLD'],
    scoreBreakdown: { interestMatch: 90, educationalValue: 91, novelty: 74, careerRelevance: 88, difficultyFit: 82, diversity: 68, hypePenalty: 6 },
  },
  {
    id: 'rec3',
    title: 'Understanding Database Indexes in 5 Minutes',
    category: 'Backend',
    difficulty: 'Beginner',
    confidence: 'Medium',
    relevance: 81,
    educationalValue: 86,
    why: 'You watched a database indexing reel and engage with backend content. This builds foundational backend knowledge relevant to interviews.',
    recentSignals: ['Databases', 'Backend'],
    underlyingInterest: 'Backend',
    recommendationPath: ['Backend', 'Databases', 'Indexing'],
    scoreBreakdown: { interestMatch: 83, educationalValue: 86, novelty: 65, careerRelevance: 79, difficultyFit: 90, diversity: 60, hypePenalty: 3 },
  },
  {
    id: 'rec4',
    title: 'How AI Agents Actually Work',
    category: 'AI',
    difficulty: 'Intermediate',
    confidence: 'Medium',
    relevance: 76,
    educationalValue: 84,
    why: 'AI is an emerging interest for you. This reel provides genuine technical depth on agent architectures without the usual hype.',
    recentSignals: ['AI agents', 'Automation'],
    underlyingInterest: 'AI',
    recommendationPath: ['AI', 'Agents', 'Architecture'],
    scoreBreakdown: { interestMatch: 78, educationalValue: 84, novelty: 82, careerRelevance: 70, difficultyFit: 80, diversity: 85, hypePenalty: 8 },
  },
  {
    id: 'rec5',
    title: 'Two Pointer Technique Explained',
    category: 'DSA',
    difficulty: 'Beginner',
    confidence: 'High',
    relevance: 84,
    educationalValue: 88,
    why: 'Your DSA interest and coding-interview signals make core patterns like two pointers highly relevant to your goals.',
    recentSignals: ['DSA patterns', 'Coding interviews'],
    underlyingInterest: 'DSA',
    recommendationPath: ['DSA', 'Patterns', 'Two Pointers'],
    scoreBreakdown: { interestMatch: 86, educationalValue: 88, novelty: 60, careerRelevance: 84, difficultyFit: 92, diversity: 55, hypePenalty: 2 },
  },
  {
    id: 'rec6',
    title: 'What Actually Happens in a TLS Handshake',
    category: 'Cybersecurity',
    difficulty: 'Advanced',
    confidence: 'Medium',
    relevance: 68,
    educationalValue: 90,
    why: 'To diversify your feed, this security topic connects to your backend interest while introducing a new domain with strong educational depth.',
    recentSignals: ['Cybersecurity', 'Backend'],
    underlyingInterest: 'Cybersecurity',
    recommendationPath: ['Security', 'Networking', 'TLS'],
    scoreBreakdown: { interestMatch: 66, educationalValue: 90, novelty: 88, careerRelevance: 72, difficultyFit: 70, diversity: 92, hypePenalty: 5 },
  },
]

export const mockRejectedContent: RejectedContent = {
  id: 'rej1',
  title: '10 AI Tools That Will Get You A Job',
  hypeScore: 94,
  educationalValue: 31,
  evidenceQuality: 25,
  status: 'REJECTED',
  reason: 'High promotional framing with low educational depth.',
}

export const mockRejectedList: RejectedContent[] = [
  mockRejectedContent,
  { id: 'rej2', title: 'This ONE Trick Makes You A 10x Developer', hypeScore: 89, educationalValue: 22, evidenceQuality: 19, status: 'REJECTED', reason: 'Unsubstantiated productivity claims with no technical evidence.' },
  { id: 'rej3', title: 'Learn To Code In 3 Days (Guaranteed Job)', hypeScore: 96, educationalValue: 15, evidenceQuality: 12, status: 'REJECTED', reason: 'Misleading timeline and guaranteed-outcome framing.' },
]

export const mockHistory: HistoryEvent[] = [
  { id: 'h1', kind: 'interaction', title: 'Liked Java Reel', description: '"Java Developers at 2 AM"', timestamp: '2026-08-18T09:12:00Z' },
  { id: 'h2', kind: 'reel', title: 'Watched coding interview Reel', description: '"Coding Interview Joke"', timestamp: '2026-08-18T08:40:00Z' },
  { id: 'h3', kind: 'interest_change', title: 'Interest in Software Engineering increased', description: '87% → 92%', timestamp: '2026-08-17T19:05:00Z' },
  { id: 'h4', kind: 'recommendation', title: 'Cloud recommendation accepted', description: '"Cloud Computing Explained"', timestamp: '2026-08-17T16:22:00Z' },
  { id: 'h5', kind: 'feedback', title: 'Marked as Not Interested', description: '"10 AI Tools That Will Get You A Job"', timestamp: '2026-08-17T11:48:00Z' },
  { id: 'h6', kind: 'reel', title: 'Watched DSA pattern Reel', description: '"DSA Interview Pattern"', timestamp: '2026-08-16T20:15:00Z' },
  { id: 'h7', kind: 'interest_change', title: 'Cloud became an emerging interest', description: '44% → 61%', timestamp: '2026-08-16T10:00:00Z' },
  { id: 'h8', kind: 'feedback', title: 'Marked as More Like This', description: '"How APIs Connect Modern Applications"', timestamp: '2026-08-15T14:30:00Z' },
]

export const mockAnalytics: Analytics = {
  kpis: {
    recommendationsGenerated: 248,
    recommendationsAccepted: 173,
    usefulContentPct: 82,
    hypeContentRejected: 41,
    topInterest: 'Software Engineering',
  },
  interestEvolution: mockInterestTimeline,
  recommendationAcceptance: [
    { label: 'Wk 1', accepted: 12, rejected: 6 },
    { label: 'Wk 2', accepted: 18, rejected: 5 },
    { label: 'Wk 3', accepted: 24, rejected: 7 },
    { label: 'Wk 4', accepted: 31, rejected: 8 },
    { label: 'Wk 5', accepted: 38, rejected: 6 },
    { label: 'Wk 6', accepted: 50, rejected: 9 },
  ],
  categoryDistribution: [
    { category: 'Backend', value: 28 },
    { category: 'DSA', value: 22 },
    { category: 'AI', value: 16 },
    { category: 'Cloud', value: 14 },
    { category: 'Java', value: 12 },
    { category: 'Security', value: 8 },
  ],
  educationalValue: [
    { label: 'Wk 1', value: 62 },
    { label: 'Wk 2', value: 68 },
    { label: 'Wk 3', value: 71 },
    { label: 'Wk 4', value: 78 },
    { label: 'Wk 5', value: 83 },
    { label: 'Wk 6', value: 88 },
  ],
  hypeRejectionRate: [
    { label: 'Wk 1', rejected: 4, approved: 14 },
    { label: 'Wk 2', rejected: 5, approved: 18 },
    { label: 'Wk 3', rejected: 7, approved: 24 },
    { label: 'Wk 4', rejected: 8, approved: 31 },
    { label: 'Wk 5', rejected: 6, approved: 38 },
    { label: 'Wk 6', rejected: 9, approved: 50 },
  ],
  difficultyDistribution: [
    { difficulty: 'Beginner', value: 34 },
    { difficulty: 'Intermediate', value: 48 },
    { difficulty: 'Advanced', value: 18 },
  ],
}

export const mockAgentPipeline: AgentPipeline = {
  runId: 'run_8f21ac',
  startedAt: '2026-08-18T09:12:04Z',
  agents: [
    { id: 'a1', name: 'ReelUnderstandingAgent', status: 'completed', summary: 'Confidence: 91%', detail: 'Parsed reel transcript and visual cues; identified Java + developer humor.', durationMs: 820 },
    { id: 'a2', name: 'InterestInferenceAgent', status: 'completed', summary: 'Software Engineering: 92%', detail: 'Aggregated recent signals into a broader interest instead of a single topic.', durationMs: 640 },
    { id: 'a3', name: 'CandidateGenerationAgent', status: 'completed', summary: '15 candidates generated', detail: 'Expanded interest into adjacent domains (APIs, HLD, DSA, Cloud).', durationMs: 1120 },
    { id: 'a4', name: 'ContentQualityAgent', status: 'rejected', summary: '5 candidates rejected', detail: 'Filtered out high-hype, low-evidence content such as "10 AI Tools...".', durationMs: 970 },
    { id: 'a5', name: 'RankingEngine', status: 'completed', summary: 'Top candidate selected', detail: 'Ranked remaining candidates by interest match, novelty and educational value.', durationMs: 410 },
    { id: 'a6', name: 'ExplanationAgent', status: 'processing', summary: 'Generating explanation', detail: 'Composing a human-readable "why this recommendation" narrative.', durationMs: undefined },
  ],
}

export const mockSettings: UserSettings = {
  preferredDifficulty: 'Intermediate',
  contentPreferences: ['AI', 'DSA', 'Java', 'Cloud', 'Career'],
  recommendationControls: {
    moreEducational: 70,
    moreCareerFocused: 60,
    moreTechnical: 55,
    moreDiverse: 45,
  },
  hypeSensitivity: 80,
}
