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
// return response.json() — parses the response body from JSON text into a usable JavaScript object.



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