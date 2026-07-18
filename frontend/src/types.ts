// This directly mirrors your backend's /ask response shape — 
// sources: Source[] means "an array of Source objects," matching the list[dict] your FastAPI endpoint returns.


export interface Source {
  document_title: string
  document_id: number
}

export interface ChatMessage {
  question: string
  answer: string
  sources: Source[]
}