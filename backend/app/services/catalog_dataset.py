from typing import List, Dict, Any

CATALOG_ITEMS: List[Dict[str, Any]] = [
    {
        "contentId": "TECH001",
        "title": "Java Backend Microservices Setup",
        "category": "Backend",
        "topic": "Java",
        "description": "Building scalable Spring Boot microservices with Java.",
        "difficulty": "Intermediate",
        "topics": ["Java", "Backend", "Software Engineering"],
        "educationalValue": 0.88,
        "learningPotential": 0.85
    },
    {
        "contentId": "TECH002",
        "title": "Java Debugging Techniques for Seniors",
        "category": "Backend",
        "topic": "Java",
        "description": "Advanced JVM thread dumps and heap memory profiling.",
        "difficulty": "Advanced",
        "topics": ["Java", "Backend", "Software Engineering"],
        "educationalValue": 0.85,
        "learningPotential": 0.82
    },
    {
        "contentId": "TECH003",
        "title": "REST APIs Explained: Design & Best Practices",
        "category": "Backend",
        "topic": "APIs",
        "description": "Designing clean, RESTful APIs with OpenAPI specs and status codes.",
        "difficulty": "Intermediate",
        "topics": ["APIs", "Backend", "Software Engineering"],
        "educationalValue": 0.92,
        "learningPotential": 0.90
    },
    {
        "contentId": "TECH004",
        "title": "Database Indexing & Query Optimization",
        "category": "Databases",
        "topic": "Databases",
        "description": "How B-Trees and composite indexes speed up SQL and NoSQL queries.",
        "difficulty": "Intermediate",
        "topics": ["Databases", "Backend", "Software Engineering"],
        "educationalValue": 0.91,
        "learningPotential": 0.89
    },
    {
        "contentId": "TECH005",
        "title": "System Design Fundamentals: Load Balancers & Proxies",
        "category": "System Design",
        "topic": "System Design",
        "description": "Understanding NGINX, HAProxy, and L4 vs L7 load balancing.",
        "difficulty": "Intermediate",
        "topics": ["System Design", "Backend", "Software Engineering"],
        "educationalValue": 0.94,
        "learningPotential": 0.93
    },
    {
        "contentId": "TECH006",
        "title": "Distributed Systems Basics: CAP Theorem & Consensus",
        "category": "System Design",
        "topic": "System Design",
        "description": "Navigating trade-offs in distributed data storage systems.",
        "difficulty": "Advanced",
        "topics": ["System Design", "Backend", "Cloud"],
        "educationalValue": 0.93,
        "learningPotential": 0.92
    },
    {
        "contentId": "TECH007",
        "title": "Cloud Architecture: AWS ECS & Lambda Serverless",
        "category": "Cloud",
        "topic": "Cloud",
        "description": "Deploying scalable serverless microservices on AWS Cloud.",
        "difficulty": "Intermediate",
        "topics": ["Cloud", "DevOps", "Software Engineering"],
        "educationalValue": 0.89,
        "learningPotential": 0.88
    },
    {
        "contentId": "TECH008",
        "title": "Docker Containers & Kubernetes Orchestration",
        "category": "DevOps",
        "topic": "DevOps",
        "description": "Containerizing microservices and managing pods with Kubernetes.",
        "difficulty": "Intermediate",
        "topics": ["DevOps", "Cloud", "Software Engineering"],
        "educationalValue": 0.90,
        "learningPotential": 0.89
    },
    {
        "contentId": "TECH009",
        "title": "API Authentication with OAuth2 & JWT",
        "category": "Cybersecurity",
        "topic": "Cybersecurity",
        "description": "Implementing secure user authentication and bearer tokens.",
        "difficulty": "Intermediate",
        "topics": ["Cybersecurity", "APIs", "Backend"],
        "educationalValue": 0.87,
        "learningPotential": 0.86
    },
    {
        "contentId": "TECH010",
        "title": "Graph Data Structures & BFS/DFS Algorithms",
        "category": "DSA",
        "topic": "DSA",
        "description": "Mastering graph traversals for technical coding interviews.",
        "difficulty": "Intermediate",
        "topics": ["DSA", "Programming", "Software Engineering"],
        "educationalValue": 0.91,
        "learningPotential": 0.88
    },
    {
        "contentId": "TECH011",
        "title": "AI Agents Architecture & Orchestration",
        "category": "AI",
        "topic": "AI",
        "description": "Building autonomous multi-agent systems with tool calling.",
        "difficulty": "Intermediate",
        "topics": ["AI", "Generative AI", "Software Engineering"],
        "educationalValue": 0.88,
        "learningPotential": 0.87
    },
    {
        "contentId": "TECH012",
        "title": "LLM Fine-Tuning & RAG Pipeline Design",
        "category": "AI",
        "topic": "AI",
        "description": "Retrieval Augmented Generation using vector embeddings.",
        "difficulty": "Advanced",
        "topics": ["AI", "Machine Learning", "Databases"],
        "educationalValue": 0.90,
        "learningPotential": 0.89
    },
    {
        "contentId": "TECH013",
        "title": "Gaming Engine Physics & Shaders",
        "category": "Other",
        "topic": "Gaming",
        "description": "Building custom 3D graphics and collision engines.",
        "difficulty": "Intermediate",
        "topics": ["Gaming", "Graphics", "Programming"],
        "educationalValue": 0.65,
        "learningPotential": 0.60
    },
    {
        "contentId": "TECH014",
        "title": "Developer Setup & Ergonomic Workspace Hacks",
        "category": "Hardware",
        "topic": "Hardware",
        "description": "Optimizing developer mechanical keyboard layouts and monitor rigs.",
        "difficulty": "Beginner",
        "topics": ["Hardware", "Productivity"],
        "educationalValue": 0.70,
        "learningPotential": 0.68
    },
    {
        "contentId": "TECH015",
        "title": "System Design Interview Strategy for Tech Leaders",
        "category": "Career",
        "topic": "Career",
        "description": "How to structure 45-minute architectural interview discussions.",
        "difficulty": "Intermediate",
        "topics": ["Career", "System Design", "Software Engineering"],
        "educationalValue": 0.93,
        "learningPotential": 0.91
    },
    {
        "contentId": "TECH016",
        "title": "Python Automation Scripts for System Admins",
        "category": "Programming",
        "topic": "Python",
        "description": "Automating file management and system tasks using Python 3.",
        "difficulty": "Beginner",
        "topics": ["Python", "Programming", "DevOps"],
        "educationalValue": 0.86,
        "learningPotential": 0.84
    },
    {
        "contentId": "TECH017",
        "title": "High Performance Caching with Redis & Memcached",
        "category": "Databases",
        "topic": "Backend",
        "description": "In-memory caching patterns to reduce database latency by 90%.",
        "difficulty": "Intermediate",
        "topics": ["Backend", "Databases", "System Design"],
        "educationalValue": 0.92,
        "learningPotential": 0.90
    },
    {
        "contentId": "TECH018",
        "title": "GraphQL vs REST API Comparisons",
        "category": "Backend",
        "topic": "APIs",
        "description": "When to choose GraphQL queries over REST endpoints.",
        "difficulty": "Intermediate",
        "topics": ["APIs", "Backend", "Frontend"],
        "educationalValue": 0.88,
        "learningPotential": 0.86
    }
]
