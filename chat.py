import json
import faiss
import numpy as np
import subprocess
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/index.faiss")

with open("data/chunks.json") as f:
    chunks = json.load(f)

def search(query, k=3):
    q_emb = model.encode([query]).astype("float32")
    _, idxs = index.search(q_emb, k)
    return [chunks[i] for i in idxs[0]]

def ask_ollama(context, question):
    prompt = f"""
You are helping understand a codebase.

Context:
{context}

Question:
{question}

Answer clearly and mention file names.
"""
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or exit): ")
        if q.lower() == "exit":
            break

        results = search(q)

        context = ""
        for r in results:
            context += f"\nFile: {r['file']}\n{r['code'][:800]}\n"

        answer = ask_ollama(context, q)
        print("\n🧠 Answer:\n")
        print(answer)
