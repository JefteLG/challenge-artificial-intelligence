import os
from pinecone import Pinecone


class PineconeDB:
    def __init__(self, index_name) -> None:        
        self._pineconedb = Pinecone(api_key=os.environ.get('API_KEY_PINECONE'))
        self.index_name = index_name

    @property
    def pineconedb(self):
        index_pinecone = self._pineconedb.Index(self.index_name)
        return index_pinecone