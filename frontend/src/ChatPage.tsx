import { useState } from "react"
import { askQuestionStream } from "./api"
import type { ChatMessage } from "./types"

interface ChatPageProps {
  token: string
  onLogout: () => void
  embedded?: boolean
}

function ChatPage({ token, onLogout }: ChatPageProps) {
  const [query, setQuery] = useState("")
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()

    if (!query.trim() || loading) return

    const currentQuery = query.trim()

    setLoading(true)
    setError("")
    setQuery("")

    const newMessage: ChatMessage = {
      question: currentQuery,
      answer: "",
      sources: [],
    }

    setMessages((prev) => [...prev, newMessage])

    try {
      await askQuestionStream(
        currentQuery,
        token,

        // Streaming callback
        (chunkText: string) => {
          setMessages((prev) => {
            const updated = [...prev]

            updated[updated.length - 1] = {
              ...updated[updated.length - 1],
              answer:
                updated[updated.length - 1].answer + chunkText,
            }

            return updated
          })
        },

        // Final callback
        (sources) => {
          setMessages((prev) => {
            const updated = [...prev]

            updated[updated.length - 1] = {
              ...updated[updated.length - 1],
              sources,
            }

            return updated
          })

          setLoading(false)
        }
      )
    } catch (err) {
      if (err instanceof Error && err.message === "UNAUTHORIZED") {
        onLogout()
      } else {
        console.error(err)
        setError("Something went wrong. Try again.")
        setLoading(false)
      }
    }
  }

  return (
    <div className="flex-1 flex flex-col">
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 max-w-3xl w-full mx-auto">
        {messages.length === 0 && (
          <p className="font-mono text-sm text-text-muted">
            No questions asked yet. Ask something below.
          </p>
        )}

        {messages.map((msg, i) => (
          <div key={i} className="space-y-2">
            <p className="font-mono text-sm text-accent">
              &gt; {msg.question}
            </p>

            <p className="font-sans text-sm text-text leading-relaxed whitespace-pre-wrap">
              {msg.answer || (loading && i === messages.length - 1 ? "..." : "")}
            </p>

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
          <p className="font-mono text-sm text-text-muted">
            Generating answer...
          </p>
        )}

        {error && (
          <p className="font-mono text-sm text-citation">
            {error}
          </p>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-border px-6 py-4"
      >
        <div className="max-w-3xl w-full mx-auto flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
            className="flex-1 bg-surface border border-border text-text px-3 py-2 font-mono text-sm focus:outline-none focus:border-accent disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="bg-accent text-bg font-mono text-sm px-4 py-2 hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatPage