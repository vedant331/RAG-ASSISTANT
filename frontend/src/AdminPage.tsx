// e.target.files?.[0] ?? null — file inputs give you a FileList (technically supporting multiple files), even for single-file inputs. ?.[0] safely grabs the first file if it exists (the ?. is optional chaining — prevents an error if files happens to be null). ?? null (the nullish coalescing operator) falls back to null if the whole expression is undefined.
// Number(documentId) — since our input's value is always a string in React (even for type="number" inputs), we convert it to an actual number before sending it, matching what your backend's document_id: int expects.




import { useState } from "react"
import { uploadDocument, grantPermission } from "./api"

interface AdminPageProps {
  token: string
}

function AdminPage({ token }: AdminPageProps) {
  const [title, setTitle] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [uploadStatus, setUploadStatus] = useState("")

  const [documentId, setDocumentId] = useState("")
  const [roleName, setRoleName] = useState("")
  const [permissionStatus, setPermissionStatus] = useState("")

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault()
    if (!file) return

    setUploadStatus("Uploading...")
    try {
      const data = await uploadDocument(title, file, token)
      setUploadStatus(`Uploaded. Document ID: ${data.id}, ${data.num_chunks} chunks created.`)
      setTitle("")
      setFile(null)
    } catch (err) {
      setUploadStatus("Upload failed.")
    }
  }

  async function handleGrant(e: React.FormEvent) {
    e.preventDefault()
    setPermissionStatus("Granting...")
    try {
      const data = await grantPermission(Number(documentId), roleName, token)
      setPermissionStatus(data.message)
      setDocumentId("")
      setRoleName("")
    } catch (err) {
      setPermissionStatus("Failed to grant permission.")
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-10 space-y-10">
      <div>
        <p className="font-mono text-xs text-text-muted uppercase tracking-wider mb-4">
          Upload Document
        </p>
        <form onSubmit={handleUpload} className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Document title"
            className="w-full bg-surface border border-border text-text px-3 py-2 font-sans text-sm focus:outline-none focus:border-accent"
            required
          />
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="w-full font-mono text-xs text-text-muted"
            required
          />
          <button
            type="submit"
            className="bg-accent text-bg font-mono text-sm px-4 py-2 hover:opacity-90 transition-opacity"
          >
            Upload
          </button>
          {uploadStatus && (
            <p className="font-mono text-xs text-text-muted">{uploadStatus}</p>
          )}
        </form>
      </div>

      <div>
        <p className="font-mono text-xs text-text-muted uppercase tracking-wider mb-4">
          Grant Permission
        </p>
        <form onSubmit={handleGrant} className="space-y-3">
          <input
            type="number"
            value={documentId}
            onChange={(e) => setDocumentId(e.target.value)}
            placeholder="Document ID"
            className="w-full bg-surface border border-border text-text px-3 py-2 font-sans text-sm focus:outline-none focus:border-accent"
            required
          />
          <input
            type="text"
            value={roleName}
            onChange={(e) => setRoleName(e.target.value)}
            placeholder="Role name (e.g. hr, engineering)"
            className="w-full bg-surface border border-border text-text px-3 py-2 font-sans text-sm focus:outline-none focus:border-accent"
            required
          />
          <button
            type="submit"
            className="bg-accent text-bg font-mono text-sm px-4 py-2 hover:opacity-90 transition-opacity"
          >
            Grant
          </button>
          {permissionStatus && (
            <p className="font-mono text-xs text-text-muted">{permissionStatus}</p>
          )}
        </form>
      </div>
    </div>
  )
}

export default AdminPage