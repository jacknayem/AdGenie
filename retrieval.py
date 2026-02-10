import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Simulating a Product Database (The Public Data)
data = [
    {"id": 1, "name": "EcoSmart Water Bottle", "category": "Lifestyle", "desc": "Self-cleaning, insulated stainless steel bottle that tracks hydration."},
    {"id": 2, "name": "Urban Glide E-Scooter", "category": "Transport", "desc": "Foldable electric scooter with 40km range, perfect for city commuting."},
    {"id": 3, "name": "NoiseCancel Pro Headphones", "category": "Tech", "desc": "Over-ear headphones with industry-leading noise cancellation and 30h battery."},
    {"id": 4, "name": "Organic Matcha Kit", "category": "Food", "desc": "Premium ceremonial grade matcha with bamboo whisk and ceramic bowl."}
]
df = pd.DataFrame(data)

# 2. Embedding Model
encoder = SentenceTransformer('all-MiniLM-L6-v2')
# 3. Build the Vector Index (The Retrieval Engine)
vectors = encoder.encode(df['desc'].tolist())
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

def get_best_product(user_query):
    query_vector = encoder.encode([user_query])
    D, I = index.search(query_vector, 1)
    product = df.iloc[I[0][0]]
    return product