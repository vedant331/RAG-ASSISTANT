// useState<string | null>(null) — TypeScript generic syntax specifying this state can be either a string or null. Starts as null (not logged in).
// if (!token) { return <LoginPage ... /> } — if there's no token yet, show the login page instead of the main app. This is conditional rendering 
// — a core React pattern for showing different UI based on state.
// onLoginSuccess={setToken} — passing React's own setToken function directly as the prop 
// — when LoginPage calls onLoginSuccess(someToken), it's really calling setToken(someToken), updating App's state, which causes App to re-render and show the logged-in view instead.

import { useState, useEffect } from "react"
import LoginPage from "./LoginPage"
import ChatPage from "./ChatPage"
import AdminPage from "./AdminPage"
import { getCurrentUser } from "./api"

function App() {
  const [token, setToken] = useState<string | null>(null)
  const [role, setRole] = useState<string | null>(null)
  const [view, setView] = useState<"chat" | "admin">("chat")

  useEffect(() => {
    const storedToken = localStorage.getItem("token")
    if (storedToken) {
      setToken(storedToken)
    }
  }, [])

  useEffect(() => {
    if (token) {
      getCurrentUser(token)
        .then((data) => setRole(data.role))
        .catch(() => handleLogout())
    }
  }, [token])

  function handleLoginSuccess(newToken: string) {
    localStorage.setItem("token", newToken)
    setToken(newToken)
  }

  function handleLogout() {
    localStorage.removeItem("token")
    setToken(null)
    setRole(null)
    setView("chat")
  }

  if (!token) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />
  }

  return (
    <div className="min-h-screen bg-bg text-text font-sans flex flex-col">
      <header className="border-b border-border px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-6">
          <p className="font-mono text-xs text-text-muted uppercase tracking-wider">
            RAG Knowledge Assistant
          </p>
          <button
            onClick={() => setView("chat")}
            className={`font-mono text-xs ${view === "chat" ? "text-accent" : "text-text-muted"}`}
          >
            Chat
          </button>
          {role === "admin" && (
            <button
              onClick={() => setView("admin")}
              className={`font-mono text-xs ${view === "admin" ? "text-accent" : "text-text-muted"}`}
            >
              Admin
            </button>
          )}
        </div>
        <button
          onClick={handleLogout}
          className="font-mono text-xs text-text-muted hover:text-text transition-colors"
        >
          Log out
        </button>
      </header>

      {view === "admin" && role === "admin" ? (
  <AdminPage token={token} />
) : (
  <ChatPage token={token} onLogout={handleLogout} embedded />
)}
    </div>
  )
}

export default App