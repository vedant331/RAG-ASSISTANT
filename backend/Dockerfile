FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



# FROM python:3.11-slim — starts from an official, minimal Python 3.11 base image (the foundation everything else builds on top of). Using 3.11 here specifically rather than matching your exact 3.14 local install — cloud deployment images commonly use a well-tested LTS-adjacent version rather than the very newest release, for stability. Your code doesn't use anything 3.14-specific, so this is safe.
# WORKDIR /app — sets the working directory inside the container to /app, similar to how you cd into backend/ locally — every subsequent command runs relative to this location inside the container.
# COPY requirements.txt . — copies just this one file in first, before the rest of your code. This is a deliberate optimization: Docker caches each step, so if you change your actual code but not your dependencies, Docker can reuse the cached "install packages" step instead of redoing it every time — faster rebuilds.
# RUN pip install --no-cache-dir -r requirements.txt — installs every package listed, inside the container. --no-cache-dir keeps the resulting image smaller by not keeping pip's download cache around afterward.
# COPY . . — now copies the rest of your actual code (main.py, models.py, etc.) into the container.
# EXPOSE 8000 — documents that this container listens on port 8000 (informational — doesn't actually open the port by itself, that happens at runtime).
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] — the command that runs when the container starts. Notice: no --reload this time — that flag is for local development only; production containers should run without it. Also notice --host 0.0.0.0 instead of the implicit 127.0.0.1 — 0.0.0.0 means "listen on all network interfaces," necessary for the container to be reachable from outside itself (a cloud platform routing traffic in).