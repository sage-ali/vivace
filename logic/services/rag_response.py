import time
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Optional, Union
import logging
from logic.utilities.html_parser import get_website_content

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def generate_response(query, knowledge_base_url, similar_docs, context_window_size):
def generate_response(query, knowledge_base_url):
    logger.info(
        f"Generating response for query: {query} using knowledge base: {knowledge_base_url}"
    )
    website_content = get_website_content(knowledge_base_url)
    if website_content is None:
        system_message = (
            f"Could not retrieve content from the following knowledge base URL: {knowledge_base_url}. "
            f"Please answer the query to the best of your ability without external information."
            f"Do not generate more than 100 words."
        )
    else:
        truncated_content = website_content[:1000]  # Limit content to 100 characters
        system_message = (
            f"Use the following Content below to answer the user's query. "
            f"Answer directly, paraphrasing from the knowledge base content if available."
            f"If the knowledge base content is not sufficient, provide a general response.\n\n"
            f"Content:\n\n {truncated_content}"
        )
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query},
        # Add the similarity search later
        # {"role": "assistant", "content": "\n\n".join(similar_docs)}
    ]

    chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    chat_model.max_output_tokens = 200
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to generate response (attempt {attempt + 1})")
            response = chat_model.invoke(messages)
            if response:
                logger.info(
                    f"Successfully generated response in {attempt + 1} attempts"
                )
                return f"Query: {query}\n\nResponse: {response.content}"
        except Exception as e:
            logger.error(f"Error calling Gemini API (attempt {attempt + 1}): {e}")
    logger.warning("Failed to generate response after multiple retries")
    return ""


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rag_response.py <query> <knowledge_base_url>")
        sys.exit(1)

    query = sys.argv[1]
    knowledge_base_url = sys.argv[2]

    start_time = time.time()
    response = generate_response(query, knowledge_base_url)
    end_time = time.time()

    print(f"Response: {response}")
    print(f"Time taken: {end_time - start_time} seconds")
