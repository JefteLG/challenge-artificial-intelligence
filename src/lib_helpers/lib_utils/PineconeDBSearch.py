import os
from pinecone import Pinecone


class PineconeDBSearch:
    def pineconedbsearch(self, index_name):
        _pineconedbsearch = Pinecone(api_key=os.environ.get('API_KEY_PINECONE'))
        index_pinecone = _pineconedbsearch.Index(index_name)
        return index_pinecone
