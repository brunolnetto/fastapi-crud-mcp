[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

# FastAPI CRUD MCP

A minimal CRUD API for “items,” built with FastAPI and exposed as MCP tools via FastAPI-MCP. Includes a scenario-driven client harness using PydanticAI and Rich.

---

## 🚀 Features

- **FastAPI**: high-performance HTTP API  
- **SQLAlchemy + Pydantic**: ORM models + input/output schemas  
- **FastAPI-MCP**: auto-expose your endpoints as MCP tools (`/mcp/tools`, `/mcp/events`)  
- **Rich CLI**: beautiful, colored terminal output for scenario runs  
- **Scenario Runner**: client harness that drives and validates your API via PydanticAI agents  
- **SQLite backend** for demo; easily swap to PostgreSQL, MySQL, etc.

---

## 📦 Project Layout

```

.
├── backend
│   ├── server
│   │   ├── main.py            # FastAPI + FastAPI-MCP wiring
│   │   ├── models.py          # SQLAlchemy + Pydantic schemas
│   │   ├── routes.py          # CRUD endpoints
│   │   ├── crud.py            # DB operations
│   │   ├── db.py              # session & engine
│   │   └── logger.py          # stdlib logging setup
│   └── client
│       ├── scenarios.py       # Scenario definitions
│       └── main.py            # run\_scenarios.py harness
├── .env                       # example environment variables
├── pyproject.toml             # Project dependencies
└── README.md                  # this file

````

---

## ⚙️ Installation & Setup

1. **Clone & enter directory**  
   ```bash
   git clone https://github.com/yourusername/fastapi-crud-mcp.git
   cd fastapi-crud-mcp
   ```

2. **Create & activate a virtualenv**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   uv sync
   ```

4. **Environment variables**
   Copy the example and adjust if needed:

   ```bash
   cp .env.example .env
   ```

   ```env
   MCP_HOST_URL='http://127.0.0.1:8000/mcp'

   LLM_PROVIDER='openai'
   LLM_MODEL_NAME='gpt-4o-mini'
   LLM_MODEL=${LLM_PROVIDER}:${LLM_MODEL_NAME}

   OPENAI_API_KEY=sk-proj-your-api-key-here
   ```

---

## 🏃 Running the Server

```bash
docker compose up -d --build
```

* **API docs** → `http://localhost:8000/docs`
* **OpenAPI JSON** → `http://localhost:8000/openapi.json`

---

## 🤖 Running the Scenario Client

```bash
python3 -m backend.client.main
```

This harness will:

1. Load your `.env` settings
2. Spin up a PydanticAI agent against `MCP_HOST_URL`
3. Execute each scenario (create/list/get/update/delete)
4. Display rich panels for prompts & outputs

---

## 🚨 Notes & Tips

* **Switch DB**: edit `backend/server/db.py` for PostgreSQL or MySQL.
* **Add auth**: protect `/mcp` or `/api` via FastAPI dependencies.
* **Extend scenarios**: drop new entries into `backend/client/scenarios.py`.
* **Production**: add Alembic for migrations, and monitor with Prometheus.

---

## 🤝 Contributing

1. Fork 🔱
2. Create a feature branch:

   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit & push:

   ```bash
   git commit -am "Add awesome feature"
   git push origin feature/my-feature
   ```
4. Open a PR and we’ll review!

---

## 📄 License

This project is MIT-licensed—see the [LICENSE](LICENSE) file for details.
