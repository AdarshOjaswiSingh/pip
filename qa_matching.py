import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functools import lru_cache

# Load the dataset from the Excel file
# Replace 'dataset.xlsx' with the actual file name and path if it's different
df = pd.read_excel('End-to-End-AI-driven-pipeline-with-real-time-interview-insights-main/compliance-checker/src/dataset')

# Check if the necessary columns ('question' and 'answer') exist in the dataset
if 'question' not in df.columns or 'answer' not in df.columns:
    raise ValueError("Dataset must contain 'question' and 'answer' columns")

# Precompute the TF-IDF vectors for the questions
vectorizer = TfidfVectorizer().fit(df['question'])

# Caching the similarity results to avoid redundant computation
@lru_cache(maxsize=1000)  # Cache up to 1000 unique queries
def get_answer(user_query):
    # Clean the user query (assuming it's in lowercase and without special characters)
    user_query_cleaned = user_query.lower().replace(r'\W', ' ')

    # Vectorize the user query
    query_vec = vectorizer.transform([user_query_cleaned])

    # Compute cosine similarities
    similarities = cosine_similarity(query_vec, vectorizer.transform(df['question']))

    # Find the index of the best matching question
    best_match_idx = np.argmax(similarities)

    # Return the corresponding answer
    return df['answer'].iloc[best_match_idx]

# Test the function
user_query = "What can I do when I'm feeling anxious?"
answer = get_answer(user_query)
print("Answer:", answer)
