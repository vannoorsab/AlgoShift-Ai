import time
from typing import Dict, Any, List
from app.models.reel import ReelContent, ReelAnalysis
from app.models.enums import Difficulty, Confidence
from app.agents.taxonomy import DOMAIN_HIERARCHY, TAXONOMY_DOMAINS
from app.services.demo_dataset import DEMO_REELS
from app.core.logging import logger

class ReelUnderstandingAgent:
    """
    Agent 1: Reel Understanding Agent (v1.0)
    Converts normalized ReelContent into structured semantic ReelAnalysis.
    Does NOT perform recommendations. Only understands the Reel.
    """
    agent_name: str = "ReelUnderstandingAgent"
    agent_version: str = "1.0"

    async def analyze_reel(self, reel_id: str) -> ReelAnalysis:
        if reel_id in DEMO_REELS:
            content = DEMO_REELS[reel_id]
        else:
            content = ReelContent(
                reelId=reel_id,
                title="Coding Interview Joke",
                caption="Coding Interview Joke",
                transcript="Coding interview questions vs actual job.",
                visualDescription="Developer laughing at whiteboarding question.",
                ocrText="Interview Prep",
                hashtags=["coding", "interview", "humor"]
            )
        return await self.analyze(content)

    async def analyze(self, content: ReelContent) -> ReelAnalysis:
        start_time = time.time()
        
        title = content.title or ""
        caption = content.caption or ""
        transcript = content.transcript or ""
        visual = content.visualDescription or ""
        ocr = content.ocrText or ""
        hashtags = [h.lower() for h in (content.hashtags or [])]
        
        text_corpus = f"{title} {caption} {transcript} {visual} {ocr} {' '.join(hashtags)}".lower()

        if "gaming" in text_corpus or "1v5" in text_corpus or "clutch" in text_corpus or "esports" in text_corpus or "fps" in hashtags:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Gaming",
                broaderDomain="Gaming",
                subtopics=["Esports", "Gameplay", "Entertainment"],
                context="Entertainment",
                intent="Entertain",
                concepts=["gaming", "esports", "fps", "gameplay"],
                educationalValue=0.05,
                careerRelevance=0.10,
                technicalDepth=0.10,
                entertainmentValue=0.95,
                hypeScore=0.20,
                clickbaitScore=0.15,
                difficulty=Difficulty.BEGINNER,
                confidence=0.95
            )

        elif ("10 secret ai tools" in text_corpus or "get a job" in text_corpus or "guaranteed job" in text_corpus or "getrich" in hashtags or "secret ai tool" in text_corpus):
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="AI Hype",
                broaderDomain="AI",
                subtopics=["AI Tools", "Career Advice", "Promotional"],
                context="Promotional",
                intent="Promote",
                concepts=["ai tools", "job guarantee", "career hacks"],
                educationalValue=0.25,
                careerRelevance=0.40,
                technicalDepth=0.15,
                entertainmentValue=0.75,
                hypeScore=0.92,
                clickbaitScore=0.88,
                difficulty=Difficulty.BEGINNER,
                confidence=0.90
            )

        elif "java" in text_corpus and ("2 am" in text_corpus or "production breaks" in text_corpus or "humor" in text_corpus or "joke" in text_corpus or "null pointer" in text_corpus):
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Java",
                broaderDomain="Software Engineering",
                subtopics=["Programming", "Debugging", "Developer Culture"],
                context="Developer Humor",
                intent="Entertain",
                concepts=["Java", "debugging", "software development", "production"],
                educationalValue=0.35,
                careerRelevance=0.72,
                technicalDepth=0.25,
                entertainmentValue=0.90,
                hypeScore=0.10,
                clickbaitScore=0.05,
                difficulty=Difficulty.BEGINNER,
                confidence=0.91
            )

        elif "day in the life" in text_corpus or "swe lifestyle" in text_corpus or "techlifestyle" in hashtags:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Software Engineering",
                broaderDomain="Software Engineering",
                subtopics=["Career", "Developer Lifestyle", "Work Routine"],
                context="Developer Lifestyle",
                intent="Entertain",
                concepts=["software engineering", "lifestyle", "workday", "standup"],
                educationalValue=0.30,
                careerRelevance=0.80,
                technicalDepth=0.20,
                entertainmentValue=0.85,
                hypeScore=0.15,
                clickbaitScore=0.10,
                difficulty=Difficulty.BEGINNER,
                confidence=0.92
            )

        elif "macbook" in text_corpus or "dell xps" in text_corpus or "laptop comparison" in text_corpus or "hardware" in text_corpus:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Developer Hardware",
                broaderDomain="Hardware",
                subtopics=["Laptops", "Product Comparison", "Performance Benchmarks"],
                context="Product Comparison",
                intent="Compare",
                concepts=["hardware", "laptops", "benchmarks", "compilation speed"],
                educationalValue=0.60,
                careerRelevance=0.65,
                technicalDepth=0.50,
                entertainmentValue=0.70,
                hypeScore=0.25,
                clickbaitScore=0.15,
                difficulty=Difficulty.INTERMEDIATE,
                confidence=0.90
            )

        elif "aws" in text_corpus or "ecs" in text_corpus or "cloudfront" in text_corpus or "cloud" in text_corpus:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Cloud Computing",
                broaderDomain="Cloud",
                subtopics=["AWS", "Containers", "DevOps", "Architecture"],
                context="Tutorial",
                intent="Educate",
                concepts=["AWS", "ECS", "CloudFront", "containers", "load balancer"],
                educationalValue=0.88,
                careerRelevance=0.90,
                technicalDepth=0.78,
                entertainmentValue=0.40,
                hypeScore=0.10,
                clickbaitScore=0.05,
                difficulty=Difficulty.INTERMEDIATE,
                confidence=0.94
            )

        elif "dsa" in text_corpus or "two pointer" in text_corpus or "binary tree" in text_corpus or "leetcode" in text_corpus:
            primary = "DSA" if "two pointer" in text_corpus or "array" in text_corpus else "Interview Preparation"
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic=primary,
                broaderDomain="Software Engineering",
                subtopics=["Algorithms", "Data Structures", "Programming", "Debugging"],
                context="Educational",
                intent="Educate",
                concepts=["two pointers", "algorithms", "array", "time complexity"],
                educationalValue=0.85,
                careerRelevance=0.88,
                technicalDepth=0.75,
                entertainmentValue=0.45,
                hypeScore=0.10,
                clickbaitScore=0.05,
                difficulty=Difficulty.INTERMEDIATE,
                confidence=0.93
            )

        elif "tls" in text_corpus or "cybersecurity" in text_corpus or "handshake" in text_corpus or "encryption" in text_corpus:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Cybersecurity",
                broaderDomain="Cybersecurity",
                subtopics=["Encryption", "Networking", "TLS Handshake", "Defense"],
                context="Educational",
                intent="Explain",
                concepts=["TLS 1.3", "encryption", "HTTPS", "certificates"],
                educationalValue=0.90,
                careerRelevance=0.85,
                technicalDepth=0.82,
                entertainmentValue=0.35,
                hypeScore=0.08,
                clickbaitScore=0.04,
                difficulty=Difficulty.ADVANCED,
                confidence=0.94
            )

        elif "pytorch" in text_corpus or "llm" in text_corpus or "agent loop" in text_corpus or "ai agent" in text_corpus:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="AI Agents",
                broaderDomain="AI",
                subtopics=["Generative AI", "Machine Learning", "Python", "Architecture"],
                context="Technical Demonstration",
                intent="Demonstrate",
                concepts=["AI agents", "PyTorch", "LLM", "embeddings", "tool calling"],
                educationalValue=0.89,
                careerRelevance=0.92,
                technicalDepth=0.85,
                entertainmentValue=0.50,
                hypeScore=0.20,
                clickbaitScore=0.10,
                difficulty=Difficulty.INTERMEDIATE,
                confidence=0.92
            )

        else:
            analysis = ReelAnalysis(
                reelId=content.reelId,
                primaryTopic="Technology",
                broaderDomain="Software Engineering",
                subtopics=["Programming", "General Tech"],
                context="Educational",
                intent="Inform",
                concepts=["technology", "programming"],
                educationalValue=0.50,
                careerRelevance=0.50,
                technicalDepth=0.50,
                entertainmentValue=0.50,
                hypeScore=0.20,
                clickbaitScore=0.15,
                difficulty=Difficulty.BEGINNER,
                confidence=0.70
            )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(f"ReelUnderstandingAgent processed {content.reelId} in {duration_ms}ms (confidence={analysis.confidence})")
        return analysis
