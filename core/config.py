import secrets
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv("../env")


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
        "date": {
            "created_at": "2025-02-20",
            "updated_at": "2025-02-21"
        },
        "descriptions": {
            "app_description": settings.PROJECT_DESCRIPTION,
            "app_logo": "URL to the application logo.",
            "app_name": settings.PROJECT_NAME,
            "app_url": "URL to the application or service.",
            "background_color": "#FFFFFF"
        },
        "integration_category": "AI & Machine Learning",
        "integration_type": "modifier",
        "is_active": True,
        "output": [
            {
                "label": "output_channel_1",
                "value": True
            }
        ],
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
        "permissions": {
            "monitoring_user": {
                "always_online": True,
                "display_name": "Vivace"
            }
        },
        "settings": [
            {
                # Separate multiple sources with
                "label": "Knowledge Base URL",
                "type": "text",
                "required": True,
                "default": "https://company-wiki.example.com"
            },
            {
                "label": "Embedding Model",
                "type": "dropdown",
                "required": True,
                "default": "BERT",
                "options": [
                    "BERT",
                    "RoBERTa",
                    "Sentence Transformers"
                ]
            },
            {
                "label": "Vector Database",
                "type": "dropdown",
                "required": True,
                "default": "FAISS",
                "options": [
                    "FAISS",
                    "Annoy"
                ]
            },
            {
                "label": "Context Window Size",
                "type": "number",
                "required": True,
                "default": 500
            },
            {
                "label": "Enable Debug Logging",
                "type": "checkbox",
                "required": True,
                "default": True
            }
        ],
        "target_url": f"{os.getenv("BASE_URL")}/webhook"
    }
}
