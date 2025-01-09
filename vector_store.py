from sklearn.neighbors import NearestNeighbors
import numpy as np 

class SklearnVectorStore:
    """Drop-in replacement for FAISS, using scikit-learn"""
    def __init__(self, documents, embedding_function):
        self.documents = documents
        self.embedding = embedding_function

        # Create embeddings
        self.vectors = []
        for doc in documents: 
            vector = embedding_function.embed_query(doc.page_content)
            self.vectors.append(vector)
        
        self.vectors = np.array(self.vectors)

        self.index = NearestNeighbors(
            n_neighbors=4,
            metric='cosine',
            n_jobs=-1 # Use all CPU cores
        )
        self.index.fit(self.vectors)
    
    @classmethod
    def from_documents(cls, documents, embedding):
        return cls(documents, embedding)

    def similarity_search(self, query, k=4):
        query_vector = self.embedding.embed_query(query)
        query_vector = np.array([query_vector]) # Reshape for scikit-learn

        distances, indices = self.index.kneighbors(query_vector, n_neighbors=k)

        # Return documents in order of similarity
        return [self.documents[i] for i in indices[0]]