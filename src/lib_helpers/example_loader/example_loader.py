import random
import pandas as pd
from tabulate import tabulate

try:
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from lib_helpers.example_loader.strategies.neirest_neighbour_strategy import NearestNeighborsStrategy

except ModuleNotFoundError:
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from src.lib_helpers.example_loader.strategies.neirest_neighbour_strategy import NearestNeighborsStrategy

class ExampleLoader:
    def __init__(self, embedder: AdaEmbedder) -> None:
        self.embedder = embedder
        self.strategy = NearestNeighborsStrategy(self.embedder)
    
    def _get_doc_embeddings(self, docs: list[str]) -> list[list[float]]: 
        return self.embedder.embedder.embed_documents(docs)

    def _get_query_embeddings(self, query: str) -> list[float]:
        return self.embedder.embedder.embed_query(query)
 
    @staticmethod
    def _df_to_markdown(df: pd.DataFrame, new_columns: dict = None, rename_columns: dict = None, select_columns: list[str] = None) -> str:
        if df is None:
            raise ValueError("Dataframe should not be None")
        if df.empty:
            raise ValueError("Dataframe should not be empty")
        if new_columns:
            for col_name, col_value in new_columns.items():
                df[col_name] = col_value
        if rename_columns:
            df = df.rename(columns=rename_columns)
        if select_columns:
            df = df[select_columns]
        return tabulate(df, headers='keys', tablefmt='pipe', showindex=True)
    
    @staticmethod
    def _df_to_text(df: pd.DataFrame, desired_column: str) -> str:
        if df is None:
            raise ValueError("Dataframe should not be None")
        if df.empty:
            raise ValueError("Dataframe should not be empty")
        # Check if the desired column is in the DataFrame
        if desired_column not in df.columns:
            raise ValueError(f"Column '{desired_column}' not found in DataFrame")

        # Convert the desired column to a string, with each element separated by '\n'
        return '\n'.join(df[desired_column].astype(str))

    def sort_examples(self, examples: list[str], target: str, k: int = 10, kwargs: dict = {}) -> pd.DataFrame:
        examples_embeddings = self._get_doc_embeddings(examples)
        target_embeddings = self._get_query_embeddings(target)
        sorted_df = self.strategy.sort_str(examples_embeddings, target_embeddings, k, embed_ready=True, options_labels=examples)
        if sorted_df.empty and kwargs.get('assign_random_on_missmatch'):
            # Choose up to k random examples
            random_examples = random.sample(examples, min(k, len(examples)))
            # Create a new DataFrame with these examples
            sorted_df = pd.DataFrame(random_examples, columns=['doc'])
        return sorted_df
    
    def relevant_examples_as_text(self, examples: list[str], target: str, k: int = 10, kwargs: dict = {}) -> str:
        sorted_df = self.sort_examples(examples, target, k, kwargs)
        return self._df_to_text(sorted_df, desired_column='doc')

    def relevant_examples_as_md(self, examples: list[str], target: str, k: int = 10, kwargs: dict = {}) -> str:
        sorted_df = self.sort_examples(examples, target, k, kwargs)
        return self._df_to_markdown(sorted_df, kwargs.get('new_columns'), kwargs.get('rename_columns'), kwargs.get('select_columns'))