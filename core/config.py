import secrets
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv("../.env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vivace"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Enhances user queries with relevant information retrieved from a knowledge base using Retrieval-Augmented Generation (RAG)."
    API_PREFIX: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    TESTING: bool = False

settings = Settings()

telex_integration_config = {
    "data": {
        "author": "Sage21",
        "date": {
            "created_at": "2025-02-20",
            "updated_at": "2025-02-20"
        },
        "descriptions": {
            "app_description": settings.PROJECT_DESCRIPTION,
            "app_logo": f"{os.getenv('BASE_URL')}/logo.png",
            "app_name": settings.PROJECT_NAME,
            "app_url": f"{os.getenv('BASE_URL')}",
            "background_color": "#4BEBA4"
        },
        "integration_category": "AI & Machine Learning",
        "integration_type": "modifier",
        "is_active": True,
        "key_features": [
            "Faster Access to Information",
            "Improved Collaboration",
            "Reduced Knowledge Silos",
            "Increased Efficiency",
            "Enhanced Onboarding",
            "Better Incident Response",
            "Streamlined Troubleshooting",
            "Augments user queries with relevant context from a knowledge base.",
            "Uses Retrieval-Augmented Generation (RAG) for enhanced responses.",
            "Improves collaboration and information access for DevOps and Software teams."
        ],
        "settings": [],  # Removed dynamic settings from here
        "website": f"{os.getenv('BASE_URL')}",
        "target_url": f"{os.getenv('BASE_URL')}{settings.API_PREFIX}/vivace",
        "tick_url": f"{os.getenv('BASE_URL')}{settings.API_PREFIX}/vivace"
    }
}
