from langchain_community.embeddings import AzureOpenAIEmbeddings
import os


class AdaEmbedder:
    def __init__(self) -> None:
        self._embedder = AzureOpenAIEmbeddings(
                azure_deployment=os.environ.get('DEPLOYMENT_NAME_EMBEDDINGS'),
                openai_api_key=os.environ.get('API_KEY_OPENAI'),
                openai_api_base=os.environ.get('API_BASE_OPENAI'),
                openai_api_type=os.environ.get('API_TYPE_OPENAI')
            )

    @property
    def embedder(self):
        return self._embedder
    
    