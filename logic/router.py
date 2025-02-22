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

api_router = APIRouter()


# Load environment variables from .env file
load_dotenv('../.env')


# Main execution
# pdf_path = os.path.abspath("logic/data/retrieval-augmented_generation.pdf")
# model_name = 'all-MiniLM-L6-v2'
# index_path = os.path.abspath("logic/data/faiss_index")

# embedding_model = SentenceTransformer(model_name).encode

# async def get_vector_db():
#     vector_store = await retrieve_vector_database(index_path, embedding_model)
#     return vector_store

class RequestData(BaseModel):
    settings: list = Field(..., example=[{"label": "Knowledge Base URL(separate multiple sources with commas)", "type": "text", "required": True, "default": "https://aws.amazon.com/what-is/retrieval-augmented-generation/"}])
    message: str = Field(..., example="This is a test message that will be formatted.")

@api_router.post("/vivace")
async def modify_message(request: RequestData):
    """
    Modifies the message based on the content of the input message.

    Receives a JSON payload with a single key, "message", and returns a JSON
    response with a single key, "message", containing the modified message.
    """
    try:
        # data = await request.json()
        # message = data.get("message")
        message = request.message
        if not message:
            raise HTTPException(
                status_code=400, detail="Missing 'message' in request body")

        query = message
        # Retrieve vector store and perform similarity search
        # Todo: Add the similarity search later
        # vector_store = await get_vector_db()
        # similar_docs = similar_from_db_tool(query, vector_store)
        # response = generate_response(query, request.settings[0]["default"], similar_docs, 2000)
        response = generate_response(query, request.settings[0]["default"])
        return JSONResponse({"message": response,
                             "settings": request.settings[0]["default"]})
    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
