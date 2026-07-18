// interface LoginPageProps { onLoginSuccess: (token: string) => void } — TypeScript's way of declaring "this component expects to receive a function called onLoginSuccess that takes a string and returns nothing." 
// This is how a parent component (which we'll build next) tells a child component (this one) what to do after login succeeds — the child doesn't handle navigation itself, it just reports back "here's the token" 
// and lets the parent decide what happens next.
// function LoginPage({ onLoginSuccess }: LoginPageProps) — this is called destructuring the props — pulling onLoginSuccess directly out of the props object, rather than writing props.onLoginSuccess everywhere.
// const [email, setEmail] = useState("") — this is React's core state mechanism, called a Hook. email is the current value, setEmail is the function you call to update it, and useState("") sets the starting value to an empty string. 
// Whenever setEmail is called, React automatically re-renders this component with the new value — this is the fundamental way React handles anything that changes on screen.
// async function handleSubmit(e: React.FormEvent) — runs when the form is submitted. e: React.FormEvent is the type of the form submission event.
// e.preventDefault() — by default, HTML forms try to reload the whole page on submit (old-school browser behavior) — this line stops that, since we're handling the submission ourselves via JavaScript instead.
// try { ... } catch (err) { ... } — same error-handling pattern as Python's try/except, just different syntax.
// onLoginSuccess(data.access_token) — calls the function passed in from the parent, handing it the token we got back from your API.
// onChange={(e) => setEmail(e.target.value)} — this is what makes the input controlled: every keystroke triggers this function, which updates the email state with whatever's currently typed. e.target.value is the input's current text.
// {error && (...)} — a common React pattern: "if error is a non-empty string (truthy), render what follows; otherwise render nothing." This is how you conditionally show/hide elements.
// Notice the Tailwind classes directly reflect your design tokens from Day 29: bg-bg, border-border, text-text-muted, text-accent — these all come from the @theme block you set up, proving that setup is working.
// Sharp edges (no rounded-* classes anywhere), hairline border-border instead of shadows, monospace labels — this is your engineering-console direction actually showing up in real code now.



import { useState } from "react"
import { login } from "./api"

interface LoginPageProps {
  onLoginSuccess: (token: string) => void
}

function LoginPage({ onLoginSuccess }: LoginPageProps) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError("")

    try {
      const data = await login(email, password)
      onLoginSuccess(data.access_token)
    } catch (err) {
      setError("Incorrect email or password")
    }
  }

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center">
      <div className="w-full max-w-sm border border-border bg-surface p-8">
        <div className="mb-6">
          <p className="font-mono text-xs text-text-muted uppercase tracking-wider">
            RAG Knowledge Assistant
          </p>
          <h1 className="font-mono text-lg text-text mt-1">Sign in</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-mono text-xs text-text-muted mb-1">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-bg border border-border text-text px-3 py-2 font-sans focus:outline-none focus:border-accent"
              required
            />
          </div>

          <div>
            <label className="block font-mono text-xs text-text-muted mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-bg border border-border text-text px-3 py-2 font-sans focus:outline-none focus:border-accent"
              required
            />
          </div>

          {error && (
            <p className="font-mono text-xs text-citation">{error}</p>
          )}

          <button
            type="submit"
            className="w-full bg-accent text-bg font-mono text-sm py-2 hover:opacity-90 transition-opacity"
          >
            Sign in
          </button>
        </form>
      </div>
    </div>
  )
}

export default LoginPage