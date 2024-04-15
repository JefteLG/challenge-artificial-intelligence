import pandas as pd
from typing import List, Union

try:
    from lib_helpers.lib_utils.memory_vector_store import MemoryVectorStore
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
except ModuleNotFoundError:
    from src.lib_helpers.lib_utils.memory_vector_store import MemoryVectorStore
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder

class NearestNeighborsStrategy():
    def __init__(self, embedder: AdaEmbedder):
        self.embedder = embedder
        self.vector_store = self.get_vector_store(self.embedder)
    
    def sort_str(
            self, 
            options: Union[List[str], List[List[float]]],
            target_option: Union[str, List[float]],
            k: int,
            embed_ready: bool = True,
            options_labels: list[str] = None
        ) -> pd.DataFrame:
        if embed_ready:
            self.vector_store.create_vector_store_w_embeddings(options_labels, options)
            results = self.vector_store.query_w_embeddings(target_option, k)
        else:
            self.vector_store.create_vector_store(options)
            results = self.vector_store.query(target_option, k)
        return results
    
    def get_vector_store(self, embedder: AdaEmbedder) -> MemoryVectorStore:
        return MemoryVectorStore(embedder)