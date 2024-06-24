from sentence_transformers import SentenceTransformer
from database import get_db_conn
import faiss
import numpy as np

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_documents():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name, editorial
    FROM cleaned_editorials
    LIMIT 10
    """
    )
    names = []
    editorials = []
    for name, editorial in cursor.fetchall():
        names.append(name)
        editorials.append(editorial)
    cursor.close()
    conn.close()
    return names, editorials

# Sample documents and a query
names, editorials = get_documents()
documents = editorials
query = "All the prime numbers less than 10 are 2, 3, 5, 7."

# Generate embeddings for documents
document_embeddings = model.encode(documents)

# Generate embedding for the query
query_embedding = model.encode([query])

# Convert embeddings to a float32 numpy array
document_embeddings = np.array(document_embeddings).astype('float32')
query_embedding = np.array(query_embedding).astype('float32')

# Build the FAISS index
print(document_embeddings.shape)
exit(0)
index = faiss.IndexFlatL2(document_embeddings.shape[1])  # L2 distance
index.add(document_embeddings)

# Perform the search
k = 5  # Number of nearest neighbors
D, I = index.search(query_embedding, k)

# D: distances, I: indices of the nearest neighbors
print(D)
top_5_doc_ids = I[0]
top_5_docs = [documents[i] for i in top_5_doc_ids]

print("Top 5 similar documents and their IDs:", top_5_doc_ids)
print("Top 5 similar names:", [names[i] for i in top_5_doc_ids])
print("Top 5 similar documents:", top_5_docs)
