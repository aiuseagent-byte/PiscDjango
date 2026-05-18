# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the development server
uv run manage.py runserver

# Run the async task worker (required for AI processing pipeline)
uv run manage.py qcluster

# Database migrations
uv run manage.py makemigrations
uv run manage.py migrate

# Run tests
uv run manage.py test

# Run a single app's tests
uv run manage.py test usuarios
uv run manage.py test consultas
```

> The project uses `uv` as the package manager. All Python commands should be prefixed with `uv run`.

## Architecture

**PsiQue** is a Django 6 web app for psychologists to manage patients and therapy sessions, with an AI layer that automatically transcribes session recordings and builds a per-patient RAG knowledge base.

### Apps

- **`usuarios/`** — User auth (cadastro/login) and `Pacientes` model. The `pacientes` view is re-exported from `consultas/urls.py`, so the canonical URL for the patient list is `/consultas/pacientes/`.
- **`consultas/`** — Core domain: recording uploads, AI pipeline, chat interface, and WhatsApp messaging.

### AI Processing Pipeline

When a `Gravacoes` object is saved with `transcrever=True`, the `post_save` signal in `consultas/signals.py` fires a **Django-Q Chain** that runs three async tasks sequentially:

1. `transcribe_recording` — sends the audio file to OpenAI Whisper (`whisper-1`) and saves the transcript + segments.
2. `task_rag` — chunks the transcript with `RecursiveCharacterTextSplitter` and upserts into a **per-patient FAISS index** stored at `faiss/banco_faiss_{paciente_id}/`.
3. `summary_recording` — runs `SummaryAgent` (bullet-point summary) and `EvaluationAgent` (mood score 1–5) via `gpt-4.1-mini` with Pydantic structured output.

The worker (`qcluster`) must be running in a separate terminal for any AI tasks to execute.

### RAG Chat

`RAGContext.retrieval()` is a generator. It performs FAISS similarity search (with optional date filtering parsed from the question), saves `DataTreinamento` references, then streams the LLM response token-by-token via `StreamingHttpResponse` at `/consultas/stream_response/<id>`.

### Prompts

All LLM system prompts live in `prompts/prompts.py` (`SUMMARY_PROMPT`, `PSI_PROMPT`, `EVALUATION_PROMPT`). Edit there to change AI behavior.

### Key configuration

All secrets and environment flags are loaded via `python-decouple` from `.env`:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local dev, omit or `False` for production |
| `OPENAI_API_KEY` | Used by Whisper, embeddings, and all LangChain agents |

The `Q_CLUSTER` config in `settings.py` uses the Django ORM as broker (`"orm": "default"`) — no Redis or RabbitMQ needed.

### Known security issues (pending fixes)

- `@csrf_exempt` on `stream_response` and `chat` views in `consultas/views.py`.
- No `@login_required` on any view — all routes are publicly accessible.
- Password validation in `usuarios/views.py:cadastro` is done manually (min 6 chars) instead of using Django's `AUTH_PASSWORD_VALIDATORS`.
- No logout URL exists.
