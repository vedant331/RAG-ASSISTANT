# RAG Knowledge Assistant

🚧 **Status: Actively in development** — Week 1 of 7 complete (Auth system done, building document permissions next).

A permission-aware RAG system where document retrieval respects role-based access control — built to explore how enterprise RAG systems handle the "different users see different documents" problem.

## Progress
- [x] FastAPI backend scaffolding
- [x] PostgreSQL + SQLAlchemy integration
- [x] User signup with bcrypt password hashing
- [x] JWT-based login and protected routes
- [ ] Role-based document permissions (in progress)
- [ ] Vector search with pgvector
- [ ] RAG generation with citations
- [ ] React frontend
- [ ] Cloud deployment

## Tech Stack
FastAPI · PostgreSQL · SQLAlchemy · pgvector · React · Anthropic API

## Why this project
Most RAG demos ignore access control entirely — this one enforces permissions at the retrieval layer itself, not as an afterthought.
