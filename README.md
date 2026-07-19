# RAG Knowledge Assistant

🚧 **Status: Actively in development** — Week 5 in progress (Full-stack RAG pipeline working end to end: login, permission-aware retrieval, LLM generation, citations, all connected through a working UI). Continuing frontend polish and error handling next.

A permission-aware RAG system where document retrieval respects role-based access control — built to explore how enterprise RAG systems handle the "different users see different documents" problem.

## Progress
- [x] FastAPI backend scaffolding
- [x] PostgreSQL + SQLAlchemy integration
- [x] User signup with bcrypt password hashing
- [x] JWT-based login and protected routes
- [x] Role-based document permissions
- [x] File upload, chunking, and embedding generation
- [x] Permission-aware semantic search with relevance threshold
- [x] RAG generation with citations (local LLM via Ollama)
- [x] React frontend with persistent auth and chat interface
- [x] Admin panel
- [x] Streaming responses
- [x] Rate limiting on LLM endpoints
- [x] Input validation and prompt-injection awareness
- [x] Structured audit logging
- [ ] Cloud deployment

## Tech Stack
FastAPI · PostgreSQL · SQLAlchemy · pgvector · React · Anthropic API

## Why this project
Most RAG demos ignore access control entirely — this one enforces permissions at the retrieval layer itself, not as an afterthought.
