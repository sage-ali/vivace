from uuid import uuid4
import asyncio
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv
import faiss

from sentence_transformers import SentenceTransformer

# from langchain_community.embeddings import GooglePalmEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import CharacterTextSplitter

# Load environment variables from .env file
load_dotenv('../../.env')


def run_in_executor(func):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, func, *args, **kwargs)
        return result
    return wrapper


@run_in_executor
def load_vector_database(pdf_path: str, embedding_model: str, index_path: str) -> any:
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n")
    split_documents = text_splitter.split_documents(documents)

    texts = [doc.page_content for doc in split_documents]

    # this changes for other kinds of models
    model = SentenceTransformer(embedding_model)
    embedding_model = model.encode

    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype('float32')

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    uuids = [str(uuid4()) for _ in range(len(split_documents))]

    vector_store = FAISS(
        embedding_function=embedding_model,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    # Add the documents
    vector_store.add_documents(documents=split_documents, ids=uuids)

    vector_store.save_local(index_path)
    return embedding_model


@run_in_executor
def retrieve_vector_database(index_path: str, embedding_model: any) -> FAISS:
    new_vectorstore = FAISS.load_local(
        index_path, embedding_model, allow_dangerous_deserialization=True)
    print("FAISS index read successfully!")
    return new_vectorstore


@run_in_executor
def add_documents_to_vector_database(documents: list, embedding_model: any, index_path: str) -> None:
    vector_store = FAISS.load_local(
        index_path, embedding_model, allow_dangerous_deserialization=True)
    print("FAISS index read successfully!")

    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n")
    split_documents = text_splitter.split_documents(documents)

    texts = [doc.page_content for doc in split_documents]

    embeddings = embedding_model(texts)
    embeddings = np.array(embeddings).astype('float32')

    uuids = [str(uuid4()) for _ in range(len(split_documents))]

    vector_store.add_documents(documents=split_documents, ids=uuids)
    vector_store.save_local(index_path)



# Add async here
def similar_from_db_tool(query: str, vectorstore: FAISS, k=3) -> list:
    # Use similarity_search
    print("retrieving similar documents")
    retrieved_docs = vectorstore.similarity_search(query=query, k=k)
    similar_docs_data = []
    for doc in retrieved_docs:
        if hasattr(doc, 'page_content'):
            similar_docs_data.append(doc.page_content)
        elif hasattr(doc, 'text'):
            similar_docs_data.append(doc.text)
        else:
            similar_docs_data.append(str(doc))

    return similar_docs_data
