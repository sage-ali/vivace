import os

from logic.services.rag_response import generate_response
# from logic.services.vector_database import (
#     retrieve_vector_database,
#     similar_from_db_tool
# )

from dotenv import load_dotenv
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, APIRouter
# from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
from typing import Optional
import re
import logging
from core.config import settings, telex_integration_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


# Load environment variables from .env file
load_dotenv('../.env')


class RequestData(BaseModel):
    channel_id: str = Field(..., example="0192dd70-cdf1-7e15-8776-4fee4a78405e", description="Unique identifier for the channel")
    settings: list = Field(..., example=[
        {"label": "Knowledge Base URL(separate multiple sources with commas)", "type": "text", "required": True, "default": "https://aws.amazon.com/what-is/retrieval-augmented_generation/"}
    ])
    message: str = Field(..., example="This is a test message that will be formatted.")

def extract_settings(settings_list: list) -> dict:
    extracted_settings = {}
    for setting in settings_list:
        extracted_settings[setting["label"]] = setting["default"]
    return extracted_settings

@api_router.post("/vivace")
async def modify_message(request: RequestData):
    """
    Modifies the message based on the content of the input message.

    Receives a JSON payload with a single key, "message", and returns a JSON
    response with a single key, "message", containing the modified message.
    """
    try:
        logger.info(f"Received request: {request}")

        message = request.message
        if not message:
            raise HTTPException(
                status_code=400, detail="Missing 'message' in request body")

        extracted_settings = extract_settings(request.settings)
        logger.info(f"Extracted settings: {extracted_settings}")
        knowledge_base_url = extracted_settings.get("Knowledge Base URL(separate multiple sources with commas)", "")

        query = message
        # Retrieve vector store and perform similarity search
        # Todo: Add the similarity search later
        # channel_id to be use for data storage and tracking
        # vector_store = await get_vector_db()
        # similar_docs = similar_from_db_tool(query, vector_store)
        # response = generate_response(query, request.settings[0]["default"], similar_docs, 2000)
        logger.info(f"Calling generate_response with query: {query} and knowledge_base_url: {knowledge_base_url}")
        response = generate_response(query, knowledge_base_url)
        return JSONResponse({
            "event_name": "message_formatted",
            "message": response,
            "status": "success",
            "username": settings.PROJECT_NAME
        })
    except HTTPException as e:
        logger.exception(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return JSONResponse({"error": str(e)}, status_code=500)
