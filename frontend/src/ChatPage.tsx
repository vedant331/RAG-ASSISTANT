// const [messages, setMessages] = useState<ChatMessage[]>([]) 
// — state holding an array of ChatMessage objects, starting empty.
// setMessages((prev) => [...prev, newMessage]) 
// — this is the correct way to add an item to a state array in React. prev is the current array; [...prev, newMessage] creates a brand new array containing everything from prev plus newMessage at the end. The ... is JavaScript's spread syntax — it "unpacks" an existing array's items into a new one. Important: you never modify prev directly (like prev.push(...)) — React requires you to create a new array/object for it to correctly detect the change and re-render.
// finally { setLoading(false) } 
// — runs whether the try succeeded or the catch caught an error, guaranteeing the loading state always gets cleared either way.
// {messages.map((msg, i) => (...))} 
// — loops over the array, rendering one block per message. key={i} is a required React prop when rendering lists — it helps React efficiently track which items changed between renders (using the array index here is acceptable for this simple case, though not always ideal for lists that reorder).
// disabled={loading} — disables the button while a request is in flight, preventing duplicate submissions.
// &gt; — the HTML entity for >, used here as a small terminal-style prompt marker before each question (> your question here) 
// — a tiny detail reinforcing the engineering-console feel.
// The citation tags: [{source.document_title}] rendered in text-citation (your amber accent) with a hairline border 
// — exactly the signature element from your design plan, now implemented.




import { useState } from "react"
import { askQuestion } from "./api"
import type { ChatMessage } from "./types"

interface ChatPageProps {
  token: string
}

function ChatPage({ token }: ChatPageProps) {
  const [query, setQuery] = useState("")
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError("")

    try {
      const data = await askQuestion(query, token)
      const newMessage: ChatMessage = {
        question: query,
        answer: data.answer,
        sources: data.sources,
      }
      setMessages((prev) => [...prev, newMessage])
      setQuery("")
    } catch (err) {
      setError("Something went wrong. Try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-bg text-text font-sans flex flex-col">
      <header className="border-b border-border px-6 py-4">
        <p className="font-mono text-xs text-text-muted uppercase tracking-wider">
          RAG Knowledge Assistant
        </p>
      </header>

      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 max-w-3xl w-full mx-auto">
        {messages.length === 0 && (
          <p className="font-mono text-sm text-text-muted">
            No questions asked yet. Ask something below.
          </p>
        )}

        {messages.map((msg, i) => (
          <div key={i} className="space-y-2">
            <p className="font-mono text-sm text-accent">&gt; {msg.question}</p>
            <p className="font-sans text-sm text-text leading-relaxed">{msg.answer}</p>
            {msg.sources.length > 0 && (
              <div className="flex flex-wrap gap-2 pt-1">
                {msg.sources.map((source, j) => (
                  <span
                    key={j}
                    className="font-mono text-xs text-citation border border-border px-2 py-0.5"
                  >
                    [{source.document_title}]
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <p className="font-mono text-sm text-text-muted">Generating answer...</p>
        )}

        {error && (
          <p className="font-mono text-sm text-citation">{error}</p>
        )}
      </div>

      <form onSubmit={handleSubmit} className="border-t border-border px-6 py-4">
        <div className="max-w-3xl w-full mx-auto flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 bg-surface border border-border text-text px-3 py-2 font-mono text-sm focus:outline-none focus:border-accent"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-accent text-bg font-mono text-sm px-4 py-2 hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            Ask
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatPage