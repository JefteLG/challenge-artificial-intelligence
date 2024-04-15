from model_embedding.data_extraction_management import DataExtractionManagement
import os

def embedding_management(diretorio_raiz):
    data_extraction = DataExtractionManagement(index_name="mais-educacao")
    for root_folder, subfolders, files in os.walk(diretorio_raiz+"/files"):
        for nome_arquivo in files:
            if nome_arquivo.endswith('.json'):
                data_extraction.json_extract(diretorio_raiz, root_folder, nome_arquivo)

            elif nome_arquivo.endswith('.txt'):
                data_extraction.text_extract(diretorio_raiz, root_folder, nome_arquivo)

            elif nome_arquivo.endswith('.pdf'):
                data_extraction.pdf_extract(diretorio_raiz, root_folder, nome_arquivo)

            elif nome_arquivo.endswith('.mp4'):
                data_extraction.movie_extract(diretorio_raiz, root_folder, nome_arquivo)

            elif nome_arquivo.endswith('.jpg'):
                data_extraction.image_extract(diretorio_raiz, root_folder, nome_arquivo)

            else:
                print("ERROR!!")

if __name__ == "__main__":
    embedding_management("embedding/resources")








