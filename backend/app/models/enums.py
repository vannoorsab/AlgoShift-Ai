from enum import Enum

class SourceType(str, Enum):
    DEMO = "demo"
    UPLOAD = "upload"
    URL = "url"

class Confidence(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Difficulty(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class InterestTrend(str, Enum):
    PRIMARY = "primary"
    GROWING = "growing"
    STABLE = "stable"
    EMERGING = "emerging"
    DECLINING = "declining"

class Category(str, Enum):
    AI = "AI"
    GENERATIVE_AI = "Generative AI"
    MACHINE_LEARNING = "Machine Learning"
    PROGRAMMING = "Programming"
    JAVA = "Java"
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    DSA = "DSA"
    HLD = "HLD"
    SOFTWARE_ENGINEERING = "Software Engineering"
    BACKEND = "Backend"
    FRONTEND = "Frontend"
    FULL_STACK = "Full Stack"
    APIS = "APIs"
    DATABASES = "Databases"
    SYSTEM_DESIGN = "System Design"
    CLOUD = "Cloud"
    DEVOPS = "DevOps"
    CYBERSECURITY = "Cybersecurity"
    NETWORKING = "Networking"
    HARDWARE = "Hardware"
    DEVELOPER_TOOLS = "Developer Tools"
    CAREER = "Career"
    INTERVIEW_PREPARATION = "Interview Preparation"
    TECHNOLOGY_NEWS = "Technology News"
    GAMING = "Gaming"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"

class ReelContextEnum(str, Enum):
    EDUCATIONAL = "Educational"
    ENTERTAINMENT = "Entertainment"
    DEVELOPER_HUMOR = "Developer Humor"
    TUTORIAL = "Tutorial"
    CAREER = "Career"
    TECHNOLOGY_NEWS = "Technology News"
    PRODUCT_REVIEW = "Product Review"
    PRODUCT_COMPARISON = "Product Comparison"
    DEVELOPER_LIFESTYLE = "Developer Lifestyle"
    TECHNICAL_DEMONSTRATION = "Technical Demonstration"
    OPINION = "Opinion"
    PROMOTIONAL = "Promotional"
    MOTIVATIONAL = "Motivational"
    OTHER = "Other"

class ReelIntentEnum(str, Enum):
    EDUCATE = "Educate"
    ENTERTAIN = "Entertain"
    INFORM = "Inform"
    PROMOTE = "Promote"
    INSPIRE = "Inspire"
    EXPLAIN = "Explain"
    COMPARE = "Compare"
    DEMONSTRATE = "Demonstrate"
    DISCUSS = "Discuss"

class FeedbackType(str, Enum):
    USEFUL = "useful"
    MORE_LIKE_THIS = "more_like_this"
    NOT_INTERESTED = "not_interested"

class InteractionType(str, Enum):
    LIKE = "like"
    WATCH = "watch"
    SKIP = "skip"
    SAVE = "save"

class HistoryEventKind(str, Enum):
    REEL = "reel"
    INTERACTION = "interaction"
    RECOMMENDATION = "recommendation"
    FEEDBACK = "feedback"
    INTEREST_CHANGE = "interest_change"

class AgentStatus(str, Enum):
    COMPLETED = "completed"
    PROCESSING = "processing"
    WAITING = "waiting"
    REJECTED = "rejected"
