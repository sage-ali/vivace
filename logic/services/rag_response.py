from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Optional, Union

class RagResponse(BaseModel):
    """Response from a Retrieval-Augmented Generation (RAG) system."""

    query: str = Field(description="The original query from the user.")
    retrieved_context: str = Field(description="The context retrieved from the knowledge base.")
    generated_response: str = Field(description="The generated response based on the query and retrieved context.")
    source_url: Optional[str] = Field(description="The URL of the source document, if applicable.")
    confidence_score: Optional[float] = Field(description="The confidence score of the generated response (0.0 to 1.0).")
    metadata: Optional[Union[dict,str]] = Field(description="Additional metadata related to the response.")

def generate_response(query, similar_docs, knowledge_base_url, context_window_size):
    system_message = (
        f"Use the following knowledge base URL: {knowledge_base_url} "
        f"to augment in answering user query or providing additional "
        f"context to user input. Limit the context window size to "
        f"{context_window_size} characters."
        f"Do not generate more than 900 characters"
        f"Answer directly, paraphrasing from the knowledge base and assistant content."
    )
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query},
        {"role": "assistant", "content": "\n\n".join(similar_docs)}
    ]

    chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001")
    chat_model.max_output_tokens = 250
    chat_model_with_structure = chat_model.with_structured_output(RagResponse)
    try:
        response:RagResponse = chat_model_with_structure.invoke(messages)
        #Handle the metadata string.
        if isinstance(response.metadata, str):
            response.metadata = {}
        return response.generated_response
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return ""

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Usage: python rag_response.py <query> <similar_docs> <knowledge_base_url> <context_window_size>")
        sys.exit(1)

    query = sys.argv[1]
    similar_docs_str = sys.argv[2]
    if similar_docs_str:
        similar_docs = similar_docs_str.split(';')
    else:
        similar_docs = []

    knowledge_base_url = sys.argv[3]
    context_window_size = int(sys.argv[4])

    response = generate_response(query, similar_docs, knowledge_base_url, context_window_size)
    print(response)