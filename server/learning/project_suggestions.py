"""
Project Suggestions Module

Provides intelligent project recommendations based on:
- Skills the user wants to learn
- Career goals (e.g., job interviews, portfolio)
- Current skill level
- Time availability

Each project is designed to be portfolio-ready for GitHub.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import json
from pathlib import Path


class SkillCategory(Enum):
    """Categories of skills that can be learned."""
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DATABASE = "database"
    DEVOPS = "devops"
    MOBILE = "mobile"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"
    SECURITY = "security"
    TESTING = "testing"
    ARCHITECTURE = "architecture"
    API_DESIGN = "api_design"
    CLOUD = "cloud"
    SYSTEMS = "systems"


class CareerGoal(Enum):
    """Common career goals for project preparation."""
    FRONTEND_JOB = "frontend_job"
    BACKEND_JOB = "backend_job"
    FULLSTACK_JOB = "fullstack_job"
    DATA_ENGINEER = "data_engineer"
    ML_ENGINEER = "ml_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    MOBILE_DEVELOPER = "mobile_developer"
    FREELANCE = "freelance"
    STARTUP = "startup"
    PORTFOLIO = "portfolio"
    OPEN_SOURCE = "open_source"
    INTERVIEW_PREP = "interview_prep"


class DifficultyLevel(Enum):
    """Project difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class ProjectSuggestion:
    """A portfolio-ready project suggestion."""
    id: str
    name: str
    description: str
    tagline: str  # Short catchy description for GitHub

    # What this project teaches
    primary_skills: list[str]
    secondary_skills: list[str]
    technologies: list[str]
    concepts_taught: list[str]

    # Categorization
    categories: list[SkillCategory]
    difficulty: DifficultyLevel
    estimated_hours: float

    # Career relevance
    career_goals: list[CareerGoal]
    interview_topics: list[str]  # Topics commonly asked in interviews

    # Portfolio appeal
    portfolio_score: int  # 1-10, how impressive for portfolio
    github_appeal: list[str]  # What makes it stand out on GitHub
    real_world_use: str  # Real-world application

    # Project structure
    suggested_features: list[str]
    stretch_goals: list[str]  # Optional advanced features

    # Prerequisites
    prerequisites: list[str]

    # Metadata
    language: str
    frameworks: list[str]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tagline": self.tagline,
            "primary_skills": self.primary_skills,
            "secondary_skills": self.secondary_skills,
            "technologies": self.technologies,
            "concepts_taught": self.concepts_taught,
            "categories": [c.value for c in self.categories],
            "difficulty": self.difficulty.value,
            "estimated_hours": self.estimated_hours,
            "career_goals": [g.value for g in self.career_goals],
            "interview_topics": self.interview_topics,
            "portfolio_score": self.portfolio_score,
            "github_appeal": self.github_appeal,
            "real_world_use": self.real_world_use,
            "suggested_features": self.suggested_features,
            "stretch_goals": self.stretch_goals,
            "prerequisites": self.prerequisites,
            "language": self.language,
            "frameworks": self.frameworks,
        }


# ============================================================================
# PROJECT CATALOG - Portfolio-Ready Projects
# ============================================================================

PROJECT_CATALOG: list[ProjectSuggestion] = [
    # -------------------------------------------------------------------------
    # BACKEND PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="rest-api-auth",
        name="RESTful API with Authentication",
        description="Build a production-ready REST API with JWT authentication, role-based access control, and proper error handling. Perfect for learning API design patterns used in real companies.",
        tagline="Production-ready REST API with JWT auth and RBAC",
        primary_skills=["REST API Design", "Authentication", "Authorization"],
        secondary_skills=["Database Design", "Error Handling", "Testing"],
        technologies=["JWT", "OAuth2", "PostgreSQL", "Redis"],
        concepts_taught=[
            "RESTful principles", "JWT tokens", "Password hashing",
            "Role-based access control", "API versioning", "Rate limiting"
        ],
        categories=[SkillCategory.BACKEND, SkillCategory.API_DESIGN, SkillCategory.SECURITY],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=25,
        career_goals=[CareerGoal.BACKEND_JOB, CareerGoal.FULLSTACK_JOB, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "How does JWT work?", "Token refresh strategies",
            "Password storage best practices", "RBAC vs ABAC"
        ],
        portfolio_score=8,
        github_appeal=[
            "Clear API documentation", "Postman collection included",
            "Docker support", "CI/CD pipeline"
        ],
        real_world_use="Authentication system used by most web applications",
        suggested_features=[
            "User registration and login",
            "JWT access and refresh tokens",
            "Role-based permissions (admin, user, guest)",
            "Password reset via email",
            "Account verification",
            "Rate limiting per user"
        ],
        stretch_goals=[
            "OAuth2 social login (Google, GitHub)",
            "Two-factor authentication",
            "API key management",
            "Audit logging"
        ],
        prerequisites=["Basic HTTP knowledge", "Basic SQL"],
        language="python",
        frameworks=["FastAPI", "SQLAlchemy"]
    ),

    ProjectSuggestion(
        id="task-queue-system",
        name="Distributed Task Queue",
        description="Build a task queue system like Celery from scratch. Learn about async processing, job scheduling, and distributed systems concepts that are crucial for scalable applications.",
        tagline="Redis-based task queue with scheduling and retries",
        primary_skills=["Distributed Systems", "Async Processing", "Message Queues"],
        secondary_skills=["Redis", "Concurrency", "Monitoring"],
        technologies=["Redis", "WebSockets", "Docker"],
        concepts_taught=[
            "Producer-consumer pattern", "Job scheduling",
            "Retry strategies", "Dead letter queues", "Worker pools"
        ],
        categories=[SkillCategory.BACKEND, SkillCategory.SYSTEMS, SkillCategory.ARCHITECTURE],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=40,
        career_goals=[CareerGoal.BACKEND_JOB, CareerGoal.STARTUP, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "How would you design a task queue?",
            "Handling job failures", "Scaling workers",
            "Exactly-once vs at-least-once delivery"
        ],
        portfolio_score=9,
        github_appeal=[
            "Architecture diagrams", "Performance benchmarks",
            "Comparison with Celery/RQ", "Dashboard UI"
        ],
        real_world_use="Background job processing for emails, reports, data pipelines",
        suggested_features=[
            "Task submission and tracking",
            "Priority queues",
            "Scheduled/delayed tasks",
            "Automatic retries with backoff",
            "Worker health monitoring",
            "Simple dashboard"
        ],
        stretch_goals=[
            "Task dependencies (DAG)",
            "Rate limiting per task type",
            "Multi-tenant support",
            "Prometheus metrics"
        ],
        prerequisites=["Redis basics", "Async programming"],
        language="python",
        frameworks=["FastAPI", "Redis"]
    ),

    ProjectSuggestion(
        id="graphql-api",
        name="GraphQL API Server",
        description="Build a GraphQL API with subscriptions, dataloaders, and proper schema design. Learn the modern API paradigm used by Facebook, GitHub, and Shopify.",
        tagline="GraphQL API with real-time subscriptions and efficient data loading",
        primary_skills=["GraphQL", "API Design", "Real-time Data"],
        secondary_skills=["Schema Design", "N+1 Prevention", "Caching"],
        technologies=["GraphQL", "WebSockets", "DataLoader"],
        concepts_taught=[
            "GraphQL schema design", "Resolvers", "Mutations",
            "Subscriptions", "N+1 problem", "Query complexity"
        ],
        categories=[SkillCategory.BACKEND, SkillCategory.API_DESIGN],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=30,
        career_goals=[CareerGoal.BACKEND_JOB, CareerGoal.FULLSTACK_JOB, CareerGoal.STARTUP],
        interview_topics=[
            "GraphQL vs REST trade-offs", "N+1 problem solutions",
            "Schema stitching", "Query depth limiting"
        ],
        portfolio_score=8,
        github_appeal=[
            "Interactive GraphQL playground", "Schema documentation",
            "Real-time demo", "Performance optimizations"
        ],
        real_world_use="Modern API architecture for complex data requirements",
        suggested_features=[
            "Type-safe schema with SDL",
            "CRUD operations via mutations",
            "Real-time subscriptions",
            "DataLoader for batching",
            "Query complexity analysis",
            "Authentication integration"
        ],
        stretch_goals=[
            "Federation/schema stitching",
            "Persisted queries",
            "Custom directives",
            "Automatic type generation"
        ],
        prerequisites=["Basic API concepts", "Database knowledge"],
        language="python",
        frameworks=["Strawberry GraphQL", "FastAPI"]
    ),

    # -------------------------------------------------------------------------
    # FRONTEND PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="react-dashboard",
        name="Analytics Dashboard",
        description="Build a responsive analytics dashboard with real-time updates, charts, and data tables. Master React patterns, state management, and data visualization.",
        tagline="Real-time analytics dashboard with interactive charts",
        primary_skills=["React", "State Management", "Data Visualization"],
        secondary_skills=["Responsive Design", "Performance Optimization", "TypeScript"],
        technologies=["React", "TypeScript", "Chart.js/D3", "TailwindCSS"],
        concepts_taught=[
            "Component architecture", "Custom hooks", "Context API",
            "Memoization", "Virtual scrolling", "WebSocket integration"
        ],
        categories=[SkillCategory.FRONTEND, SkillCategory.FULLSTACK],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=35,
        career_goals=[CareerGoal.FRONTEND_JOB, CareerGoal.FULLSTACK_JOB, CareerGoal.PORTFOLIO],
        interview_topics=[
            "React performance optimization", "State management approaches",
            "Component design patterns", "Handling large datasets"
        ],
        portfolio_score=9,
        github_appeal=[
            "Live demo link", "Beautiful UI screenshots",
            "Responsive design", "Dark mode support"
        ],
        real_world_use="Business intelligence and monitoring dashboards",
        suggested_features=[
            "Multiple chart types (line, bar, pie, area)",
            "Interactive data tables with sorting/filtering",
            "Real-time data updates",
            "Date range selection",
            "Export to PDF/CSV",
            "Responsive mobile view"
        ],
        stretch_goals=[
            "Drag-and-drop widget customization",
            "Saved dashboard configurations",
            "Embeddable widgets",
            "Email reports"
        ],
        prerequisites=["React basics", "JavaScript/TypeScript"],
        language="typescript",
        frameworks=["React", "TailwindCSS", "Recharts"]
    ),

    ProjectSuggestion(
        id="ecommerce-frontend",
        name="E-commerce Storefront",
        description="Build a complete e-commerce frontend with shopping cart, checkout flow, and payment integration. Learn essential patterns for production React applications.",
        tagline="Modern e-commerce storefront with cart and checkout",
        primary_skills=["React", "E-commerce Patterns", "Payment Integration"],
        secondary_skills=["State Management", "Forms", "SEO"],
        technologies=["React", "TypeScript", "Stripe", "Next.js"],
        concepts_taught=[
            "Shopping cart logic", "Optimistic updates", "Form validation",
            "Payment flows", "SEO optimization", "Server-side rendering"
        ],
        categories=[SkillCategory.FRONTEND, SkillCategory.FULLSTACK],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=40,
        career_goals=[CareerGoal.FRONTEND_JOB, CareerGoal.FULLSTACK_JOB, CareerGoal.FREELANCE],
        interview_topics=[
            "Cart state management", "Handling payment failures",
            "Inventory management", "Performance with many products"
        ],
        portfolio_score=9,
        github_appeal=[
            "Polished UI/UX", "Mobile responsive",
            "Stripe test mode demo", "Loading states"
        ],
        real_world_use="Online stores and marketplaces",
        suggested_features=[
            "Product listing with filters",
            "Product detail pages",
            "Shopping cart with persistence",
            "Checkout flow",
            "Order history",
            "Wishlist functionality"
        ],
        stretch_goals=[
            "Product reviews",
            "Inventory tracking",
            "Discount codes",
            "Multi-currency support"
        ],
        prerequisites=["React fundamentals", "Basic CSS"],
        language="typescript",
        frameworks=["Next.js", "TailwindCSS", "Stripe"]
    ),

    # -------------------------------------------------------------------------
    # FULLSTACK PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="realtime-chat",
        name="Real-time Chat Application",
        description="Build a Slack-like chat application with channels, direct messages, and real-time updates. Learn WebSockets, state synchronization, and scalable architecture.",
        tagline="Real-time chat with channels, DMs, and file sharing",
        primary_skills=["WebSockets", "Real-time Systems", "Full Stack Development"],
        secondary_skills=["Database Design", "File Upload", "Authentication"],
        technologies=["WebSockets", "React", "PostgreSQL", "Redis"],
        concepts_taught=[
            "WebSocket protocols", "Message queuing", "Presence detection",
            "Optimistic UI updates", "File storage", "Message search"
        ],
        categories=[SkillCategory.FULLSTACK, SkillCategory.BACKEND, SkillCategory.FRONTEND],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=50,
        career_goals=[CareerGoal.FULLSTACK_JOB, CareerGoal.STARTUP, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "WebSocket vs polling", "Scaling chat systems",
            "Message ordering", "Offline support"
        ],
        portfolio_score=10,
        github_appeal=[
            "Live demo", "Clean architecture",
            "Scalability documentation", "Mobile responsive"
        ],
        real_world_use="Team communication, customer support, social platforms",
        suggested_features=[
            "User authentication",
            "Public and private channels",
            "Direct messages",
            "Real-time message delivery",
            "Message history with search",
            "User presence (online/offline)",
            "File and image sharing"
        ],
        stretch_goals=[
            "Message reactions",
            "Threads",
            "Voice/video calls",
            "Message encryption"
        ],
        prerequisites=["React", "Node.js or Python", "SQL"],
        language="typescript",
        frameworks=["Next.js", "FastAPI", "Socket.io"]
    ),

    ProjectSuggestion(
        id="project-management",
        name="Project Management Tool",
        description="Build a Trello/Jira-like project management tool with boards, tasks, and team collaboration. Master complex state management and drag-and-drop interfaces.",
        tagline="Kanban board with drag-and-drop and team collaboration",
        primary_skills=["Complex State Management", "Drag and Drop", "Collaboration"],
        secondary_skills=["Real-time Updates", "Permissions", "Search"],
        technologies=["React", "DnD Kit", "PostgreSQL", "WebSockets"],
        concepts_taught=[
            "Drag and drop mechanics", "Optimistic updates",
            "Complex relational data", "Activity tracking", "Permissions"
        ],
        categories=[SkillCategory.FULLSTACK, SkillCategory.FRONTEND],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=45,
        career_goals=[CareerGoal.FULLSTACK_JOB, CareerGoal.STARTUP, CareerGoal.PORTFOLIO],
        interview_topics=[
            "Implementing drag and drop", "Handling concurrent edits",
            "Permission systems", "Activity feeds"
        ],
        portfolio_score=9,
        github_appeal=[
            "Smooth drag-and-drop demo", "Clean board UI",
            "Multiple view options", "Keyboard shortcuts"
        ],
        real_world_use="Team productivity and project tracking",
        suggested_features=[
            "Multiple boards per project",
            "Drag-and-drop cards between columns",
            "Card details (description, checklists, due dates)",
            "Team member assignment",
            "Activity log",
            "Board filtering and search"
        ],
        stretch_goals=[
            "Timeline/Gantt view",
            "Automations (rules)",
            "Time tracking",
            "Integrations (GitHub, Slack)"
        ],
        prerequisites=["React", "REST APIs", "Database design"],
        language="typescript",
        frameworks=["Next.js", "DnD Kit", "Prisma"]
    ),

    ProjectSuggestion(
        id="social-media-app",
        name="Social Media Platform",
        description="Build a Twitter/Instagram-like social platform with posts, followers, and a feed algorithm. Learn scalable architecture patterns used by real social networks.",
        tagline="Social platform with posts, followers, and smart feed",
        primary_skills=["Feed Algorithms", "Social Graph", "Scalable Architecture"],
        secondary_skills=["Media Upload", "Notifications", "Search"],
        technologies=["React", "PostgreSQL", "Redis", "S3"],
        concepts_taught=[
            "Fan-out on write vs read", "Social graph modeling",
            "Feed ranking", "Content moderation", "Media processing"
        ],
        categories=[SkillCategory.FULLSTACK, SkillCategory.BACKEND, SkillCategory.ARCHITECTURE],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=60,
        career_goals=[CareerGoal.FULLSTACK_JOB, CareerGoal.INTERVIEW_PREP, CareerGoal.STARTUP],
        interview_topics=[
            "Design a Twitter feed", "Handling viral content",
            "User recommendation", "Content moderation at scale"
        ],
        portfolio_score=10,
        github_appeal=[
            "Algorithm explanation", "Architecture diagrams",
            "Performance benchmarks", "Demo with sample data"
        ],
        real_world_use="Social networks, community platforms",
        suggested_features=[
            "User profiles and settings",
            "Posts with images/text",
            "Follow/unfollow system",
            "Personalized feed",
            "Likes and comments",
            "Notifications"
        ],
        stretch_goals=[
            "Stories feature",
            "Direct messages",
            "Hashtags and trending",
            "Content recommendations"
        ],
        prerequisites=["Full stack basics", "Database design"],
        language="typescript",
        frameworks=["Next.js", "FastAPI", "PostgreSQL"]
    ),

    # -------------------------------------------------------------------------
    # CLI TOOLS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="cli-dev-tool",
        name="Developer CLI Tool",
        description="Build a developer productivity CLI like gh, npm, or docker. Learn argument parsing, configuration management, and creating delightful command-line experiences.",
        tagline="Developer-friendly CLI with beautiful output and config management",
        primary_skills=["CLI Design", "Argument Parsing", "Configuration"],
        secondary_skills=["File System Operations", "Process Management", "Packaging"],
        technologies=["Click/Typer", "Rich", "TOML"],
        concepts_taught=[
            "CLI best practices", "Argument parsing patterns",
            "Config file management", "Interactive prompts", "Progress bars"
        ],
        categories=[SkillCategory.BACKEND, SkillCategory.SYSTEMS],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=20,
        career_goals=[CareerGoal.BACKEND_JOB, CareerGoal.DEVOPS_ENGINEER, CareerGoal.OPEN_SOURCE],
        interview_topics=[
            "CLI design patterns", "Configuration management",
            "Error handling in CLIs", "Publishing packages"
        ],
        portfolio_score=7,
        github_appeal=[
            "Beautiful terminal screenshots", "GIF demos",
            "Published to PyPI/npm", "Shell completions"
        ],
        real_world_use="Developer tooling and automation",
        suggested_features=[
            "Multiple subcommands",
            "Configuration file support",
            "Interactive mode",
            "Colored output and progress bars",
            "Shell completion scripts",
            "Verbose/quiet modes"
        ],
        stretch_goals=[
            "Plugin system",
            "Self-update mechanism",
            "Man pages",
            "Homebrew formula"
        ],
        prerequisites=["Python or Node.js basics"],
        language="python",
        frameworks=["Typer", "Rich"]
    ),

    ProjectSuggestion(
        id="git-tool",
        name="Git Workflow Tool",
        description="Build a git productivity tool that simplifies common workflows. Learn git internals and create something developers will actually use.",
        tagline="Git workflow automation with interactive branch management",
        primary_skills=["Git Internals", "Process Automation", "CLI UX"],
        secondary_skills=["Shell Integration", "Configuration", "Error Handling"],
        technologies=["Git", "Click", "GitHub API"],
        concepts_taught=[
            "Git plumbing commands", "Branch management",
            "Commit parsing", "Interactive selection", "API integration"
        ],
        categories=[SkillCategory.BACKEND, SkillCategory.DEVOPS],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=25,
        career_goals=[CareerGoal.BACKEND_JOB, CareerGoal.DEVOPS_ENGINEER, CareerGoal.OPEN_SOURCE],
        interview_topics=[
            "Git internals", "Branching strategies",
            "Merge vs rebase", "Git hooks"
        ],
        portfolio_score=8,
        github_appeal=[
            "Solves real problems", "Easy to install",
            "Great documentation", "Active community use"
        ],
        real_world_use="Developer daily workflow improvement",
        suggested_features=[
            "Interactive branch cleanup",
            "Smart checkout (fuzzy find)",
            "Quick PR creation",
            "Commit message templates",
            "Stash management",
            "Branch sync status"
        ],
        stretch_goals=[
            "GitHub/GitLab integration",
            "Commit signing helper",
            "Bisect helper",
            "Multi-repo support"
        ],
        prerequisites=["Git basics", "Python/Node.js"],
        language="python",
        frameworks=["Typer", "GitPython"]
    ),

    # -------------------------------------------------------------------------
    # DATA & ML PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="data-pipeline",
        name="Data Pipeline Framework",
        description="Build a data pipeline system like Airflow/Prefect. Learn DAG execution, task scheduling, and data engineering fundamentals.",
        tagline="DAG-based data pipeline with scheduling and monitoring",
        primary_skills=["Data Engineering", "DAG Processing", "Task Scheduling"],
        secondary_skills=["Monitoring", "Error Handling", "Storage"],
        technologies=["PostgreSQL", "Redis", "S3", "Docker"],
        concepts_taught=[
            "DAG execution", "Task dependencies", "Backfills",
            "Data lineage", "Retry strategies", "Observability"
        ],
        categories=[SkillCategory.DATA_SCIENCE, SkillCategory.BACKEND, SkillCategory.SYSTEMS],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=45,
        career_goals=[CareerGoal.DATA_ENGINEER, CareerGoal.BACKEND_JOB, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "DAG scheduling algorithms", "Handling failures",
            "Data quality checks", "Pipeline testing"
        ],
        portfolio_score=9,
        github_appeal=[
            "Architecture documentation", "Comparison with Airflow",
            "Example pipelines", "Performance benchmarks"
        ],
        real_world_use="ETL, data warehousing, analytics pipelines",
        suggested_features=[
            "Python DAG definition",
            "Task dependencies",
            "Scheduled runs",
            "Manual triggers",
            "Task retries",
            "Simple web UI for monitoring"
        ],
        stretch_goals=[
            "Distributed execution",
            "Data lineage tracking",
            "Slack notifications",
            "Custom operators"
        ],
        prerequisites=["Python", "SQL", "Basic async"],
        language="python",
        frameworks=["FastAPI", "Pydantic", "APScheduler"]
    ),

    ProjectSuggestion(
        id="ml-model-server",
        name="ML Model Serving Platform",
        description="Build a platform for deploying and serving ML models with versioning and A/B testing. Learn MLOps patterns used at scale.",
        tagline="ML model deployment platform with versioning and A/B testing",
        primary_skills=["MLOps", "Model Serving", "A/B Testing"],
        secondary_skills=["Docker", "Monitoring", "API Design"],
        technologies=["FastAPI", "Docker", "Redis", "Prometheus"],
        concepts_taught=[
            "Model packaging", "Version management", "Canary deployments",
            "Feature stores", "Model monitoring", "Latency optimization"
        ],
        categories=[SkillCategory.MACHINE_LEARNING, SkillCategory.BACKEND, SkillCategory.DEVOPS],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=40,
        career_goals=[CareerGoal.ML_ENGINEER, CareerGoal.DATA_ENGINEER, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "ML system design", "Model versioning",
            "Handling model drift", "A/B testing ML models"
        ],
        portfolio_score=9,
        github_appeal=[
            "MLOps best practices", "Docker-based",
            "Metrics dashboard", "Easy model deployment"
        ],
        real_world_use="Production ML systems at tech companies",
        suggested_features=[
            "Model upload and versioning",
            "REST API for predictions",
            "A/B testing configuration",
            "Request logging",
            "Basic metrics (latency, throughput)",
            "Health checks"
        ],
        stretch_goals=[
            "Batch prediction",
            "Model explainability",
            "Shadow deployments",
            "Auto-scaling"
        ],
        prerequisites=["Python", "Basic ML knowledge", "Docker"],
        language="python",
        frameworks=["FastAPI", "MLflow", "Docker"]
    ),

    # -------------------------------------------------------------------------
    # DEVOPS PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="deployment-platform",
        name="Simple PaaS Platform",
        description="Build a Heroku-like deployment platform. Learn container orchestration, git hooks, and platform engineering fundamentals.",
        tagline="Git-push deployment platform with auto-scaling",
        primary_skills=["Container Orchestration", "Platform Engineering", "Automation"],
        secondary_skills=["Git Hooks", "Networking", "Monitoring"],
        technologies=["Docker", "Nginx", "Git", "PostgreSQL"],
        concepts_taught=[
            "Container management", "Reverse proxy configuration",
            "Git deploy hooks", "Process supervision", "Log aggregation"
        ],
        categories=[SkillCategory.DEVOPS, SkillCategory.SYSTEMS, SkillCategory.CLOUD],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=50,
        career_goals=[CareerGoal.DEVOPS_ENGINEER, CareerGoal.BACKEND_JOB, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "Container vs VM", "Zero-downtime deployments",
            "Service discovery", "Log management"
        ],
        portfolio_score=10,
        github_appeal=[
            "Impressive scope", "Architecture deep-dive",
            "Comparison with Heroku", "One-command setup"
        ],
        real_world_use="Internal deployment platforms, dev environments",
        suggested_features=[
            "Git push deployment",
            "Automatic SSL certificates",
            "Environment variables",
            "Application logs",
            "Custom domains",
            "Basic scaling"
        ],
        stretch_goals=[
            "Database provisioning",
            "Marketplace add-ons",
            "Review apps",
            "Metrics dashboard"
        ],
        prerequisites=["Docker", "Linux basics", "Networking"],
        language="python",
        frameworks=["FastAPI", "Docker SDK"]
    ),

    ProjectSuggestion(
        id="monitoring-system",
        name="Application Monitoring System",
        description="Build a Datadog-like monitoring system with metrics collection, alerting, and dashboards. Learn observability fundamentals.",
        tagline="Metrics collection and alerting with custom dashboards",
        primary_skills=["Observability", "Metrics", "Alerting"],
        secondary_skills=["Time-series Data", "Visualization", "Anomaly Detection"],
        technologies=["TimescaleDB", "React", "Grafana concepts"],
        concepts_taught=[
            "Time-series databases", "Metric types (counter, gauge, histogram)",
            "Alert conditions", "Dashboard design", "Agent-based collection"
        ],
        categories=[SkillCategory.DEVOPS, SkillCategory.BACKEND, SkillCategory.DATA_SCIENCE],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=45,
        career_goals=[CareerGoal.DEVOPS_ENGINEER, CareerGoal.BACKEND_JOB, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "Metrics vs logs vs traces", "Alert fatigue prevention",
            "High-cardinality metrics", "Sampling strategies"
        ],
        portfolio_score=9,
        github_appeal=[
            "Beautiful dashboards", "Easy agent setup",
            "Alerting examples", "Docker compose demo"
        ],
        real_world_use="Infrastructure and application monitoring",
        suggested_features=[
            "Metrics ingestion API",
            "Agent for system metrics",
            "Custom metric submission",
            "Dashboard builder",
            "Alert rules engine",
            "Notification channels (email, Slack)"
        ],
        stretch_goals=[
            "Log aggregation",
            "Distributed tracing",
            "Anomaly detection",
            "SLO tracking"
        ],
        prerequisites=["Databases", "REST APIs", "React basics"],
        language="python",
        frameworks=["FastAPI", "TimescaleDB", "React"]
    ),

    # -------------------------------------------------------------------------
    # LIBRARY/PACKAGE PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="validation-library",
        name="Data Validation Library",
        description="Build a validation library like Pydantic or Zod. Learn type systems, schema validation, and library API design.",
        tagline="Type-safe data validation with great error messages",
        primary_skills=["Library Design", "Type Systems", "API Design"],
        secondary_skills=["Error Messages", "Performance", "Documentation"],
        technologies=["TypeScript/Python", "Type Hints"],
        concepts_taught=[
            "Schema definition", "Type coercion", "Error formatting",
            "Composable validators", "Generic types", "Tree-shakeable exports"
        ],
        categories=[SkillCategory.BACKEND, SkillCategory.ARCHITECTURE],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=30,
        career_goals=[CareerGoal.BACKEND_JOB, CareerGoal.OPEN_SOURCE, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "Schema validation approaches", "Type inference",
            "Error handling strategies", "API design principles"
        ],
        portfolio_score=8,
        github_appeal=[
            "Published to npm/PyPI", "100% test coverage",
            "Great documentation", "Benchmark comparisons"
        ],
        real_world_use="API input validation, form validation, config parsing",
        suggested_features=[
            "Primitive type validators",
            "Object schema definition",
            "Array and optional types",
            "Custom validators",
            "Detailed error messages",
            "Type inference"
        ],
        stretch_goals=[
            "JSON Schema generation",
            "OpenAPI integration",
            "Async validators",
            "Branded types"
        ],
        prerequisites=["Strong typing knowledge", "Testing"],
        language="typescript",
        frameworks=["TypeScript"]
    ),

    ProjectSuggestion(
        id="state-machine-lib",
        name="State Machine Library",
        description="Build a state machine library like XState. Learn formal state machines, event-driven programming, and developer tooling.",
        tagline="Type-safe state machines with visualization",
        primary_skills=["State Machines", "Event-Driven Design", "TypeScript"],
        secondary_skills=["Visualization", "Testing", "Documentation"],
        technologies=["TypeScript", "D3/Mermaid"],
        concepts_taught=[
            "Finite state machines", "Statecharts", "Event handling",
            "Guards and actions", "Hierarchical states", "Visualization"
        ],
        categories=[SkillCategory.FRONTEND, SkillCategory.ARCHITECTURE],
        difficulty=DifficultyLevel.ADVANCED,
        estimated_hours=35,
        career_goals=[CareerGoal.FRONTEND_JOB, CareerGoal.OPEN_SOURCE, CareerGoal.INTERVIEW_PREP],
        interview_topics=[
            "State machine benefits", "Complex UI state management",
            "Formal verification", "State explosion problem"
        ],
        portfolio_score=8,
        github_appeal=[
            "Interactive visualizer", "TypeScript types",
            "Comprehensive examples", "React integration"
        ],
        real_world_use="Complex UI flows, game logic, workflow engines",
        suggested_features=[
            "State definition DSL",
            "Transitions and events",
            "Guards (conditional transitions)",
            "Actions (side effects)",
            "Visualization output",
            "React hook integration"
        ],
        stretch_goals=[
            "Parallel states",
            "History states",
            "Delayed transitions",
            "Persistence"
        ],
        prerequisites=["TypeScript", "State management concepts"],
        language="typescript",
        frameworks=["TypeScript", "React"]
    ),

    # -------------------------------------------------------------------------
    # MOBILE PROJECTS
    # -------------------------------------------------------------------------
    ProjectSuggestion(
        id="mobile-fitness-app",
        name="Fitness Tracking App",
        description="Build a fitness app with workout tracking, progress charts, and offline support. Learn mobile development patterns and native integrations.",
        tagline="Workout tracker with offline support and progress analytics",
        primary_skills=["Mobile Development", "Offline-First", "Data Visualization"],
        secondary_skills=["Local Storage", "Push Notifications", "Health APIs"],
        technologies=["React Native", "SQLite", "Charts"],
        concepts_taught=[
            "Offline-first architecture", "Local database sync",
            "Native module integration", "Push notifications", "Health kit"
        ],
        categories=[SkillCategory.MOBILE, SkillCategory.FULLSTACK],
        difficulty=DifficultyLevel.INTERMEDIATE,
        estimated_hours=40,
        career_goals=[CareerGoal.MOBILE_DEVELOPER, CareerGoal.FREELANCE, CareerGoal.PORTFOLIO],
        interview_topics=[
            "Offline-first design", "Mobile performance",
            "State persistence", "Background sync"
        ],
        portfolio_score=8,
        github_appeal=[
            "App store screenshots", "Smooth animations",
            "Cross-platform", "Health integration"
        ],
        real_world_use="Personal fitness tracking, gym apps",
        suggested_features=[
            "Workout logging",
            "Exercise library",
            "Progress charts",
            "Workout history",
            "Offline mode",
            "Push notification reminders"
        ],
        stretch_goals=[
            "Apple Health / Google Fit sync",
            "Social sharing",
            "Custom workout builder",
            "AI workout suggestions"
        ],
        prerequisites=["React basics", "JavaScript"],
        language="typescript",
        frameworks=["React Native", "Expo"]
    ),
]


class ProjectSuggester:
    """Suggests projects based on user goals and skills."""

    def __init__(self, catalog: list[ProjectSuggestion] = None):
        self.catalog = catalog or PROJECT_CATALOG

    def suggest_by_skills(
        self,
        skills_to_learn: list[str],
        current_skills: list[str] = None,
        difficulty: DifficultyLevel = None,
        max_hours: float = None,
        limit: int = 4
    ) -> list[dict]:
        """
        Suggest projects based on skills the user wants to learn.

        Args:
            skills_to_learn: Skills/technologies the user wants to learn
            current_skills: Skills the user already has
            difficulty: Preferred difficulty level
            max_hours: Maximum hours available
            limit: Maximum number of suggestions

        Returns:
            List of scored project suggestions
        """
        current_skills = current_skills or []
        skills_lower = [s.lower() for s in skills_to_learn]
        current_lower = [s.lower() for s in current_skills]

        scored_projects = []

        for project in self.catalog:
            score = 0
            matches = []

            # Check skill matches
            all_project_skills = (
                project.primary_skills +
                project.secondary_skills +
                project.technologies +
                project.concepts_taught
            )
            all_project_skills_lower = [s.lower() for s in all_project_skills]

            for skill in skills_lower:
                for ps in all_project_skills_lower:
                    if skill in ps or ps in skill:
                        # Primary skills worth more
                        if any(skill in s.lower() for s in project.primary_skills):
                            score += 3
                        else:
                            score += 1
                        matches.append(skill)
                        break

            # Check if prerequisites are met
            prereqs_met = True
            for prereq in project.prerequisites:
                prereq_lower = prereq.lower()
                if not any(prereq_lower in cs or cs in prereq_lower for cs in current_lower):
                    prereqs_met = False
                    break

            if prereqs_met:
                score += 2

            # Apply filters
            if difficulty and project.difficulty != difficulty:
                continue
            if max_hours and project.estimated_hours > max_hours:
                continue

            # Portfolio score bonus
            score += project.portfolio_score / 2

            if score > 0:
                scored_projects.append({
                    "project": project.to_dict(),
                    "score": score,
                    "matched_skills": list(set(matches)),
                    "prerequisites_met": prereqs_met
                })

        # Sort by score
        scored_projects.sort(key=lambda x: x["score"], reverse=True)

        return scored_projects[:limit]

    def suggest_by_career_goal(
        self,
        career_goal: CareerGoal,
        current_skills: list[str] = None,
        difficulty: DifficultyLevel = None,
        limit: int = 4
    ) -> list[dict]:
        """
        Suggest projects based on career goals.

        Args:
            career_goal: The career goal to prepare for
            current_skills: Skills the user already has
            difficulty: Preferred difficulty level
            limit: Maximum number of suggestions

        Returns:
            List of scored project suggestions
        """
        current_skills = current_skills or []
        current_lower = [s.lower() for s in current_skills]

        scored_projects = []

        for project in self.catalog:
            if career_goal not in project.career_goals:
                continue

            score = 0

            # Base score from portfolio appeal
            score += project.portfolio_score

            # Bonus for interview relevance
            if project.interview_topics:
                score += len(project.interview_topics)

            # Check prerequisites
            prereqs_met = True
            for prereq in project.prerequisites:
                prereq_lower = prereq.lower()
                if not any(prereq_lower in cs or cs in prereq_lower for cs in current_lower):
                    prereqs_met = False
                    break

            if prereqs_met:
                score += 3

            # Apply filters
            if difficulty and project.difficulty != difficulty:
                continue

            scored_projects.append({
                "project": project.to_dict(),
                "score": score,
                "interview_topics": project.interview_topics,
                "prerequisites_met": prereqs_met
            })

        # Sort by score
        scored_projects.sort(key=lambda x: x["score"], reverse=True)

        return scored_projects[:limit]

    def suggest_for_portfolio(
        self,
        categories: list[SkillCategory] = None,
        current_skills: list[str] = None,
        limit: int = 4
    ) -> list[dict]:
        """
        Suggest projects that look great on a portfolio/GitHub.

        Args:
            categories: Optional filter by skill categories
            current_skills: Skills the user already has
            limit: Maximum number of suggestions

        Returns:
            List of portfolio-optimized project suggestions
        """
        current_skills = current_skills or []
        current_lower = [s.lower() for s in current_skills]

        scored_projects = []

        for project in self.catalog:
            # Filter by category if specified
            if categories:
                if not any(cat in project.categories for cat in categories):
                    continue

            score = project.portfolio_score * 2  # Portfolio score is primary

            # Bonus for GitHub appeal items
            score += len(project.github_appeal)

            # Check prerequisites
            prereqs_met = True
            for prereq in project.prerequisites:
                prereq_lower = prereq.lower()
                if not any(prereq_lower in cs or cs in prereq_lower for cs in current_lower):
                    prereqs_met = False
                    break

            if prereqs_met:
                score += 2

            scored_projects.append({
                "project": project.to_dict(),
                "score": score,
                "github_appeal": project.github_appeal,
                "portfolio_score": project.portfolio_score,
                "prerequisites_met": prereqs_met
            })

        # Sort by score
        scored_projects.sort(key=lambda x: x["score"], reverse=True)

        return scored_projects[:limit]

    def get_project_by_id(self, project_id: str) -> Optional[ProjectSuggestion]:
        """Get a specific project by ID."""
        for project in self.catalog:
            if project.id == project_id:
                return project
        return None

    def list_all_skills(self) -> dict[str, list[str]]:
        """List all skills that can be learned across all projects."""
        skills = {
            "primary": set(),
            "secondary": set(),
            "technologies": set(),
            "concepts": set()
        }

        for project in self.catalog:
            skills["primary"].update(project.primary_skills)
            skills["secondary"].update(project.secondary_skills)
            skills["technologies"].update(project.technologies)
            skills["concepts"].update(project.concepts_taught)

        return {k: sorted(list(v)) for k, v in skills.items()}

    def list_career_goals(self) -> list[dict]:
        """List all supported career goals with descriptions."""
        goal_descriptions = {
            CareerGoal.FRONTEND_JOB: "Frontend Developer position",
            CareerGoal.BACKEND_JOB: "Backend Developer position",
            CareerGoal.FULLSTACK_JOB: "Full Stack Developer position",
            CareerGoal.DATA_ENGINEER: "Data Engineer position",
            CareerGoal.ML_ENGINEER: "Machine Learning Engineer position",
            CareerGoal.DEVOPS_ENGINEER: "DevOps/Platform Engineer position",
            CareerGoal.MOBILE_DEVELOPER: "Mobile Developer position",
            CareerGoal.FREELANCE: "Freelance/Consulting work",
            CareerGoal.STARTUP: "Startup or founding a company",
            CareerGoal.PORTFOLIO: "Building an impressive portfolio",
            CareerGoal.OPEN_SOURCE: "Contributing to open source",
            CareerGoal.INTERVIEW_PREP: "Technical interview preparation",
        }

        return [
            {"id": goal.value, "name": goal.name, "description": desc}
            for goal, desc in goal_descriptions.items()
        ]


# Singleton instance
_suggester = None

def get_suggester() -> ProjectSuggester:
    """Get the singleton ProjectSuggester instance."""
    global _suggester
    if _suggester is None:
        _suggester = ProjectSuggester()
    return _suggester
