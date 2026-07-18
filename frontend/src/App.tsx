// useState<string | null>(null) — TypeScript generic syntax specifying this state can be either a string or null. Starts as null (not logged in).
// if (!token) { return <LoginPage ... /> } — if there's no token yet, show the login page instead of the main app. This is conditional rendering 
// — a core React pattern for showing different UI based on state.
// onLoginSuccess={setToken} — passing React's own setToken function directly as the prop 
// — when LoginPage calls onLoginSuccess(someToken), it's really calling setToken(someToken), updating App's state, which causes App to re-render and show the logged-in view instead.

import { useState, useEffect } from "react"
import LoginPage from "./LoginPage"
import ChatPage from "./ChatPage"

function App() {
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const storedToken = localStorage.getItem("token")
    if (storedToken) {
      setToken(storedToken)
    }
  }, [])

  function handleLoginSuccess(newToken: string) {
    localStorage.setItem("token", newToken)
    setToken(newToken)
  }

  function handleLogout() {
    localStorage.removeItem("token")
    setToken(null)
  }

  if (!token) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />
  }

  return <ChatPage token={token} onLogout={handleLogout} />
}

export default App