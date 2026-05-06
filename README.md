# AI RAG Project — Step-by-Step Run Guide

```
User → Angular UI (4200) → Spring Boot (8080) → FastAPI (8000) → LangChain Agent
                                                                        ├── Tool: Calculator
                                                                        └── Tool: Document Search → Pinecone + OpenAI
```

---

## Step 1 — Get your API Keys

| Key | Where to get |
|-----|-------------|
| `OPENAI_API_KEY` | platform.openai.com → API Keys |
| `PINECONE_API_KEY` | app.pinecone.io → API Keys |
| `PINECONE_INDEX_NAME` | any name, e.g. `company-docs` |

---

## Step 2 — FastAPI Agent (Python)

```bash
cd fastapi-agent

# create & activate virtual env
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# install deps
pip install -r requirements.txt

# copy env file and fill in your keys
copy .env.example .env         # then edit .env

# (optional) upload your documents to Pinecone first
mkdir docs
# put your .txt files inside ./docs/
python upload_docs.py

# start the agent server
python main.py
# ✅ runs on http://localhost:8000
```

Test it:
```bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\": \"what is 25 * 4?\"}"
```

---

## Step 3 — Spring Boot API (Java 21)

```bash
cd spring-boot-api
./mvnw spring-boot:run        # Mac/Linux
mvnw.cmd spring-boot:run      # Windows
# ✅ runs on http://localhost:8080
```

Test it:
```bash
curl -X POST http://localhost:8080/api/ask -H "Content-Type: application/json" -d "{\"question\": \"what is 25 * 4?\"}"
```

---

## Step 4 — Angular UI

```bash
cd angular-ui
npm install
ng serve
# ✅ runs on http://localhost:4200
```

Open your browser at **http://localhost:4200** and start chatting!

---

## Project File Map

```
ai-rag-project/
├── fastapi-agent/
│   ├── main.py               ← FastAPI app + lifespan (agent warm-up)
│   ├── agent.py              ← Singleton LangChain AgentExecutor
│   ├── upload_docs.py        ← One-time Pinecone document uploader
│   ├── tools/
│   │   ├── calculator_tool.py
│   │   └── document_search_tool.py
│   ├── requirements.txt
│   └── .env.example
│
├── spring-boot-api/
│   ├── pom.xml
│   └── src/main/java/com/example/api/
│       ├── AiGatewayApplication.java
│       ├── controller/QuestionController.java  ← POST /api/ask
│       ├── service/AgentService.java           ← calls FastAPI
│       └── dto/  (QuestionRequest, AgentResponse)
│
└── angular-ui/
    └── src/app/
        ├── app.component.ts
        ├── chat/
        │   ├── chat.component.ts    ← logic
        │   ├── chat.component.html  ← template
        │   └── chat.component.scss  ← styles
        └── services/chat.service.ts ← HTTP call to Spring Boot
```

<img width="1543" height="976" alt="image" src="https://github.com/user-attachments/assets/7992d9ec-d9f4-4d13-8557-651dbf6ca446" />

