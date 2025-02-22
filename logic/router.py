import os
import logging
from logic.services.rag_response import generate_response

# from logic.services.vector_database import (
#     retrieve_vector_database,
#     similar_from_db_tool
# )

from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, APIRouter

# from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
from typing import Optional
from core.config import settings, telex_integration_config
from core.settings import extract_settings
import markdownify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
api_router = APIRouter()

# Load environment variables from .env file
load_dotenv("../.env")


# Main execution
# pdf_path = os.path.abspath("logic/data/retrieval-augmented_generation.pdf")
# model_name = 'all-MiniLM-L6-v2'
# index_path = os.path.abspath("logic/data/faiss_index")

# embedding_model = SentenceTransformer(model_name).encode

# async def get_vector_db():
#     vector_store = await retrieve_vector_database(index_path, embedding_model)
#     return vector_store

# class RequestData(BaseModel):
#     channel_id: str = Field(..., example="0192dd70-cdf1-7e15-8776-4fee4a78405e", description="Unique identifier for the channel")
#     settings: list = Field(..., example=[{"label": "Knowledge Base URL(separate multiple sources with commas)", "type": "text", "required": True, "default": "https://aws.amazon.com/what-is/retrieval-augmented_generation/"}])
#     message: str = Field(..., example="This is a test message that will be formatted.")


@api_router.post("/vivace")
async def modify_message(request: Request):
    """
    Modifies the message based on the content of the input message.

    Receives a JSON payload and returns a JSON response.
    """
    try:
        data = await request.json()
        logger.info(f"Received request data: {data}")

        message = data.get("message")
        if not message:
            raise HTTPException(
                status_code=400, detail="Missing 'message' in request body"
            )

        settings_list = data.get("settings", [])
        extracted_settings = extract_settings(settings_list)
        logger.info(f"Extracted settings: {extracted_settings}")
        knowledge_base_url = extracted_settings.get(
            "Knowledge Base URL(separate multiple sources with commas)", ""
        )

        # Retrieve vector store and perform similarity search
        # Todo: Add the similarity search later
        # channel_id to be use for data storage and tracking
        # vector_store = await get_vector_db()
        # similar_docs = similar_from_db_tool(query, vector_store)
        #  # Convert HTML message to Markdown
        markdown_message = markdownify.markdownify(message)
        logger.info(f"Converted message to Markdown: {markdown_message}")

        query = markdown_message
        logger.info(
            f"Calling generate_response with query: {query} and knowledge_base_url: {knowledge_base_url}"
        )
        # vector_store = await get_vector_db()
        # similar_docs = similar_from_db_tool(query, vector_store)

        # vector_store = await get_vector_db()
        # similar_docs = similar_from_db_tool(query, vector_store)

        response = generate_response(query, knowledge_base_url)
        return JSONResponse(
            {
                "event_name": "message_formatted",
                "message": response,
                "status": "success",
                "username": settings.PROJECT_NAME,
            }
        )
    except HTTPException as e:
        logger.exception(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return JSONResponse({"error": str(e)}, status_code=500)
