from langchain_huggingface import HuggingFaceEmbeddings

model_name = "Qwen/Qwen3-Embedding-0.6B"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)