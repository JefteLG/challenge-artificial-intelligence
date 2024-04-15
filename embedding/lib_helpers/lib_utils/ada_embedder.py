import os
from langchain_community.embeddings import AzureOpenAIEmbeddings


class AdaEmbedder:
    def __init__(self) -> None:
        self._embedder = AzureOpenAIEmbeddings(
                model=os.environ.get('MODEL_NAME_OPENAI_EMBEDDINGS'),
                azure_deployment=os.environ.get('DEPLOYMENT_NAME_EMBEDDINGS'),
                openai_api_key=os.environ.get('API_KEY_OPENAI'),
                openai_api_base=os.environ.get('API_BASE_OPENAI'),
                openai_api_type=os.environ.get('API_TYPE_OPENAI')
            )
    
    @property
    def embedder(self):
        return self._embedder
    
    