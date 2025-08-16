# Medisyn (Medical + Synthesis)
Built a RAG Based application for answering the unanswered questions regarding some diseases or rare diseases on which medical research is going on.

## Models:
1. Chat Model - TinyLlama-1.1B-Chat-v1.0 -> https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
2. Embedding Model - sentence-transformer/all-mpnet/base/v2 -> https://huggingface.co/sentence-transformers/all-mpnet-base-v2

## Medical Research Documents
Scraped the medical research papers from PubMed (a free resource for biomedical and life sciences journal articles) via Biopython library and E-utilities documentation(https://lnkd.in/g4g3uGgN) which consists of E-Search and E-Fetch methods for retrieval.

## Steps to use it:
1. Clone the repository:
```git
git clone https://github.com/RishitSaxena55/Medisyn
```
2. Create a LangSmith account and generate a key: https://www.langchain.com/langsmith
  
3. Run app.py:
```app
uvicorn main:app --reload
```
> **Note:** The answers can be delayed as I have used free Open-sourced Models from hugging face. Will upgrade it to better models to make the experience faster.


