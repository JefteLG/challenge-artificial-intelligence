import numpy as np
import pandas as pd
from typing import List
from docarray.typing import NdArray
from docarray import BaseDoc, DocList
from docarray.index import InMemoryExactNNIndex

try:
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
except ModuleNotFoundError:
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder

class InMemoryDoc(BaseDoc):
    content: str 
    embedding: NdArray[1536]

class MemoryVectorStore:
    def __init__(self, embedder: AdaEmbedder) -> None:
        self.embedder = embedder.embedder

    def create_vector_store(self, docs: list[str]) -> None:
        doc_embeddings = self.embedder.embed_documents(docs)
        in_memory_docs = DocList[InMemoryDoc](InMemoryDoc(content=doc, embedding=np.array(doc_embeddings[i])) for i, doc in enumerate(docs))
        self.doc_index = InMemoryExactNNIndex[InMemoryDoc]()
        self.doc_index.index(in_memory_docs)
        
    def create_vector_store_w_embeddings(self, docs: list[str], doc_embeddings: List[List[float]]) -> None:
        in_memory_docs = DocList[InMemoryDoc](InMemoryDoc(content=doc, embedding=np.array(doc_embeddings[i])) for i, doc in enumerate(docs))
        self.doc_index = InMemoryExactNNIndex[InMemoryDoc]()
        self.doc_index.index(in_memory_docs)

    def query(self, query: str, k: int) -> pd.DataFrame:
        query_embeddings = np.array(self.embedder.embed_query(query))
        retrieved_docs, scores = self.doc_index.find(query_embeddings, search_field='embedding', limit=k)
        return pd.DataFrame({
            'doc':[doc.content for doc in retrieved_docs],
            'score':scores.tolist()
        })
    
    def query_w_embeddings(self, query_embeddings: List[float], k: int) -> pd.DataFrame:
        query_embeddings = np.array(query_embeddings)
        retrieved_docs, scores = self.doc_index.find(query_embeddings, search_field='embedding', limit=k)
        return pd.DataFrame({
            'doc':[doc.content for doc in retrieved_docs],
            'score':scores.tolist()
        })