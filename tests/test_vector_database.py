# import os
# import pytest
# import asyncio  # Import asyncio


# from logic.services.vector_database import (
#     load_vector_database,
#     retrieve_vector_database,
#     add_documents_to_vector_database,
#     similar_from_db_tool
# )
# from sentence_transformers import SentenceTransformer
# from langchain_community.vectorstores import FAISS
# from langchain.docstore.document import Document


# PROJECT_ROOT = os.path.dirname(os.path.dirname(
#     os.path.abspath(__file__)))  # Project root directory
# DATA_DIR = os.path.join(PROJECT_ROOT, "logic", "data")
# # Corrected path for FAISS index
# FAISS_INDEX_DIR = os.path.join(DATA_DIR, "faiss_index_test")


# @pytest.fixture(scope="session")
# def setup_environment():
#     # Absolute path to PDF
#     pdf_path = os.path.join(DATA_DIR, 'retrieval-augmented_generation.pdf')
#     os.environ['PDF_PATH'] = pdf_path
#     os.environ['EMBEDDING_MODEL'] = 'all-MiniLM-L6-v2'
#     os.environ['INDEX_PATH'] = FAISS_INDEX_DIR
#     # Ensure the test PDF file exists
#     if not os.path.exists(os.environ['PDF_PATH']):
#         with open(os.environ['PDF_PATH'], 'w') as f:
#             f.write("This is a test PDF content.")
#     yield


# @pytest.fixture(scope="session")
# def vector_store(setup_environment):
#     embedding_model = SentenceTransformer(os.environ['EMBEDDING_MODEL']).encode
#     index_path = os.environ['INDEX_PATH']
#     return asyncio.run(retrieve_vector_database(index_path, embedding_model))  # Use asyncio.run and return the result


# @pytest.mark.asyncio
# async def test_load_vector_database(setup_environment):
#     pdf_path = os.environ['PDF_PATH']
#     embedding_model = os.environ['EMBEDDING_MODEL']
#     index_path = os.environ['INDEX_PATH']

#     embedding_function = await load_vector_database(pdf_path, embedding_model, index_path)
#     assert embedding_function is not None
#     assert os.path.exists(index_path + "/index.faiss")


# @pytest.mark.asyncio
# # vector_store is already awaited!
# async def test_retrieve_vector_database(vector_store):
#     assert isinstance(vector_store, FAISS)


# @pytest.mark.asyncio
# async def test_add_documents_to_vector_database(setup_environment):
#     embedding_model = SentenceTransformer(os.environ['EMBEDDING_MODEL']).encode
#     index_path = os.environ['INDEX_PATH']

#     documents = [
#         Document(page_content="This is the first document."),
#         Document(page_content="This is the second document."),
#     ]
#     await add_documents_to_vector_database(documents, embedding_model, index_path)
#     assert os.path.exists(index_path)


# def test_similar_from_db_tool(vector_store):  # vector_store is already awaited!
#     query = "the first document."
#     similar_docs = similar_from_db_tool(query, vector_store)  # Await here!
#     assert isinstance(similar_docs, list)


