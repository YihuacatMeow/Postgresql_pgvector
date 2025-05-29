import os
import re
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ================= 基本設定 ====================
EMBEDDING_MODEL_ID = "paraphrase-multilingual-mpnet-base-v2"
DOCS_PATH = "./docs"
COLLECTION_NAME = "embed_pgvector1"

# ✅ PostgreSQL 連線設定
CONNECTION_STRING = "postgresql+psycopg2://postgres:123456@localhost:5433/vector"

embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_ID)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=80,
    keep_separator=False,
    add_start_index=True,
    separators=["\n\n"],
    is_separator_regex=False
)

# ================= 文本切分 ====================
documents = []

for filename in os.listdir(DOCS_PATH):
    if filename.endswith(".txt"):
        file_path = os.path.join(DOCS_PATH, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            chunks = text_splitter.split_text(content)
            for idx, chunk in enumerate(chunks, start=1):
                doc = Document(
                    page_content=chunk,
                    metadata={"source": f"{filename}_chunk{idx}"}
                )
                documents.append(doc)

# ================= 儲存到 PostgreSQL/pgvector ====================
vectorstore = PGVector.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

retriever = vectorstore.as_retriever()
