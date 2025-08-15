from langchain_chroma import Chroma
from embedding_model import embeddings

vector_store = Chroma(
    collection_name="Medical-Research-Papers",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)