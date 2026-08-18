from app.db.mongodb import (
    get_database,
    COLLECTION_USERS, COLLECTION_REELS, COLLECTION_INTERACTIONS,
    COLLECTION_INTEREST_PROFILES, COLLECTION_INTEREST_GRAPH, COLLECTION_INTEREST_HISTORY,
    COLLECTION_RECOMMENDATIONS, COLLECTION_RECOMMENDATION_CATALOG, COLLECTION_FEEDBACK, COLLECTION_AGENT_RUNS
)
from app.services.catalog_dataset import CATALOG_ITEMS
from app.core.logging import logger

MOCK_USER_ID = "demo-user"
ALT_USER_ID = "me"
STUDENT_USER_ID = "student_001"

STUDENT_INTERACTIONS = [
    # student_001: Software Engineering & Java Trap
    {"userId": "student_001", "reelId": "R001", "watchPercentage": 95, "liked": True, "saved": False, "shared": False, "rewatched": True, "action": "like", "timestamp": "2026-08-11T10:00:00Z"},
    {"userId": "student_001", "reelId": "R002", "watchPercentage": 100, "liked": True, "saved": True, "shared": False, "rewatched": False, "action": "save", "timestamp": "2026-08-12T11:15:00Z"},
    {"userId": "student_001", "reelId": "R003", "watchPercentage": 92, "liked": False, "saved": False, "shared": False, "rewatched": True, "action": "replay", "timestamp": "2026-08-13T14:30:00Z"},
    {"userId": "student_001", "reelId": "R004", "watchPercentage": 88, "liked": True, "saved": False, "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-14T09:20:00Z"},
    {"userId": "student_001", "reelId": "R005", "watchPercentage": 12, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "skip", "timestamp": "2026-08-15T16:45:00Z"},
    {"userId": "student_001", "reelId": "R006", "watchPercentage": 42, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "viewed", "timestamp": "2026-08-16T18:10:00Z"},
    {"userId": "student_001", "reelId": "R007", "watchPercentage": 25, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "skip", "timestamp": "2026-08-17T12:00:00Z"},
    {"userId": "student_001", "reelId": "R008", "watchPercentage": 65, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "viewed", "timestamp": "2026-08-18T08:30:00Z"},

    # student_002: Cloud Architecture & DevOps
    {"userId": "student_002", "reelId": "R007", "watchPercentage": 98, "liked": True, "saved": True, "shared": True, "rewatched": True, "action": "like", "timestamp": "2026-08-14T10:00:00Z"},
    {"userId": "student_002", "reelId": "R004", "watchPercentage": 92, "liked": True, "saved": False, "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-15T11:15:00Z"},
    {"userId": "student_002", "reelId": "R001", "watchPercentage": 85, "liked": True, "saved": False, "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-16T14:30:00Z"},
    {"userId": "student_002", "reelId": "R005", "watchPercentage": 10, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "skip", "timestamp": "2026-08-17T09:20:00Z"},

    # student_003: AI Agents & Machine Learning
    {"userId": "student_003", "reelId": "R006", "watchPercentage": 100, "liked": True, "saved": True, "shared": True, "rewatched": True, "action": "like", "timestamp": "2026-08-14T10:00:00Z"},
    {"userId": "student_003", "reelId": "R009", "watchPercentage": 88, "liked": True, "saved": False, "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-15T11:15:00Z"},
    {"userId": "student_003", "reelId": "R003", "watchPercentage": 80, "liked": True, "saved": False, "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-16T14:30:00Z"},
    {"userId": "student_003", "reelId": "R005", "watchPercentage": 15, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "skip", "timestamp": "2026-08-17T09:20:00Z"},

    # student_004: Cybersecurity & Network Defense
    {"userId": "student_004", "reelId": "R008", "watchPercentage": 96, "liked": True, "saved": True, "shared": True, "rewatched": True, "action": "like", "timestamp": "2026-08-14T10:00:00Z"},
    {"userId": "student_004", "reelId": "R002", "watchPercentage": 85, "liked": True, "saved": False, "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-15T11:15:00Z"},
    {"userId": "student_004", "reelId": "R007", "watchPercentage": 90, "liked": True, "saved": True, "shared": False, "rewatched": False, "action": "save", "timestamp": "2026-08-16T14:30:00Z"},
    {"userId": "student_004", "reelId": "R005", "watchPercentage": 0, "liked": False, "saved": False, "shared": False, "rewatched": False, "action": "skip", "timestamp": "2026-08-17T09:20:00Z"},
]

INITIAL_INTERESTS = [
    {
        "id": "i1", "userId": MOCK_USER_ID, "name": "Software Engineering", "score": 92,
        "confidence": "High", "trend": "primary",
        "relatedTopics": ["Java", "Backend", "APIs", "System Design"],
        "recentActivity": ["Watched SWE lifestyle reel", "Liked Java humor reel"]
    },
    {
        "id": "i2", "userId": MOCK_USER_ID, "name": "Programming", "score": 87,
        "confidence": "High", "trend": "stable",
        "relatedTopics": ["Java", "Python", "Clean Code"],
        "recentActivity": ["Watched Python automation reel"]
    },
    {
        "id": "i3", "userId": MOCK_USER_ID, "name": "DSA", "score": 73,
        "confidence": "Medium", "trend": "stable",
        "relatedTopics": ["Arrays", "Graphs", "Interview Patterns"],
        "recentActivity": ["Watched DSA interview pattern reel"]
    },
    {
        "id": "i4", "userId": MOCK_USER_ID, "name": "Cloud", "score": 61,
        "confidence": "Medium", "trend": "growing",
        "relatedTopics": ["AWS", "DevOps", "Deployment"],
        "recentActivity": ["Watched cloud computing reel"]
    },
    {
        "id": "i5", "userId": MOCK_USER_ID, "name": "AI", "score": 57,
        "confidence": "Medium", "trend": "emerging",
        "relatedTopics": ["AI Agents", "LLMs", "Automation"],
        "recentActivity": ["Watched AI agents reel"]
    },
    {
        "id": "i6", "userId": MOCK_USER_ID, "name": "Hardware", "score": 52,
        "confidence": "Low", "trend": "stable",
        "relatedTopics": ["Laptops", "Peripherals"],
        "recentActivity": ["Watched laptop comparison reel"]
    }
]

INITIAL_GRAPH = {
    "userId": MOCK_USER_ID,
    "root": "Technology",
    "nodes": [
        {"id": "se", "label": "Software Engineering", "score": 92, "confidence": "High", "relatedTopics": ["Java", "APIs", "HLD"], "recentActivity": ["Liked Java reel", "Watched SWE vlog"]},
        {"id": "prog", "label": "Programming", "score": 87, "confidence": "High", "relatedTopics": ["Java", "Python"], "recentActivity": ["Python automation reel"]},
        {"id": "java", "label": "Java", "score": 84, "confidence": "High", "relatedTopics": ["Spring", "JVM"], "recentActivity": ["Java humor reel"]},
        {"id": "dsa", "label": "DSA", "score": 73, "confidence": "Medium", "relatedTopics": ["Graphs", "DP"], "recentActivity": ["DSA pattern reel"]},
        {"id": "backend", "label": "Backend", "score": 70, "confidence": "Medium", "relatedTopics": ["APIs", "Databases"], "recentActivity": ["API reel", "Indexing reel"]},
        {"id": "cloud", "label": "Cloud", "score": 61, "confidence": "Medium", "relatedTopics": ["AWS", "DevOps"], "recentActivity": ["Cloud reel"]},
        {"id": "ai", "label": "AI", "score": 57, "confidence": "Medium", "relatedTopics": ["Agents", "LLMs"], "recentActivity": ["AI agents reel"]},
        {"id": "sec", "label": "Cybersecurity", "score": 44, "confidence": "Low", "relatedTopics": ["Attacks", "Defense"], "recentActivity": ["Security reel"]},
        {"id": "hw", "label": "Hardware", "score": 52, "confidence": "Low", "relatedTopics": ["Laptops"], "recentActivity": ["Laptop reel"]},
        {"id": "career", "label": "Career", "score": 66, "confidence": "Medium", "relatedTopics": ["Interviews", "Growth"], "recentActivity": ["Interview reel"]}
    ],
    "edges": [
        {"from": "root", "to": "se"},
        {"from": "root", "to": "prog"},
        {"from": "root", "to": "dsa"},
        {"from": "root", "to": "cloud"},
        {"from": "root", "to": "ai"},
        {"from": "root", "to": "sec"},
        {"from": "root", "to": "hw"},
        {"from": "root", "to": "career"},
        {"from": "se", "to": "java"},
        {"from": "se", "to": "backend"}
    ],
    "inference": {
        "primaryInterest": "Software Engineering",
        "supportingSignals": ["Java", "Coding Interviews", "Software Engineer Lifestyle", "Developer Hardware"],
        "note": "AI inferred a broader interest instead of relying on a single topic."
    }
}

INITIAL_RECOMMENDATIONS = [
    {
        "id": "rec1",
        "userId": MOCK_USER_ID,
        "title": "How APIs Connect Modern Applications",
        "category": "Backend",
        "difficulty": "Intermediate",
        "confidence": "High",
        "relevance": 92,
        "educationalValue": 89,
        "why": "We inferred that your broader interest is Software Engineering...",
        "recentSignals": ["Java programming", "Coding interviews"],
        "underlyingInterest": "Software Engineering",
        "recommendationPath": ["Programming", "Backend", "APIs"],
        "scoreBreakdown": {
            "interestMatch": 94, "educationalValue": 89, "novelty": 78,
            "careerRelevance": 85, "difficultyFit": 88, "diversity": 72, "hypePenalty": 4
        },
        "status": "APPROVED"
    }
]

INITIAL_HISTORY = [
    {"id": "h1", "userId": MOCK_USER_ID, "kind": "interaction", "title": "Liked Java Reel", "description": '"Java Developers at 2 AM"', "timestamp": "2026-08-18T09:12:00Z"}
]

async def seed_initial_data():
    try:
        db = get_database()
        
        # Seed users
        for uid in [MOCK_USER_ID, ALT_USER_ID, "student_001", "student_002", "student_003", "student_004"]:
            existing_user = await db[COLLECTION_USERS].find_one({"id": uid})
            if not existing_user:
                await db[COLLECTION_USERS].insert_one({
                    "id": uid,
                    "name": f"Student {uid.replace('student_', '')}",
                    "email": f"{uid}@demo.com",
                    "settings": {
                        "preferredDifficulty": "Intermediate",
                        "contentPreferences": ["AI", "DSA", "Java", "Cloud", "Career"],
                        "recommendationControls": {
                            "moreEducational": 70, "moreCareerFocused": 60,
                            "moreTechnical": 55, "moreDiverse": 45
                        },
                        "hypeSensitivity": 80
                    }
                })

        # Seed student interactions for all 4 students
        for interaction in STUDENT_INTERACTIONS:
            existing = await db[COLLECTION_INTERACTIONS].find_one({
                "userId": interaction["userId"],
                "reelId": interaction["reelId"]
            })
            if not existing:
                await db[COLLECTION_INTERACTIONS].insert_one(interaction)

        # Seed recommendation_catalog
        for item in CATALOG_ITEMS:
            existing = await db[COLLECTION_RECOMMENDATION_CATALOG].find_one({"contentId": item["contentId"]})
            if not existing:
                await db[COLLECTION_RECOMMENDATION_CATALOG].insert_one(item)

        logger.info("MongoDB seed check complete for users student_001 to student_004, interactions, and catalog.")
    except Exception as e:
        logger.warning(f"Seed data insertion warning: {e}")
