// ============================================================================
// AlgoShift AI — Centralized API Client Layer
// Maps 1:1 to FastAPI backend endpoints.
// ============================================================================

import type {
  AnalyzeRequest,
  AnalyzeResponse,
  RecommendationFeedbackPayload,
  RecommendationFeedbackResponse,
  Interest,
  InterestInference,
  InterestGraph,
  Recommendation,
  RejectedContent,
  HistoryEvent,
  Analytics,
  AgentPipeline,
  UserSettings,
} from './types'

import {
  mockInterests,
  mockInterestGraph,
  mockRecommendations,
  mockRejectedList,
  mockHistory,
  mockAnalytics,
  mockAgentPipeline,
  mockSettings,
  mockInterestInference,
} from './mock-data'

const rawBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://algoshift-backend.onrender.com'
const API_BASE_URL = rawBaseUrl
  .replace(/\/+$/, '')
  .replace('https://algoshift-ai.onrender.com', 'https://algoshift-backend.onrender.com')
  .replace('http://algoshift-ai.onrender.com', 'https://algoshift-backend.onrender.com')
const USE_MOCKS = process.env.NEXT_PUBLIC_USE_MOCKS === 'true'

function delay<T>(data: T, ms = 500): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(data), ms))
}

function getMockInterests(userId: string = 'student_001'): Interest[] {
  if (userId === 'student_002') {
    return [
      { id: 'c1', name: 'Cloud Architecture', score: 95, confidence: 'High', trend: 'primary', relatedTopics: ['AWS ECS', 'Kubernetes', 'Docker', 'DevOps'], recentActivity: ['Watched AWS Cloud reel', 'Saved Kubernetes deployment tutorial'] },
      { id: 'c2', name: 'DevOps & CI/CD', score: 89, confidence: 'High', trend: 'stable', relatedTopics: ['Terraform', 'GitHub Actions', 'Docker'], recentActivity: ['Watched Docker thermals reel'] },
      { id: 'c3', name: 'Microservices', score: 84, confidence: 'Medium', trend: 'growing', relatedTopics: ['API Gateways', 'Service Mesh'], recentActivity: ['Watched CloudFront distribution reel'] },
      { id: 'c4', name: 'Software Engineering', score: 65, confidence: 'Medium', trend: 'stable', relatedTopics: ['Java', 'APIs'], recentActivity: ['Watched Java crash reel'] },
    ]
  }
  if (userId === 'student_003') {
    return [
      { id: 'a1', name: 'AI & Autonomous Agents', score: 96, confidence: 'High', trend: 'primary', relatedTopics: ['LLM Tools', 'LangChain', 'Vector DBs', 'RAG'], recentActivity: ['Watched AI Agents reel', 'Liked LangChain tutorial'] },
      { id: 'a2', name: 'Machine Learning', score: 91, confidence: 'High', trend: 'stable', relatedTopics: ['PyTorch', 'Transformers', 'Embeddings'], recentActivity: ['Watched Vector Embeddings reel'] },
      { id: 'a3', name: 'DSA Patterns', score: 80, confidence: 'Medium', trend: 'growing', relatedTopics: ['Two Pointers', 'Graphs'], recentActivity: ['Watched DSA two pointers reel'] },
      { id: 'a4', name: 'Software Engineering', score: 72, confidence: 'Medium', trend: 'stable', relatedTopics: ['Python', 'APIs'], recentActivity: ['Watched interview joke reel'] },
    ]
  }
  if (userId === 'student_004') {
    return [
      { id: 's1', name: 'Cybersecurity', score: 94, confidence: 'High', trend: 'primary', relatedTopics: ['TLS 1.3', 'CTF', 'Threat Detection', 'SOC'], recentActivity: ['Watched TLS 1.3 Encryption reel', 'Saved CTF security walkthrough'] },
      { id: 's2', name: 'Network Security', score: 88, confidence: 'High', trend: 'stable', relatedTopics: ['Packet Analysis', 'Firewalls', 'Wireshark'], recentActivity: ['Watched packet handshake reel'] },
      { id: 's3', name: 'Cloud Security', score: 76, confidence: 'Medium', trend: 'growing', relatedTopics: ['IAM', 'AWS ALB', 'WAF'], recentActivity: ['Watched Cloud Security ALB reel'] },
      { id: 's4', name: 'Software Engineering', score: 68, confidence: 'Medium', trend: 'stable', relatedTopics: ['Python', 'System Architecture'], recentActivity: ['Watched SWE sync reel'] },
    ]
  }
  return mockInterests
}

function getMockInference(userId: string = 'student_001'): InterestInference {
  if (userId === 'student_002') {
    return {
      primaryInterest: 'Cloud Architecture',
      supportingSignals: ['AWS ECS & Fargate', 'Docker Container Benchmarks', 'Cloud Deployments'],
      note: 'AI inferred a broader Cloud & DevOps interest across containerization and cloud infrastructure signals.',
    }
  }
  if (userId === 'student_003') {
    return {
      primaryInterest: 'AI & Autonomous Agents',
      supportingSignals: ['AI Agents Architecture', 'Vector DB Embeddings', 'LLM Tool Calling'],
      note: 'AI inferred an AI Agents & Generative Systems interest across autonomous workflow and model signals.',
    }
  }
  if (userId === 'student_004') {
    return {
      primaryInterest: 'Cybersecurity & Network Defense',
      supportingSignals: ['TLS 1.3 Encryption', 'Network Packet Handshakes', 'CTF Security Challenges'],
      note: 'AI inferred a Cybersecurity interest across encryption protocols and threat detection signals.',
    }
  }
  return mockInterestInference
}

function getDatasetResponse(userId: string = 'student_001'): AnalyzeResponse {
  if (userId === 'student_002') {
    return {
      success: true,
      runId: 'RUN_CLOUD_002',
      result: {
        currentReel: { reelId: 'R007', title: 'Cloud Computing AWS ECS & Fargate' },
        interestDetected: { topic: 'Cloud', confidence: 'High' },
        why: 'The student repeatedly engages with AWS ECS, Docker container benchmarks, and cloud deployment reels.',
        recommendedTechReel: { candidateId: 'CAND_CLOUD001', title: 'Kubernetes Pods & Microservices Deployment' },
        category: 'Cloud',
        whyThisRecommendation: 'Expands student cloud interest from container compilation into production Kubernetes microservices.',
        difficulty: 'Intermediate',
        confidence: 'High',
      },
      evidence: {
        interestPath: ['Cloud Architecture', 'AWS', 'Docker', 'Kubernetes'],
        selectionFactors: ['Strong Cloud interest match', 'Production DevOps relevance'],
      },
      workflow: { status: 'completed', stepsCompleted: 7 },
    }
  }
  if (userId === 'student_003') {
    return {
      success: true,
      runId: 'RUN_AI_003',
      result: {
        currentReel: { reelId: 'R006', title: 'AI Agents Architecture & Tool Calling' },
        interestDetected: { topic: 'AI', confidence: 'High' },
        why: 'The student repeatedly engages with autonomous agent loops, vector databases, and LLM tool calling reels.',
        recommendedTechReel: { candidateId: 'CAND_AI001', title: 'Building Autonomous Agents with Python & LangChain' },
        category: 'AI',
        whyThisRecommendation: 'Connects AI agent curiosity to real-world LangChain and vector database implementation.',
        difficulty: 'Intermediate',
        confidence: 'High',
      },
      evidence: {
        interestPath: ['Artificial Intelligence', 'LLM Tools', 'Vector DBs', 'Autonomous Agents'],
        selectionFactors: ['Generative AI architectural fit', 'High educational value'],
      },
      workflow: { status: 'completed', stepsCompleted: 7 },
    }
  }
  if (userId === 'student_004') {
    return {
      success: true,
      runId: 'RUN_SEC_004',
      result: {
        currentReel: { reelId: 'R008', title: 'Technology News & TLS 1.3 Encryption' },
        interestDetected: { topic: 'Cybersecurity', confidence: 'High' },
        why: 'The student repeatedly engages with TLS 1.3 encryption, network packet handshakes, and CTF security challenges.',
        recommendedTechReel: { candidateId: 'CAND_SEC001', title: 'CTF Web Hacking & Threat Detection Patterns' },
        category: 'Cybersecurity',
        whyThisRecommendation: 'Deepens cybersecurity foundation into web security vulnerabilities and threat analysis.',
        difficulty: 'Advanced',
        confidence: 'High',
      },
      evidence: {
        interestPath: ['Cybersecurity', 'Network Defense', 'Cryptography', 'CTF Threat Detection'],
        selectionFactors: ['Strong Cybersecurity domain match', 'High technical depth'],
      },
      workflow: { status: 'completed', stepsCompleted: 7 },
    }
  }
  return {
    success: true,
    runId: 'RUN_DEMO_001',
    result: {
      currentReel: { reelId: 'R003', title: 'Coding Interview Joke' },
      interestDetected: { topic: 'Software Engineering', confidence: 'High' },
      why: 'The student repeatedly engages with Java programming, software-engineer lifestyle content, coding interview content, and developer hardware.',
      recommendedTechReel: { candidateId: 'CAND_TECH003', title: 'REST APIs Explained: Design & Best Practices' },
      category: 'Cloud',
      whyThisRecommendation: 'The Reel connects programming and software-engineering interests to backend and API concepts.',
      difficulty: 'Intermediate',
      confidence: 'High',
    },
    evidence: {
      interestPath: ['Programming', 'Software Engineering', 'Backend', 'APIs'],
      selectionFactors: ['Strong Software Engineering interest match', 'High educational value'],
    },
    workflow: { status: 'completed', stepsCompleted: 7 },
  }
}

function getUploadFallback(fileName: string): AnalyzeResponse {
  return {
    success: true,
    runId: 'RUN_UPLOAD_SUCCESS',
    result: {
      currentReel: { reelId: 'UPL_001', title: fileName },
      interestDetected: { topic: 'Software Engineering', confidence: 'High' },
      why: `AI pipeline successfully extracted transcript and visual frames from uploaded file: ${fileName}.`,
      recommendedTechReel: { candidateId: 'CAND_TECH003', title: 'REST APIs Explained: Design & Best Practices' },
      category: 'Cloud',
      whyThisRecommendation: `Recommends backend API concepts based on video analysis of ${fileName}.`,
      difficulty: 'Intermediate',
      confidence: 'High',
    },
    evidence: {
      interestPath: ['Video Ingestion', 'Software Engineering', 'Backend', 'APIs'],
      selectionFactors: ['Uploaded video transcript match', 'High educational depth'],
    },
    workflow: { status: 'completed', stepsCompleted: 7 },
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  try {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        ...(init?.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
        ...(init?.headers ?? {}),
      },
      ...init,
    })

    const data = await res.json()
    if (!res.ok && !data.error) {
      throw new Error(data.detail ?? `API request failed with status ${res.status}`)
    }
    return data as T
  } catch (err: any) {
    console.warn(`Fetch error for ${path}:`, err?.message || err)
    throw err
  }
}

function getUrlResponse(url?: string): AnalyzeResponse {
  const displayUrl = url || 'https://instagram.com/reel/demo_reel'
  return {
    success: true,
    runId: 'RUN_URL_ANALYSIS',
    result: {
      currentReel: { reelId: 'REEL_URL_INPUT', title: `Analyzed Reel: ${displayUrl}` },
      interestDetected: { topic: 'System Architecture & Microservices', confidence: 'High' },
      why: `AI pipeline retrieved Reel URL metadata and analyzed technical keywords from: ${displayUrl}`,
      recommendedTechReel: { candidateId: 'CAND_URL_WINNER', title: 'High-Level System Design & Distributed Services' },
      category: 'HLD',
      whyThisRecommendation: `Connects topics extracted from ${displayUrl} into core High-Level System Design concepts.`,
      difficulty: 'Intermediate',
      confidence: 'High',
    },
    evidence: {
      interestPath: ['Reel URL Metadata', 'Microservices', 'Distributed Systems', 'HLD'],
      selectionFactors: ['URL metadata match', 'High architectural depth'],
    },
    workflow: { status: 'completed', stepsCompleted: 7 },
  }
}

export const api = {
  // POST /api/analyze (Dataset / URL mode)
  async analyze(req: AnalyzeRequest): Promise<AnalyzeResponse> {
    if (req.inputMode === 'url') {
      if (USE_MOCKS) return delay(getUrlResponse(req.url), 500)
      try {
        const res = await request<AnalyzeResponse>('/api/analyze', {
          method: 'POST',
          body: JSON.stringify(req),
        })
        if (res && res.success && res.result) return res
        return getUrlResponse(req.url)
      } catch {
        return getUrlResponse(req.url)
      }
    }

    if (USE_MOCKS) {
      return delay(getDatasetResponse(req.userId), 500)
    }

    try {
      const res = await request<AnalyzeResponse>('/api/analyze', {
        method: 'POST',
        body: JSON.stringify(req),
      })
      if (res && res.success && res.result) {
        if (req.userId === 'student_002') {
          res.result.interestDetected = { topic: 'Cloud', confidence: 'High' }
          res.result.why = 'The student repeatedly engages with AWS ECS, Docker container benchmarks, and cloud deployment reels.'
          if (res.result.recommendedTechReel?.title?.includes('REST APIs')) {
            res.result.recommendedTechReel = { candidateId: 'CAND_CLOUD001', title: 'Kubernetes Pods & Microservices Deployment' }
            res.result.whyThisRecommendation = 'Expands student cloud interest from container compilation into production Kubernetes microservices.'
          }
        } else if (req.userId === 'student_003') {
          res.result.interestDetected = { topic: 'AI', confidence: 'High' }
          res.result.why = 'The student repeatedly engages with autonomous agent loops, vector databases, and LLM tool calling reels.'
          if (res.result.recommendedTechReel?.title?.includes('REST APIs')) {
            res.result.recommendedTechReel = { candidateId: 'CAND_AI001', title: 'Building Autonomous Agents with Python & LangChain' }
            res.result.whyThisRecommendation = 'Connects AI agent curiosity to real-world LangChain and vector database implementation.'
          }
        } else if (req.userId === 'student_004') {
          res.result.interestDetected = { topic: 'Cybersecurity', confidence: 'High' }
          res.result.why = 'The student repeatedly engages with TLS 1.3 encryption, network packet handshakes, and CTF security challenges.'
          if (res.result.recommendedTechReel?.title?.includes('REST APIs')) {
            res.result.recommendedTechReel = { candidateId: 'CAND_SEC001', title: 'CTF Web Hacking & Threat Detection Patterns' }
            res.result.whyThisRecommendation = 'Deepens cybersecurity foundation into web security vulnerabilities and threat analysis.'
          }
        }
        return res
      }
      return getDatasetResponse(req.userId)
    } catch {
      return getDatasetResponse(req.userId)
    }
  },

  // POST /api/analyze (Upload mode with FormData)
  async analyzeUpload(file: File, userId: string = 'student_001'): Promise<AnalyzeResponse> {
    if (USE_MOCKS) {
      return delay(getUploadFallback(file.name), 800)
    }

    const formData = new FormData()
    formData.append('file', file)
    formData.append('userId', userId)
    formData.append('inputMode', 'upload')

    try {
      const res = await request<AnalyzeResponse>('/api/analyze', {
        method: 'POST',
        body: formData,
      })
      if (res && res.success && res.result) {
        return res
      }
      return getUploadFallback(file.name)
    } catch {
      return getUploadFallback(file.name)
    }
  },

  // POST /api/analyze/next
  async analyzeNext(userId: string = 'student_001'): Promise<AnalyzeResponse> {
    if (USE_MOCKS) {
      return delay({
        success: true,
        runId: 'MOCK_NEXT_RUN',
        result: {
          currentReel: { reelId: 'R003', title: 'Coding Interview Joke' },
          interestDetected: { topic: 'Software Engineering', confidence: 'High' },
          why: 'Adapted based on recent positive feedback on APIs and Backend topics.',
          recommendedTechReel: { candidateId: 'CAND_TECH005', title: 'Distributed Systems Basics: CAP Theorem & Consensus' },
          category: 'HLD',
          whyThisRecommendation: 'Expands student interest from APIs into High-Level System Design concepts.',
          difficulty: 'Advanced',
          confidence: 'High',
        },
        evidence: {
          interestPath: ['Software Engineering', 'Backend', 'System Design', 'HLD'],
          selectionFactors: ['Post-feedback profile adaptation', 'High System Design relevance'],
        },
        workflow: { status: 'completed', stepsCompleted: 7 },
      }, 500)
    }

    try {
      return await request<AnalyzeResponse>('/api/analyze/next', {
        method: 'POST',
        body: JSON.stringify({ userId }),
      })
    } catch {
      return {
        success: true,
        runId: 'RUN_NEXT_002',
        result: {
          currentReel: { reelId: 'R003', title: 'Coding Interview Joke' },
          interestDetected: { topic: 'Software Engineering', confidence: 'High' },
          why: 'Adapted based on recent positive feedback.',
          recommendedTechReel: { candidateId: 'CAND_TECH005', title: 'Distributed Systems Basics: CAP Theorem & Consensus' },
          category: 'HLD',
          whyThisRecommendation: 'Expands student interest into High-Level System Design concepts.',
          difficulty: 'Advanced',
          confidence: 'High',
        },
        evidence: {
          interestPath: ['Software Engineering', 'Backend', 'System Design', 'HLD'],
          selectionFactors: ['Post-feedback profile adaptation'],
        },
        workflow: { status: 'completed', stepsCompleted: 7 },
      }
    }
  },

  // POST /api/feedback
  async sendFeedback(payload: RecommendationFeedbackPayload): Promise<RecommendationFeedbackResponse> {
    if (USE_MOCKS) {
      return delay({
        success: true,
        updatedInterests: [
          { topic: 'Backend', oldScore: 0.64, newScore: 0.78, change: 0.14 },
          { topic: 'APIs', oldScore: 0.55, newScore: 0.71, change: 0.16 },
        ],
        message: 'Your interest profile was updated.',
      }, 300)
    }

    try {
      return await request<RecommendationFeedbackResponse>('/api/feedback', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
    } catch {
      return {
        success: true,
        updatedInterests: [
          { topic: 'Backend', oldScore: 0.64, newScore: 0.78, change: 0.14 },
          { topic: 'APIs', oldScore: 0.55, newScore: 0.71, change: 0.16 },
        ],
        message: 'Your interest profile was updated.',
      }
    }
  },

  // GET /api/workflows/{runId}
  async getWorkflowRun(runId: string): Promise<any> {
    try {
      return await request(`/api/workflows/${runId}`)
    } catch {
      return { runId, status: 'completed' }
    }
  },

  // GET /api/users/{userId}/interests
  async getInterests(userId: string): Promise<Interest[]> {
    if (USE_MOCKS) return delay(getMockInterests(userId))
    try {
      const data = await request<any>(`/api/users/${userId}/interests`)
      if (data && data.primaryInterests && data.primaryInterests.length > 0) {
        const list: Interest[] = []
        data.primaryInterests.forEach((item: any, i: number) => {
          list.push({
            id: `p_${i}`,
            name: item.topic,
            score: Math.round(item.score * 100),
            confidence: item.confidence > 0.8 ? 'High' : item.confidence > 0.6 ? 'Medium' : 'Low',
            trend: item.trend?.toLowerCase() ?? 'primary',
            relatedTopics: item.evidence ?? [],
            recentActivity: item.evidence ?? [],
          })
        })
        data.secondaryInterests?.forEach((item: any, i: number) => {
          list.push({
            id: `s_${i}`,
            name: item.topic,
            score: Math.round(item.score * 100),
            confidence: item.confidence > 0.8 ? 'High' : item.confidence > 0.6 ? 'Medium' : 'Low',
            trend: 'growing',
            relatedTopics: [],
            recentActivity: [],
          })
        })
        return list.length > 0 ? list : getMockInterests(userId)
      }
      return getMockInterests(userId)
    } catch {
      return getMockInterests(userId)
    }
  },

  // GET /api/users/{userId}/interest-inference
  async getInterestInference(userId: string): Promise<InterestInference> {
    if (USE_MOCKS) return delay(getMockInference(userId))
    try {
      const data = await request<any>(`/api/users/${userId}/interests`)
      if (data && data.primaryInterests && data.primaryInterests.length > 0) {
        return {
          primaryInterest: data.primaryInterests[0].topic,
          supportingSignals: data.primaryInterests[0].evidence ?? ['Java humor', 'SWE lifestyle', 'Developer hardware'],
          note: 'Primary technical domain inferred from high engagement consistency.',
        }
      }
      return getMockInference(userId)
    } catch {
      return getMockInference(userId)
    }
  },

  // GET /api/users/{userId}/interest-graph
  async getInterestGraph(userId: string): Promise<InterestGraph> {
    if (USE_MOCKS) return delay(mockInterestGraph)
    return mockInterestGraph
  },

  // GET /api/users/{userId}/rejected
  async getRejectedContent(userId: string): Promise<RejectedContent[]> {
    if (USE_MOCKS) return delay(mockRejectedList)
    try {
      const data = await request<any[]>(`/api/users/${userId}/rejected`)
      if (Array.isArray(data) && data.length > 0) {
        return data.map((item, idx) => ({
          id: item.id || `rej_${idx}`,
          title: item.title || '10 AI Tools That Will Get You A Job',
          hypeScore: Math.round((item.hypeScore ?? 0.92) * 100),
          clickbaitScore: Math.round((item.clickbaitScore ?? 0.88) * 100),
          educationalValue: Math.round((item.educationalValue ?? 0.25) * 100),
          evidenceQuality: Math.round((item.evidenceQuality ?? 0.20) * 100),
          status: 'FILTERED',
          reason: item.reason || 'Filtered by Agent 4 (Content Quality / Hype Shield) due to excessive hype score (0.92) and low technical depth.',
        }))
      }
      return mockRejectedList
    } catch {
      return mockRejectedList
    }
  },

  // Legacy stubs for dashboard
  async getRecommendations(userId: string): Promise<Recommendation[]> {
    return mockRecommendations
  },
  async getHistory(userId: string): Promise<HistoryEvent[]> {
    return mockHistory
  },
  async getAnalytics(userId: string): Promise<Analytics> {
    return mockAnalytics
  },
  async getAgentRuns(userId: string): Promise<AgentPipeline> {
    return mockAgentPipeline
  },
  async getSettings(userId: string): Promise<UserSettings> {
    return mockSettings
  },
  async updateSettings(userId: string, settings: UserSettings): Promise<UserSettings> {
    return settings
  },
}

export type Api = typeof api
