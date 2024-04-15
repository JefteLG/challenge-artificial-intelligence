import re
from unidecode import unidecode
import time
import json
import os
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
# from langchain_community.document_loaders import PyPDFLoader
from model_embedding.templates_ import DataExtractionTemplate, DataExtractionJsonTemplate
from lib_helpers.llm.llm import LLM
from lib_helpers.lib_utils.pinecone_db import PineconeDB
from lib_helpers.lib_utils.ada_embedder import AdaEmbedder


class DataExtractionManagement():
    def __init__(self, index_name):
        self.llm = LLM()
        self.embed = AdaEmbedder().embedder
        self.db_pinecone = PineconeDB(index_name).pineconedb
        self.output_schema = {
            "type": "object",
            "properties": {
                "response": {"type": "string"}
            },
            "required": ["response"],
            "additionalProperties": False
        }

    
    def create_file_txt(self, root_directory, root_path, file_name, text, type_file):
        parts = root_path.split('/')
        last_name = parts[-1]

        # Remover extensão do nome
        file_name_without_extension = re.sub(r'\.[^.]*$', '', file_name)
        # Remover caracteres especiais e acentos
        cleaned_file_name = unidecode(re.sub(r'[^\w\s]', '', file_name_without_extension))
        # Remover espaços em branco
        cleaned_file_name = re.sub(r'\s+', '', cleaned_file_name)

        path_extractions = root_directory + f"/extractions/{last_name}/{type_file}{cleaned_file_name.lower()}.txt"

        if not os.path.exists(root_directory + f"/extractions/{last_name}"):
            os.makedirs(root_directory + f"/extractions/{last_name}")
            print("Pasta criada com sucesso!")
        else:
            print("A pasta já existe.")

        list_texts = []

        for metadata in text:
            list_texts.append(metadata["metadata"]['text'])

        with open(path_extractions, "w") as file:
            for elemento in list_texts:
                file.write(elemento + "\n\n")

        print("Arquivo texto.txt criado com sucesso!")
    
    
    def create_embeddings(self, list_text, path, file_path):
        # Vetoriza os textos
        # cria um objeto com o vetor e os metadados
        # Define a function to create embeddings
        vectors = []
        # query_result_documents = self.embed.embed_documents(list_text)
        for text in list_text:
            query_result = self.embed.embed_query(text)
            time.sleep(1)
            vectors.append(
                {
                    "id": str(int(time.time() * 1000)),                    
                    "values": query_result, 
                    "metadata": {
                        "path": path,
                        "file_path": file_path,
                        "text": text
                    }
                }
            )
        return vectors
    
    
    def process_text(self, root_path, file_name):
        loader = TextLoader(root_path + "/" + file_name)
        document = loader.load_and_split()

        text = document[0].page_content
        text = text.replace("\n", " ")
        return text


    def save_embeddings(self, embeddings):
        index = self.db_pinecone
        index.upsert(
            vectors=embeddings
        )
    

    def request_gpt(self,text, root_path, file_name, human_prompt_template, system_prompt_template):
        kwargs = {
            'context': text
        }

        response = self.llm.run(
            human_prompt_template,
            system_prompt_template,
            kwargs,
            self.output_schema
        )
        rsp = response['response']

        list_text = rsp.split("\n\n")

        embeddings = self.create_embeddings(
                list_text=list_text,
                path=root_path,
                file_path=root_path + "/" + file_name
            )
        
        return embeddings

    
    def pdf_extract(self, root_directory, root_path, file_name):
        # Logica para extrair os dados do arquivo PDF
        # Criar os vetor
        # Atualizar o index fazendo o upload do vetor para o index
        # Criar um arquivo .txt com os dados extraidos e salvar no diretório case_mais_educacao/embedding/resources/extractions

        loader = PyPDFLoader(root_path + "/" + file_name)
        document = loader.load_and_split()
        document_new = [doc.page_content.replace("\n", " ") for doc in document]
        new_text = []
        list_embeddings = []
        for doc_new in range(0, len(document_new) - 1):
            new_text.append(document_new[doc_new] + " " + document_new[doc_new + 1])

        for text in new_text:
            embeddings = self.request_gpt(
                text,
                root_path,
                file_name,
                DataExtractionTemplate.SYSTEM_PROMPT_TEMPLATE,
                DataExtractionTemplate.HUMAN_PROMPT_TEMPLATE
            )
            list_embeddings.extend(embeddings)

        self.save_embeddings(list_embeddings)
        self.create_file_txt(root_directory, root_path, file_name, list_embeddings, type_file="type_pdf-")
    
    
    def text_extract(self, root_directory, root_path, file_name):
        # Logica para extrair os dados do arquivo TXT.
        # Para garantir que o texto seja um texto curto é interessante coletar apenas as informações mais relevantes. Para isso podemos usar um LLM para extrair apenas as informações mais importante para sanar duvidas sobre o assunto referente ao texto.

        text = self.process_text(root_path, file_name)

        list_embeddings = []
        embeddings = self.request_gpt(
            text,
            root_path,
            file_name,
            DataExtractionTemplate.SYSTEM_PROMPT_TEMPLATE,
            DataExtractionTemplate.HUMAN_PROMPT_TEMPLATE
        )
        list_embeddings.extend(embeddings)

        self.save_embeddings(list_embeddings)
        self.create_file_txt(root_directory, root_path, file_name, list_embeddings, type_file="type_text-")
    

    def json_extract(self, root_directory, root_path, file_name):
        file_path = os.path.join(root_path, file_name)
        with open(file_path, 'r') as file:
            json_text = json.load(file)
        
        questoes = []
        for item in json_text.get("content"):
            questao = {
                "Questão": item["title"],
                "Pergunta": item["content"]["html"],
                "Resposta": next(([opcao["content"]["html"], opcao["feedback"]["html"]] for opcao in item["content"]["options"] if opcao["correct"]), None)
            }
            questoes.append(questao)

        formatted_data = ""
        for item in questoes:
            formatted_data += f"""Questão: {item['Questão']}. Pergunta: {item['Pergunta']}. Resposta: {item['Resposta'][0]}. Explicação: {item['Resposta'][1]}.\n\n"""

        list_embeddings = []
        embeddings = self.request_gpt(
            formatted_data,
            root_path,
            file_name,
            DataExtractionJsonTemplate.SYSTEM_PROMPT_TEMPLATE,
            DataExtractionJsonTemplate.HUMAN_PROMPT_TEMPLATE
        )
        list_embeddings.extend(embeddings)

        self.save_embeddings(list_embeddings)      
        self.create_file_txt(root_directory, root_path, file_name, list_embeddings, type_file="type_json-")
    

    def movie_extract(self, root_directory, root_path, file_name):
        # Logica para extrair os dados do arquivo MP4
        # usar um serviço de trancrever audios e videos para texto.
        # Nesse exemplo foi utilizado o serviço de trancrever audios e videos. da AWS https://aws.amazon.com/pt/transcribe/
        
        text = """Olá, Seja bem vindo a dica do professor da unidade de aprendizagem Criação de páginas web com h t ML cinco Neste vídeo, vamos falar sobre formatação de texto e âncoras em h T ML a especificação HTML cinco Disponibiliza uma série de elementos para formatar textos e criar âncoras em páginas web. Para isso você deve usar tags específicas que permitem formatar os elementos visando o equilíbrio do código com a semântica do h T ML cinco Nesta dica criamos uma página H T ML que apresenta uma relação de músicas de Roberto Carlos. Nesta página montamos um menu de navegação que contém links para algumas páginas do astro. O objetivo desses links é posicionar a página no início de cada música sem precisar percorrer todo o documento. Vejamos agora a estrutura dessa página. A instrução Doc type h T ML informa o navegador que estamos trabalhando com a versão cinco. Roberto Carlos é o nosso rei é o título da nossa página. Ele é exibido na barra de título do navegador. Músicas de Roberto Carlos é o título principal apresentado na nossa página. Esse destaque se dá através de h dois Nave é uma tag específica do H t ML cinco Ela define uma área da nossa página onde colocamos os principais links dela. Section define uma área da nossa página. Nós podemos ter várias sessões na nossa página Arco é uma área principal da nossa seção. É nela que vamos colocar as músicas de Roberto Carlos. Cada música de Roberto Carlos possui um título. Esse título é destacado com o H três, que informa uma letra um pouquinho menor que o título principal da nossa página que é o h dois. Para apresentar as musicas utilizamos a tag pre e define a formatação. Tal como está digitada na nossa pagina, ela respeita quebras de linha e linhas em branco. Ao final de cada musica colocamos um atalho para topo. Esse atalho irá direcionar a pagina para o início onde temos o mesmo indicador topo no titulo Musicas de Roberto Carlos Encerramos o fechamento da tag pré e em seguida iniciamos a próxima música e assim por diante até que todas as músicas estejam na nossa página. Voltando para a nossa pagina podemos ver como ella se comporta clicando no início de uma musica, percebemos que o navegador posiciona logo no início de no final de cada musica temos o atalho que volta para o início de podemos navegar entre as musicas e voltar para o início da pagina isso com cada uma delas. O link de cada música é feito com âncoras, ou seja, são endereços apontados para dentro da própria página. Nesse caso, como é grande, aponta para o início da música como é grande o meu amor por você. Nesse caso nós temos esse identificador como é grande com esse título que aponta para o início dessa música e assim encerramos a dica do professor, que tratou sobre formatação de texto e âncoras em h t ML Espero que você tenha aproveitado essa dica bons estudos."""

        list_embeddings = []
        embeddings = self.request_gpt(
            text,
            root_path,
            file_name,
            DataExtractionTemplate.SYSTEM_PROMPT_TEMPLATE,
            DataExtractionTemplate.HUMAN_PROMPT_TEMPLATE
        )
        list_embeddings.extend(embeddings)

        self.save_embeddings(list_embeddings)
        self.create_file_txt(root_directory, root_path, file_name, list_embeddings, type_file="type_movie-")
    

    def image_extract(self, root_directory, root_path, file_name):
        # Logica para extrair os dados do arquivo JPG
        # Usar um serviço para reconhecer os elementos na imagem e criar um texto.
        # GPT-4 multimodal e o Claude 3 Sonnet da Anthrop fornece ferramentas para reconhecer os elementos na imagem.
        # Nesse exemplo foi utilizado o GPT-4 para reconhecer os elementos na imagem.
        
        text = """A imagem é um diagrama que explica os elementos de um layout de página da web:

        - HEADER DA PÁGINA: Indica que o cabeçalho contém informações apresentadas no topo da página, como dados da organização e links gerais (página inicial, mapa do site, etc.).
        
        - NAV: Identifica uma área definida para os principais atalhos da página, provavelmente se referindo à barra de navegação que facilita o acesso a diferentes seções do site.

        - FOOTER DA PÁGINA: Aponta para o rodapé da página, onde são apresentadas informações como dados de contato da organização ou outras informações relevantes.

        As linhas conectam os termos aos respectivos elementos no exemplo de layout à direita, ilustrando onde cada um dos termos seria aplicado no contexto de um website real."""

        list_embeddings = []
        embeddings = self.request_gpt(
            text,
            root_path,
            file_name,
            DataExtractionTemplate.SYSTEM_PROMPT_TEMPLATE,
            DataExtractionTemplate.HUMAN_PROMPT_TEMPLATE
        )
        list_embeddings.extend(embeddings)

        self.save_embeddings(list_embeddings)
        self.create_file_txt(root_directory, root_path, file_name, list_embeddings, type_file="type_image-")
