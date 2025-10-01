# Continuing the Local AI Bot Chat From a Fresh VS Code Window

The Local AI Bot stack is split into a FastAPI backend (`src/web_api.py`) and a Vite/React frontend (`frontend/`).  Follow the steps below any time you want to reopen the project in a clean editor window and keep working with the chat experience.

---

## 1. Pre-flight Checklist

Make sure these tools are available on your machine:

| Requirement | How to verify | Notes |
| --- | --- | --- |
| Python 3.10+ | `python3 --version` | Used for the FastAPI backend and processors |
| Node.js 18+ & npm | `node --version`, `npm --version` | Needed for the Vite dev server |
| Ollama | `ollama --version` | LLM runtime; ensure `ollama serve` can reach `http://localhost:11434` |
| (Optional) Docker Desktop | `docker --version` | Only required if you plan to launch Open WebUI via `./scripts/start-webui.sh` |

> Tip: if you ran `setup.sh` previously, most prerequisites—including the recommended models—may already be satisfied.

---

## 2. Open the Project in a New Window

1. Launch a fresh VS Code window (`⌘⇧N`).
2. Use **File → Open Folder…** and select `local-ai-bot/` (full path: `/Users/yancyshepherd/MEGA/PythonProjects/GCG/local-ai-bot`).
3. Once the editor finishes indexing, open an integrated terminal (``⌃` ``) so the next commands run in the repository root.

---

## 3. Prepare the Python Environment

> Skip these commands if `.venv/` already exists and you simply want to reuse it.

```bash
# From local-ai-bot/
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

When you finish for the day, you can deactivate the virtual environment with `deactivate`.

---

## 4. Install/Refresh Frontend Dependencies

```bash
# Still in local-ai-bot/
cd frontend
npm install
cd ..
```

Do this once per environment (or whenever `package.json` changes).

---

## 5. Confirm Ollama Models

`src/web_api.py` defaults to the `phi3:3.8b` model. Make sure the models you expect to use are available:

```bash
ollama list
# Optional pulls that mirror current defaults
ollama pull phi3:3.8b
ollama pull llama3.1
ollama pull nomic-embed-text
```

Keep the Ollama service running: `ollama serve` (it usually starts automatically when a model is requested).

---

## 6. Launch the Stack

You have two options.

### Option A: One-touch Dev Script (recommended during iteration)

```bash
# From local-ai-bot/
./dev.sh
```

Requirements: `.venv` must exist, and `frontend/package.json` should be present.  The script boots:

- FastAPI backend with auto-reload on `http://localhost:8899`
- Vite dev server with hot reload on `http://localhost:3000`

Press `Ctrl+C` to stop both servers.

### Option B: Manual Control (backend & frontend in separate terminals)

#### Backend

```bash
# Terminal 1 in local-ai-bot/
source .venv/bin/activate
PYTHONPATH=$(pwd) uvicorn src.web_api:app \
  --host 0.0.0.0 \
  --port 8899 \
  --reload
```

#### Frontend

```bash
# Terminal 2 in local-ai-bot/frontend
npm run dev
```

Vite will print the local URL (default `http://localhost:3000`).

---

## 7. Smoke-test the Services

### Backend Health Check

```bash
curl http://localhost:8899/status | jq
```

Expect JSON containing `api_status`, `ollama_status`, and discovered models.

### Frontend Check

Open `http://localhost:3000` in your browser. If Vite shows a network prompt, allow it to bind to the port.

---

## 8. Continue the Chat Experience

Once the backend is running, you can interact with the chat endpoint directly or through your UI:

```bash
curl -X POST http://localhost:8899/chat \
  -H 'Content-Type: application/json' \
  -d '{
        "message": "Summarize the latest document that was processed.",
        "model": "phi3:3.8b"
      }'
```

The response payload matches `ChatResponse` in `src/web_api.py`.

If you are using a custom frontend (for example the React UI served at port 3000), confirm the app’s API base points to `http://localhost:8899` so chats and document calls flow through the new backend instance.

---

## 9. Document Workflow Recap

- Upload & Process: `POST /api/process-document` with `multipart/form-data` (`file=@path/to/doc.pdf`).
- Save Edited JSON: `POST /api/save-json`
- Generate DOCX: `POST /api/generate-mtl`
- Inspect: `GET /documents/{doc_id}`
- Remove: `DELETE /documents/{doc_id}`

All endpoints are defined in `src/web_api.py`. Results are stored under `data/`.

---

## 10. Graceful Shutdown

- Scripted (`./dev.sh`): press `Ctrl+C`; the trap will terminate both services.
- Manual: `Ctrl+C` in each terminal. If a process lingers, run `pkill -f "uvicorn.*web_api"` or `pkill -f "vite"`.

---

## 11. Troubleshooting Quick Hits

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `Connection refused` when calling `/chat` | Backend not running or wrong port | Re-run `uvicorn`, verify port `8899` |
| `Failed to get response from AI model` | Ollama not serving the requested model | Start `ollama serve` and `ollama pull <model>` |
| `ModuleNotFoundError` for project imports | `PYTHONPATH` not set when launching backend | Use `PYTHONPATH=$(pwd)` or run `./dev.sh` |
| Vite complains about port in use | Old dev server still alive | `pkill -f vite` or choose another port with `npm run dev -- --port 3001` |

---

## 12. Where to Look Next

- Logs: `logs/`
- Processed artifacts: `data/processed/` and `data/uploads/`
- Backend entrypoint: `src/web_api.py`
- Ollama configuration: `config/models.yaml`

You are now ready to keep iterating in your new VS Code window without losing the ability to chat with the Local AI Bot stack.
