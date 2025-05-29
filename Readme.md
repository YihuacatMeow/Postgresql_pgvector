# python

## 一、建立虛擬環境
`python -m venv .venv`
`.venv\Scripts\activate`

## 二、安裝相關依賴
`pip install langchain langchain-community langchain-text-splitters`
`pip install sentence-transformers`
`pip install pgvector psycopg2-binary`

# postgresql+pgvector

## 一、安裝
電腦安裝postgresql、pgadmin、docker、SQL shell
postgresql連線設定

## 二、開啟資料庫連線  
SQL shell輸入登入內容(先前安裝時設定的)，記得不要關閉視窗
開啟專案，創建docker-compose.yml檔案，設定port
範例:
    ``ports:
      - '5433:5432'(改前面的port)``


## 三、透過docker安裝pgvector
在終端機輸入:
`docker pull pgvector/pgvector:pg17`
`git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git`
完成後到docker確認連線成功(綠燈)
`cd pgvector`
`docker build --pull --build-arg PG_MAJOR=17 -t myuser/pgvector .`
`docker run -d   --name pgvector-db   --shm-size=1g   -e POSTGRES_USER=postgres`



## 四、確認pgvector成功安裝
`docker exec -it pgvector-db psql -U postgres -d vector`
(sql指令)
`CREATE EXTENSION IF NOT EXISTS vector;(安裝)`
`CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));`
`INSERT INTO items (embedding) VALUES ('[1, 0, 0.1]'), ('[1, 0, -0.1]');`
`SELECT * FROM items ORDER BY embedding <-> '[1, 1, 0.1]' LIMIT 2;`


## 五、執行檔案
`python .\Embedding_pgvector.py`
