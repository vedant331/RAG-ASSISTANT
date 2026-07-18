// useState<string | null>(null) — TypeScript generic syntax specifying this state can be either a string or null. Starts as null (not logged in).
// if (!token) { return <LoginPage ... /> } — if there's no token yet, show the login page instead of the main app. This is conditional rendering 
// — a core React pattern for showing different UI based on state.
// onLoginSuccess={setToken} — passing React's own setToken function directly as the prop 
// — when LoginPage calls onLoginSuccess(someToken), it's really calling setToken(someToken), updating App's state, which causes App to re-render and show the logged-in view instead.

import { useState } from "react"
import LoginPage from "./LoginPage"

function App() {
  const [token, setToken] = useState<string | null>(null)

  if (!token) {
    return <LoginPage onLoginSuccess={setToken} />
  }

  return (
    <div className="min-h-screen bg-bg text-text font-sans p-8">
      <p className="font-mono text-sm">Logged in. Token stored.</p>
    </div>
  )
}

export default App