# def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]: — a function with default parameter values. 
# If you call chunk_text(some_text) without specifying chunk_size/overlap, it automatically uses 500 and 50. The -> list[str] at the end is a return type hint — telling readers (and tools) this function returns a list of strings.
# chunks = [] — an empty list we'll fill as we go.
# start = 0 — tracks our current position as we slide through the text.
# while start < len(text): — keep looping as long as there's more text left to process. len(text) gives the total character count.
# end = start + chunk_size — calculates where this particular chunk should stop.
# chunk = text[start:end] — Python's slice syntax again (you saw this with text[:200] earlier) — this grabs the substring from position start up to (but not including) position end. 
# If end goes past the actual end of the string, Python just gives you whatever's left — no error, which is convenient here.
# chunks.append(chunk) — adds this piece to our results list.
# start += chunk_size - overlap — this is the key trick for overlap. Instead of jumping forward by the full chunk_size (which would mean zero overlap), we jump forward by chunk_size - overlap. 
# With chunk_size=500 and overlap=50, we advance by 450 each time — meaning the last 50 characters of one chunk are also the first 50 characters of the next chunk.





def chunk_text(text: str,chunk_size:int= 500,overlap:int = 50)->list[str]:
    chunks = []
    start = 0

    while (start < len(text)):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks