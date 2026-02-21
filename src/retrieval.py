import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# ROOT SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'products_clean.csv')
# 1. DATA INGESTION (The Knowledge Base)
if os.path.exists(DATA_PATH):
    print(f"Loading clean data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
else:
    # 1. Simulating a Product Database (The Public Data)
    data = [
        {"name": "EcoSmart Bottle", "category": "Lifestyle", "desc": "Self-cleaning insulated water bottle tracking hydration."},
        {"name": "Urban E-Scooter", "category": "Transport", "desc": "Foldable electric scooter, 40km range, city commuter."},
        {"name": "ZenNoise Headphones", "category": "Tech", "desc": "Active noise cancelling over-ear headphones, 30h battery."},
        {"name": "Glacier Gaming Mouse", "category": "Gaming", "desc": "Ultra-lightweight wireless esports mouse with RGB lighting."},
        {"name": "Chef's Knife Pro", "category": "Kitchen", "desc": "Damascus steel chef knife, razor sharp, ergonomic handle."},
        {"name": "Retro Film Camera", "category": "Photography", "desc": "35mm film camera with vintage lens and manual controls."}
    ]
    print("Loading Retrieval Engine...")
    df = pd.DataFrame(data)

# 2. VECTOR DATABASE SETUP (The "Memory")
encoder = SentenceTransformer('all-MiniLM-L6-v2')
vectors = encoder.encode(df['desc'].tolist())
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

def get_best_product(user_query):
    # 3. THE RETRIEVAL ENGINE (Semantic Search)
    query_vector = encoder.encode([user_query])
    D, I = index.search(query_vector, 1)
    product = df.iloc[I[0][0]]
    return product