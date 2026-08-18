import pytest

@pytest.mark.asyncio
async def test_agent1_java_meme(client):
    """TEST 1 — Java Meme"""
    payload = {
        "reelId": "R001",
        "sourceType": "demo",
        "title": "Java Developers at 2 AM",
        "caption": "When production breaks at 2 AM",
        "transcript": "The Java application worked locally but failed in production.",
        "visualDescription": "Developer debugging code."
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    analysis = res_data["analysis"]
    
    assert analysis["primaryTopic"] == "Java"
    assert "Software Engineering" in analysis["broaderDomain"]
    assert any("Programming" in s for s in analysis["subtopics"])
    assert any("Debugging" in s for s in analysis["subtopics"])

@pytest.mark.asyncio
async def test_agent1_swe_lifestyle(client):
    """TEST 2 — Software Engineer Lifestyle"""
    payload = {
        "reelId": "R002",
        "sourceType": "demo",
        "title": "Day in the Life of a Software Engineer",
        "caption": "A realistic look at my work day in tech",
        "transcript": "Morning standup, reviewing pull requests, working on backend microservices architecture.",
        "visualDescription": "Montage of modern tech office."
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    
    assert analysis["broaderDomain"] == "Software Engineering"
    assert "Developer Lifestyle" in analysis["context"] or "Career" in analysis["context"]

@pytest.mark.asyncio
async def test_agent1_laptop_comparison(client):
    """TEST 3 — Laptop Comparison"""
    payload = {
        "reelId": "R004",
        "sourceType": "demo",
        "title": "Laptop Comparison for Developers",
        "caption": "MacBook Pro M3 Max vs Dell XPS 15",
        "transcript": "Comparing compile times and thermals on MacBook Pro vs Dell XPS for software engineering workloads.",
        "visualDescription": "Side-by-side comparison of two laptops."
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    
    assert analysis["broaderDomain"] in ["Hardware", "Technology"]
    assert analysis["context"] == "Product Comparison"

@pytest.mark.asyncio
async def test_agent1_gaming(client):
    """TEST 4 — Gaming"""
    payload = {
        "reelId": "R005",
        "sourceType": "demo",
        "title": "Epic Esports Gaming Clutch",
        "caption": "Unbelievable 1v5 clutch in rank match!",
        "transcript": "One opponent left, defusing the bomb while landing a headshot through smoke for the win!",
        "visualDescription": "High energy gameplay video."
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    
    assert analysis["broaderDomain"] == "Gaming"
    assert analysis["educationalValue"] < 0.20

@pytest.mark.asyncio
async def test_agent1_ai_job_hype(client):
    """TEST 5 — AI Job Hype"""
    payload = {
        "reelId": "R010",
        "sourceType": "demo",
        "title": "10 AI Tools That Will Get You A Job",
        "caption": "SECRET AI TOOL TRICK! Get a $200k tech job automatically in 3 days!",
        "transcript": "These 10 secret AI job tools will automatically write your resume and pass all your interviews!",
        "visualDescription": "Influencer pointing frantic text overlays with dollar signs."
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    
    assert analysis["broaderDomain"] in ["AI", "Career"]
    assert analysis["hypeScore"] > 0.75
    assert analysis["clickbaitScore"] > 0.70

@pytest.mark.asyncio
async def test_agent1_cloud_tutorial(client):
    """TEST 6 — Cloud Tutorial"""
    payload = {
        "reelId": "R006",
        "sourceType": "demo",
        "title": "AWS Cloud Architecture Tutorial",
        "caption": "How to deploy a scalable containerized app on AWS ECS & CloudFront",
        "transcript": "In this step-by-step tutorial, we set up AWS ECS Fargate, Application Load Balancers, and CloudFront CDN.",
        "visualDescription": "Detailed cloud architecture diagram animation."
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    
    assert analysis["broaderDomain"] == "Cloud"
    assert analysis["intent"] == "Educate"
    assert analysis["educationalValue"] > 0.70

@pytest.mark.asyncio
async def test_agent1_url_unsupported_error(client):
    """URL ingestion returns controlled error message"""
    payload = {
        "reelId": "R999",
        "sourceType": "url",
        "sourceUrl": "https://instagram.com/reel/unknown"
    }
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 422
    err_data = response.json()
    assert "Unable to retrieve Reel content from this URL" in err_data["message"]

@pytest.mark.asyncio
async def test_agent1_manual_verification_endpoint(client):
    """GET /api/reels/{reelId} returns stored content and analysis"""
    # First analyze
    payload = {
        "reelId": "R001",
        "sourceType": "demo",
        "title": "Java Developers at 2 AM"
    }
    await client.post("/api/reels/analyze", json=payload)
    
    # Now inspect MongoDB stored record via manual verification endpoint
    get_res = await client.get("/api/reels/R001")
    assert get_res.status_code == 200
    rec = get_res.json()
    assert rec["reelId"] == "R001"
    assert "content" in rec
    assert "analysis" in rec
    assert rec["analysisVersion"] == "1.0"
