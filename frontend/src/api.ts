// const API_BASE_URL = "http://127.0.0.1:8000" — your FastAPI server's address, matching exactly what you've been testing against in /docs this whole time.
// export async function login(...) — export makes this function usable from other files (like import { login } from './api'). 
// async because network requests take time and we need to await them, same concept as your Python async def upload_document.
// fetch(...) — the browser's built-in function for making HTTP requests — this is the frontend equivalent of what your curl commands in Swagger's "
// Try it out" have been doing all along, just written in JavaScript instead of generated for you.
// method: "POST" — same HTTP method concept from your backend.
// headers: { "Content-Type": "application/json" } — tells the server "the body I'm sending is JSON" — matches what FastAPI expects for your LoginRequest Pydantic model.
// body: JSON.stringify({ email, password }) — converts a JavaScript object into a JSON string to send over the network. { email, password } is JavaScript shorthand for { email: email, password: password } 
// — if a variable name matches the key name, you can skip repeating it.
// if (!response.ok) — response.ok is true for any successful HTTP status (200-299), false otherwise (like your 401 for wrong credentials). 
// This is how JavaScript checks for errors, since fetch doesn't automatically throw an error on a 401/400 the way you might expect.
// // return response.json() — parses the response body from JSON text into a usable JavaScript object.
// encodeURIComponent(query) — your /ask endpoint takes query as a URL parameter (?query=...), same as it did in /docs. 
// But raw text can contain spaces, question marks, and other characters that would break a URL if inserted directly. 
// encodeURIComponent safely converts those into URL-safe encoding (e.g. a space becomes %20) — this is the JavaScript equivalent of what Swagger's "Try it out" was doing invisibly for you this whole time.
// headers: { "Authorization": \Bearer ${token}` }` — this is the exact same header format you've been manually pasting into Swagger's "Authorize" button, 
// now built programmatically. This is how your protected endpoint knows who's asking.
// // Notice: no body this time, since GET requests don't send a request body — all the info needed (query in the URL, token in the header) travels outside the body.
// response.status === 401 — specifically checks for the "unauthorized" status code (your backend returns this for expired/invalid tokens), distinct from other kinds of failures.
// throw new Error("UNAUTHORIZED") — a specific, recognizable error message.
// // Back in ChatPage, err.message === "UNAUTHORIZED" catches this specific case and calls onLogout() — automatically clearing the stale token and kicking the user back to the login screen, rather than leaving them stuck with a confusing generic error.
// new FormData() — this is the browser's built-in way of building a multipart/form-data payload 
// (remember this term from Day 16 — it's what your /documents/upload endpoint expects, since it handles both a text field and a file together).
// formData.append("title", title) / formData.append("file", file) 
// — adds each piece, matching the exact field names your FastAPI endpoint expects (title: str and file: UploadFile).
// Notice: no "Content-Type": "application/json" header for the upload function — when sending FormData, 
// // the browser automatically sets the correct multipart/form-data content type (including a special boundary marker) for you. Manually setting it yourself would actually break the request
// onChunk: (text: string) => void and onDone: (sources: Source[]) => void — this function takes callback functions as parameters, rather than returning a single value. Since data arrives progressively, we can't just return one final answer — instead, we call onChunk every time a new piece arrives, and onDone once at the very end. The calling code (in ChatPage) will define what these callbacks actually do.
// response.body.getReader() — gets a low-level reader for the raw response stream, letting you pull data as it arrives instead of waiting for the whole thing.
// const decoder = new TextDecoder() — the stream arrives as raw bytes; TextDecoder converts those bytes into readable text.
// while (true) { const { done, value } = await reader.read() ... } — an infinite loop that keeps pulling more data until done becomes true (meaning the stream has ended).
// buffer += decoder.decode(value, { stream: true }) — appends newly-decoded text to a running buffer, since a single "chunk" of bytes from the network might contain a partial event, or multiple events at once.
// buffer.split("\n\n") — splits the buffer on our SSE event separator. parts.pop() removes and returns the last element (which might be an incomplete event still waiting for more data) and keeps it in buffer for next time, while everything else in parts is a complete, ready-to-process event.
// part.slice(6) — removes the literal "data: " prefix (6 characters) to get just the JSON portion.
// JSON.parse(jsonStr) — converts the JSON string back into a real JavaScript object.


import type { Source } from "./types"

const API_BASE_URL = "http://127.0.0.1:8000"

export async function login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
        throw new Error("Incorrect email or password")
    }
    return response.json()
}

export async function askQuestion(query: string, token: string) {
  const response = await fetch(`${API_BASE_URL}/ask?query=${encodeURIComponent(query)}`, {
    method: "GET",
    headers: { "Authorization": `Bearer ${token}` },
  })

  if (response.status === 401) {
    throw new Error("UNAUTHORIZED")
  }

  if (!response.ok) {
    throw new Error("Failed to get an answer")
  }

  return response.json()
}
export async function getCurrentUser(token: string) {
  const response = await fetch(`${API_BASE_URL}/me`, {
    method: "GET",
    headers: { "Authorization": `Bearer ${token}` },
  })

  if (!response.ok) {
    throw new Error("UNAUTHORIZED")
  }

  return response.json()
}

export async function uploadDocument(title: string, file: File, token: string) {
  const formData = new FormData()
  formData.append("title", title)
  formData.append("file", file)

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: formData,
  })

  if (!response.ok) {
    throw new Error("Upload failed")
  }

  return response.json()
}

export async function grantPermission(documentId: number, roleName: string, token: string) {
  const response = await fetch(`${API_BASE_URL}/documents/${documentId}/permissions`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ role_name: roleName }),
  })

  if (!response.ok) {
    throw new Error("Failed to grant permission")
  }

  return response.json()
}
export async function askQuestionStream(
  query: string,
  token: string,
  onChunk: (text: string) => void,
  onDone: (sources: Source[]) => void
) {
  const response = await fetch(`${API_BASE_URL}/ask/stream?query=${encodeURIComponent(query)}`, {
    method: "GET",
    headers: { "Authorization": `Bearer ${token}` },
  })

  if (response.status === 401) {
    throw new Error("UNAUTHORIZED")
  }

  if (!response.ok || !response.body) {
    throw new Error("Failed to get an answer")
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const parts = buffer.split("\n\n")
    buffer = parts.pop() ?? ""

    for (const part of parts) {
      if (!part.startsWith("data: ")) continue
      const jsonStr = part.slice(6)
      const event = JSON.parse(jsonStr)

      if (event.type === "chunk") {
        onChunk(event.text)
      } else if (event.type === "done") {
        onDone(event.sources)
      }
    }
  }
}