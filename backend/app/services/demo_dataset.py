from typing import Dict, List
from app.models.reel import ReelContent
from app.models.enums import SourceType

DEMO_REELS: Dict[str, ReelContent] = {
    "R001": ReelContent(
        reelId="R001",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Java Developers at 2 AM",
        caption="When production breaks at 2 AM 😂",
        hashtags=["java", "developer", "coding", "humor"],
        transcript="The Java application worked perfectly on my local environment, but when we deployed to production at 2 AM, null pointer exceptions exploded everywhere.",
        visualDescription="A software engineer sitting in a dark room debugging code on a laptop screen with coffee cups around.",
        ocrText="JAVA DEVELOPER AT 2 AM"
    ),
    "R002": ReelContent(
        reelId="R002",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Software Engineer Lifestyle",
        caption="A realistic look at my work day in tech 💻✨",
        hashtags=["softwareengineer", "techlifestyle", "wfh", "office"],
        transcript="Morning standup at 9:30 AM, reviewing pull requests, working on backend microservices architecture, grabbing iced matcha, and team syncs.",
        visualDescription="Montage of modern tech office, mechanical keyboard typing, coffee pouring, and code review comments.",
        ocrText="DAY IN THE LIFE: SWE"
    ),
    "R003": ReelContent(
        reelId="R003",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Coding Interview Joke",
        caption="Interviewer: Can you invert a binary tree? Me: 💀",
        hashtags=["codinginterview", "dsa", "devjoke", "leetcode"],
        transcript="Interviewer asks me to reverse a linked list and balance a binary tree on a whiteboard in 5 minutes while I just memorized array formulas.",
        visualDescription="Comedian developer acting out an awkward interview room scene sweating in front of a whiteboard.",
        ocrText="LEETCODE HARD VS REAL LIFE"
    ),
    "R004": ReelContent(
        reelId="R004",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Laptop Comparison for Developers",
        caption="MacBook Pro M3 Max vs Dell XPS 15 for software development",
        hashtags=["hardware", "macbook", "dell", "techreview"],
        transcript="Comparing compile times, battery efficiency, thermals, and Docker container performance on MacBook Pro vs Dell XPS for software engineering workloads.",
        visualDescription="Side-by-side comparison of two laptops running code compilation benchmarks and render tests.",
        ocrText="BEST DEVELOPER LAPTOP 2026"
    ),
    "R005": ReelContent(
        reelId="R005",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Gaming Highlights",
        caption="Unbelievable 1v5 clutch in rank match! 🔥🎮",
        hashtags=["gaming", "esports", "clutch", "fps"],
        transcript="One opponent left, 10 seconds on the clock, defusing the bomb while landing a headshot through smoke for the win!",
        visualDescription="High energy first-person shooter gameplay video with gaming overlay and reaction webcam.",
        ocrText="1v5 CLUTCH WIN"
    ),
    "R006": ReelContent(
        reelId="R006",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="AI Agents Explained",
        caption="Deep dive into autonomous agent loop and tool calling architecture",
        hashtags=["ai", "generativeai", "llm", "python"],
        transcript="Understanding how autonomous AI agents execute planning loops, invoke tools via function calling, and maintain short-term memory using vector embeddings.",
        visualDescription="Python code walkthrough showing AI agent orchestrator execution loop and terminal output.",
        ocrText="AI AGENT ARCHITECTURE DEMO"
    ),
    "R007": ReelContent(
        reelId="R007",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Cloud Computing Explained",
        caption="How to deploy a scalable containerized app on AWS ECS & CloudFront",
        hashtags=["cloud", "aws", "devops", "architecture"],
        transcript="In this step-by-step tutorial, we set up AWS ECS Fargate, configure Application Load Balancers, route traffic via CloudFront CDN, and monitor with CloudWatch.",
        visualDescription="Detailed cloud infrastructure diagram animation highlighting AWS service icons and traffic flow.",
        ocrText="AWS ECS CONTAINER TUTORIAL"
    ),
    "R008": ReelContent(
        reelId="R008",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Technology News & Security",
        caption="Latest tech news: HTTPS encryption and TLS 1.3 updates",
        hashtags=["technews", "cybersecurity", "security", "tech"],
        transcript="Explaining asymmetric key exchange, digital certificates, cipher suite negotiation, and how TLS 1.3 prevents interception during HTTP transport.",
        visualDescription="Animated security diagram illustrating client and server key exchange packets across a network.",
        ocrText="CYBERSECURITY: TLS 1.3 EXPLAINED"
    ),
    "R009": ReelContent(
        reelId="R009",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="Two Pointer Technique in DSA",
        caption="Master this pattern to solve 80% of array interview questions",
        hashtags=["dsa", "algorithms", "leetcode", "interviewprep"],
        transcript="The two pointer pattern uses left and right pointers converging from both ends of a sorted array to achieve O(n) linear time complexity.",
        visualDescription="Animated pointer movement sliding across an array data structure visualizer with Big-O complexity callouts.",
        ocrText="DSA PATTERN: TWO POINTERS"
    ),
    "R010": ReelContent(
        reelId="R010",
        sourceType=SourceType.DEMO,
        sourceUrl=None,
        title="10 AI Tools That Will Get You A Job",
        caption="SECRET AI TOOL TRICK! Get a $200k tech job automatically in 3 days! 🚀🔥",
        hashtags=["ai", "aitools", "careerhack", "getrich"],
        transcript="These 10 secret AI job tools will automatically write your resume, apply to 500 tech companies, and pass all your interviews without coding!",
        visualDescription="High energy influencer pointing frantically at text overlays with dollar signs and shiny AI app logos.",
        ocrText="10 SECRET AI TOOLS GUARANTEED JOB"
    )
}

def get_demo_reel(reel_id: str) -> ReelContent:
    return DEMO_REELS.get(reel_id, DEMO_REELS["R001"])
