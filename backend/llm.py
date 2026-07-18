# What changed from the Anthropic version, conceptually: 
# the shape of a RAG prompt (system instructions + context + question) is identical — that's a provider-agnostic pattern. 
# Only the actual API call syntax differs: ollama.chat(...) instead of client.messages.create(...), and the response is a plain dictionary (response["message"]["content"]) instead of an object with .content[0].text.
# You can now remove ANTHROPIC_API_KEY from your .env file if you'd like (not required, just unused) — 
# and no need for the anthropic or python-dotenv packages for this specific file anymore, though no harm leaving them installed.

import ollama

def generate_answer(question:str,context_chunks:list[str])->str:
    context_text = "\n\n---\n\n".join(context_chunks)

    system_prompt = (
        "You are a helpful assistant answering questions using only the provided context. "
        "If the answer cannot be found in the context, say so clearly instead of guessing. "
        "Be concise and direct."
    )

    user_message = f"Context:\n{context_text}\n\nQuestion: {question}"

    response = ollama.chat(
        model="llama3.2",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response["message"]["content"]