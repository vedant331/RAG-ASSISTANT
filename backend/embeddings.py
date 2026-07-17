# model = SentenceTransformer("all-MiniLM-L6-v2") — this line downloads the model the first time it runs 
# (a few hundred MB, cached locally afterward so it won't re-download every time), then loads it into memory. Notice this line sits outside any function, at the top level of the file — meaning it runs once when the file is first imported, not every time you call get_embedding(). This matters for performance: loading a model is slow, so we want to do it once, not on every single request.
# model.encode(text) — the actual embedding call. Feed it a string, get back a vector.
# embedding.tolist() — the model returns its result as a NumPy array (a specialized numerical data structure), 
# but SQLAlchemy's Vector column type expects a plain Python list. .tolist() converts between the two.

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text:str)->list[float]:
    embedding = model.encode(text)
    return embedding.tolist()