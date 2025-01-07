from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma

# from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    # SemanticChunker,
    # AI21SemanticTextSplitter,
    RecursiveJsonSplitter,
    HTMLHeaderTextSplitter,
    # HTMLSectionSplitter,
    MarkdownHeaderTextSplitter,
    TokenTextSplitter
)
from langchain_experimental.text_splitter import SemanticChunker
# from langchain_experimental.text_splitter import AI21SemanticTextSplitter

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_community.document_loaders import BSHTMLLoader
# from langchain_community.document_loaders import UnstructuredHTMLLoader

# from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
# import settings

# import pinecone  # Use pinecone-client separately
# from langchain_pinecone import Pinecone as LangChainPinecone  # Updated import for LangChain's Pinecone

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

class SchoginiAICore:
    """
    Original AI core template.
    """

    def __init__(self): #, model_name="default"):
        import settings
        self.model_name = model_name

    def predict(self, input_data: str) -> str:
        return f"Prediction from {self.model_name} for: {input_data}"

    # api_key = settings.openai_api_key
    # pinecone_api_key = settings.pinecone_api_key
    # vector_store_type=settings.vector_store_type,  
    # chroma_persist_directory=settings.vector_store_dir,
    # pinecone_index_name=settings.pinecone_index_name
    # model_name = settings.model_name

import os
from dotenv import load_dotenv

# Existing imports
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter,
    HTMLHeaderTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# New CreateSettings class
class CreateSettings:
    """
    A utility class to create a default settings.py file if it is missing.
    """
    @staticmethod
    def create_settings_py():
        settings_content = """
import os
from dotenv import load_dotenv

# Load .env contents
load_dotenv(override=True)

# Retrieve necessary environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

model_name = "gpt-4o-mini"

pinecone_environment = "us-east-1"  # Default environment
pinecone_index_name = "schogini-pinecone-index"

vector_store_type = "chroma"  # 'faiss', 'chroma', or 'pinecone'
vector_store_dir = "chroma_store"  # none faiss_store chroma_store

# Supported similarity metrics: euclidean, max_inner_product, dotproduct, jaccard, cosine
pinecone_metric = "cosine"

# Supported text splitter strategies:
# 'RecursiveCharacterTextSplitter', 'TokenTextSplitter', 'SemanticChunker', etc.
text_splitter_strategy = "SemanticChunker"

chunk_size = 1000
chunk_overlap = 200

# ------------ NO EDITS BELOW ------------
# Further validations or configurations can be added here.
"""
        with open("settings.py", "w") as file:
            file.write(settings_content)
        print("settings.py has been created.")

    @staticmethod
    def ensure_settings():
        try:
            import settings
            print("settings module imported successfully.")
        except ModuleNotFoundError:
            print("settings.py not found. Creating it now...")
            CreateSettings.create_settings_py()
            print("Re-run your script to apply the newly created settings.")


class SchoginiAIRAG:
    """
    A retrieval-augmented generation (RAG) class using LangChain components.

    Supports FAISS, ChromaDB, and Pinecone as vector store backends.

    Steps:
      1. Split text into chunks (recursive).
      2. Embed chunks with OpenAI Embeddings.
      3. Store chunks in the selected vector store (FAISS, ChromaDB, or Pinecone).
      4. Query with a RetrievalQA chain using ChatOpenAI.
    """

    def __init__(
        self,
        # openai_api_key: str,
        # pinecone_api_key: str = None,  # Required if using Pinecone
        # model_name: str = "gpt-3.5-turbo",
        # vector_store_type: str = "faiss",  # Options: 'faiss', 'chroma', 'pinecone'
        # chroma_persist_directory: str = "chroma_store",  # Required if using ChromaDB
        # pinecone_index_name: str = "schogini-pinecone-index",  # Required if using Pinecone
    ):
        import settings
        self.api_key = settings.openai_api_key
        self.pinecone_api_key = settings.pinecone_api_key
        self.model_name = settings.model_name
        self.vector_store_type = settings.vector_store_type
        self.chroma_persist_directory = settings.vector_store_dir #chroma_persist_directory
        self.pinecone_index_name = settings.pinecone_index_name
        self._retriever = None
        self._vector_store = None

    def load_html_documents(self, url):
        """
        Loads and processes an HTML file using LangChain's UnstructuredHTMLLoader.
        """
        import settings

        print(f"Loading HTML from {url}")
        # loader = UnstructuredHTMLLoader(file_path=url)
        # loader = BSHTMLLoader(url)
        loader = UnstructuredURLLoader(urls=url)
        documents = loader.load()
        print(f"Loaded HTML from {url}")
        # Mapping of strategy names to splitter classes
        splitter_mapping = {
            "RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter,
            "SemanticChunker": SemanticChunker,
            # "AI21SemanticTextSplitter": AI21SemanticTextSplitter,
            "RecursiveJsonSplitter": RecursiveJsonSplitter,
            "HTMLHeaderTextSplitter": HTMLHeaderTextSplitter,
            # "HTMLSectionSplitter": HTMLSectionSplitter,
            "MarkdownHeaderTextSplitter": MarkdownHeaderTextSplitter,
            "TokenTextSplitter": TokenTextSplitter
        }
        # Retrieve the text splitter strategy from environment variables
        # text_splitter_strategy = os.getenv("TEXT_SPLITTER_STRATEGY", "HTMLHeaderTextSplitter")
        splitter_class = splitter_mapping.get(settings.text_splitter_strategy)
        # splitter_class = splitter_mapping.get(text_splitter_strategy)
        if not splitter_class:
            raise ValueError(f"Unsupported TEXT_SPLITTER_STRATEGY '{text_splitter_strategy}'. Choose from {list(splitter_mapping.keys())}.")

        print(f"Using Text Splitter Strategy: {settings.text_splitter_strategy}")

        if settings.text_splitter_strategy == "SemanticChunker":
            # Instantiate the splitter with default parameters or customize as needed
            splitter = splitter_class(
                # chunk_size=settings.chunk_size,
                # chunk_overlap=settings.chunk_overlap,
                #separators=["\n\n", "\n", " ", ""]
                embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
            )
        else:
            # Instantiate the splitter with default parameters or customize as needed
            splitter = splitter_class(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                #separators=["\n\n", "\n", " ", ""]
            )


        # splitter = splitter_class(chunk_size=1000, chunk_overlap=200)

        split_docs = splitter.split_documents(documents)
        return split_docs

    def build_vector_store_from_html(self, url):
        """
        Builds a vector store from an HTML file.
        """
        docs = self.load_html_documents(url)
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

        print("Creating vector store...")
        if self.vector_store_type == "faiss":
            self.vector_store = FAISS.from_documents(docs, embeddings)
            print("FAISS vector store created.")
        elif self.vector_store_type == "chroma":
            self.vector_store = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=self.chroma_persist_directory
            )
            print(f"ChromaDB vector store created at {self.chroma_persist_directory}.")
        elif self.vector_store_type == "pinecone":
            pc = Pinecone(api_key=self.pinecone_api_key)
            selected_metric = settings.pinecone_metric
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
            if self.pinecone_index_name not in existing_indexes:
                pc.create_index(
                    name=self.pinecone_index_name,
                    dimension=1536,
                    metric=selected_metric,
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                print(f"Pinecone index '{self.pinecone_index_name}' created.")
            index = pc.Index(self.pinecone_index_name)
            self.vector_store = PineconeVectorStore.from_documents(
                docs, embedding=embeddings, index_name=self.pinecone_index_name
            )
            print(f"Pinecone vector store created and indexed in '{self.pinecone_index_name}'.")
            # vector_store = PineconeVectorStore.from_documents(docs, embedding=embeddings, index_name=self.pinecone_index_name)
            print(f"Pinecone vector store created and indexed in '{self.pinecone_index_name}'.")

        print("Vector store creation complete.")
        # self.vector_store = vector_store
        # return vector_store

    def load_pdf_documents(self, pdf_file_path):
        """
        Loads and processes a PDF file using LangChain's PyPDFLoader.
        """
        print(f"Loading PDF from {pdf_file_path}")
        loader = PyPDFLoader(pdf_file_path)
        documents = loader.load()
        # print("LOADER DONE")

        # Mapping of strategy names to splitter classes
        splitter_mapping = {
            "RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter,
            "SemanticChunker": SemanticChunker,
            # "AI21SemanticTextSplitter": AI21SemanticTextSplitter,
            "RecursiveJsonSplitter": RecursiveJsonSplitter,
            "HTMLHeaderTextSplitter": HTMLHeaderTextSplitter,
            # "HTMLSectionSplitter": HTMLSectionSplitter,
            "MarkdownHeaderTextSplitter": MarkdownHeaderTextSplitter,
            "TokenTextSplitter": TokenTextSplitter
        }
        # Get the splitter class based on the strategy
        splitter_class = splitter_mapping.get(settings.text_splitter_strategy)
        if not splitter_class:
            raise ValueError(f"Unsupported TEXT_SPLITTER_STRATEGY '{settings.text_splitter_strategy}'. "
                             f"Choose from {list(splitter_mapping.keys())}.")

        print(f"Using Text Splitter Strategy: {settings.text_splitter_strategy}")


        if settings.text_splitter_strategy == "SemanticChunker":
            # Instantiate the splitter with default parameters or customize as needed
            splitter = splitter_class(
                # chunk_size=settings.chunk_size,
                # chunk_overlap=settings.chunk_overlap,
                #separators=["\n\n", "\n", " ", ""]
                embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
            )
        else:
            # Instantiate the splitter with default parameters or customize as needed
            splitter = splitter_class(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                #separators=["\n\n", "\n", " ", ""]
            )

        # splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=settings.chunk_size,
        #     chunk_overlap=settings.chunk_overlap,
        #     separators=["\n\n", "\n", " ", ""]
        # )
        print("ABOUT TO SPLIT")
        # split_docs = [Document(page_content=chunk) for chunk in splitter.split_documents(documents)]
        split_docs = splitter.split_documents(documents)
        return split_docs

    def build_vector_store_from_pdf(self, pdf_file_path):
        """
        Builds a vector store from a PDF file.
        """
        docs = self.load_pdf_documents(pdf_file_path)
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

        # print("DOCS AND EMBEDDINGS DONE")
        if self.vector_store_type == "faiss":
            self.vector_store = FAISS.from_documents(docs, embeddings)
            print("FAISS vector store created.")
        elif self.vector_store_type == "chroma":
            self.vector_store = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=self.chroma_persist_directory
            )
            print(f"ChromaDB vector store created at {self.chroma_persist_directory}.")
        elif self.vector_store_type == "pinecone":
            pc = Pinecone(api_key=self.pinecone_api_key)
            selected_metric = settings.pinecone_metric
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
            if self.pinecone_index_name not in existing_indexes:
                pc.create_index(
                    name=self.pinecone_index_name,
                    dimension=1536,
                    metric=selected_metric,
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                print(f"Pinecone index '{self.pinecone_index_name}' created.")
            index = pc.Index(self.pinecone_index_name)
            self.vector_store = PineconeVectorStore.from_documents(
                docs, embedding=embeddings, index_name=self.pinecone_index_name
            )
            print(f"Pinecone vector store created and indexed in '{self.pinecone_index_name}'.")

        # print("VECTORESTOE DONE")

    def build_vector_store(self, text_data: str):
        """
        Splits text_data, embeds chunks, and builds the selected vector store.
        """
        import settings

        # Mapping of strategy names to splitter classes
        splitter_mapping = {
            "RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter,
            "SemanticChunker": SemanticChunker,
            # "AI21SemanticTextSplitter": AI21SemanticTextSplitter,
            "RecursiveJsonSplitter": RecursiveJsonSplitter,
            "HTMLHeaderTextSplitter": HTMLHeaderTextSplitter,
            # "HTMLSectionSplitter": HTMLSectionSplitter,
            "MarkdownHeaderTextSplitter": MarkdownHeaderTextSplitter
        }
        # Get the splitter class based on the strategy
        splitter_class = splitter_mapping.get(settings.text_splitter_strategy)
        if not splitter_class:
            raise ValueError(f"Unsupported TEXT_SPLITTER_STRATEGY '{settings.text_splitter_strategy}'. "
                             f"Choose from {list(splitter_mapping.keys())}.")

        print(f"Using Text Splitter Strategy: {settings.text_splitter_strategy}")

        # Instantiate the splitter with default parameters or customize as needed
        # splitter = splitter_class(
        #     chunk_size=settings.chunk_size,
        #     chunk_overlap=settings.chunk_overlap
        # )

        if settings.text_splitter_strategy == "SemanticChunker":
            # Instantiate the splitter with default parameters or customize as needed
            splitter = splitter_class(
                # chunk_size=settings.chunk_size,
                # chunk_overlap=settings.chunk_overlap,
                #separators=["\n\n", "\n", " ", ""]
                embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
            )
        else:
            # Instantiate the splitter with default parameters or customize as needed
            splitter = splitter_class(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                #separators=["\n\n", "\n", " ", ""]
            )

        # Split text into Document chunks
        docs = [Document(page_content=chunk) for chunk in splitter.split_text(text_data)]

        # Embed with OpenAI
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

        if self.vector_store_type == "faiss":
            # Create a FAISS vector store
            self.vector_store = FAISS.from_documents(docs, embeddings)
            print("FAISS vector store created.")
        elif self.vector_store_type == "chroma":
            # Create a ChromaDB vector store
            self.vector_store = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=self.chroma_persist_directory
            )
            print(f"ChromaDB vector store created at {self.chroma_persist_directory}.")
        elif self.vector_store_type == "pinecone":
            if not self.pinecone_api_key:
                raise ValueError("Pinecone API key is missing.")

            # Initialize Pinecone
            print("Initialize Pinecone")
            pc = Pinecone(api_key=self.pinecone_api_key)

            selected_metric = settings.pinecone_metric #os.getenv("PINECONE_METRIC", "euclidean") #.upper()

            # Create or connect to an existing Pinecone index
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
            if self.pinecone_index_name not in existing_indexes:
                pc.create_index(
                    name=self.pinecone_index_name,
                    dimension=1536,  # Fixed dimension for text-embedding-ada-002
                    metric= selected_metric, # "euclidean",  # Change to "cosine" if needed
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
                print(f"Pinecone index '{self.pinecone_index_name}' created.")
                while not pc.describe_index(self.index_name).status["ready"]:
                    time.sleep(1)
            else:
                print(f"Pinecone index '{self.pinecone_index_name}' already exists.")

            # Connect to the index
            index = pc.Index(self.pinecone_index_name)

            # from langchain_openai import OpenAIEmbeddings
            # embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

            # self.vector_store = PineconeVectorStore(index=index, embedding=embeddings)
            # self.vector_store = PineconeVectorStore.from_documents(docs, embedding=embeddings, index=index)
            self.vector_store = PineconeVectorStore.from_documents(docs, embedding=embeddings, index_name=self.pinecone_index_name)
            print(f"Pinecone vector store created and indexed in '{self.pinecone_index_name}'.")

        # results = vector_store.similarity_search(
        #     "LangChain provides abstractions to make working with LLMs easy",
        #     k=2,
        #     filter={"source": "tweet"},
        # )
        # for res in results:
        #     print(f"* {res.page_content} [{res.metadata}]")

        # Create a retriever for downstream queries
        # print("RETRIEVER1")
        self._retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        # print("RETRIEVER2")

    def save_vector_store(self): #, directory: str = None):
        """
        Saves the vector store to the specified directory.
        For FAISS, it saves using the save_local method.
        For ChromaDB, data is persisted automatically if persist_directory was set.
        For Pinecone, data is managed by Pinecone's managed index.
        """
        import settings

        directory = settings.vector_store_dir

        if self.vector_store_type != "pinecone" and self.vector_store is None:
            raise ValueError("Vector store is not built. Call build_vector_store() first.")

        if self.vector_store_type == "faiss":
            if directory is None:
                raise ValueError("Please specify a directory to save the FAISS vector store.")
            self.vector_store.save_local(directory)
            print(f"FAISS vector store saved to {directory}")
        elif self.vector_store_type == "chroma":
            # ChromaDB persists automatically, but you can manually persist if needed
            print(f"ChromaDB vector store persisted at {self.chroma_persist_directory}")
        elif self.vector_store_type == "pinecone":
            # Pinecone manages persistence automatically via its managed index
            print(f"Pinecone vector store persisted in Pinecone index '{self.pinecone_index_name}'.")
            # print("SAVE1")

    def load_vector_store(self): #, directory: str = None):
        """
        Loads the vector store from the specified directory.
        For FAISS, it loads using the load_local method.
        For ChromaDB, it loads from the persist_directory.
        For Pinecone, it connects to the existing Pinecone index.
        """

        import settings

        directory = settings.vector_store_dir
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

        if self.vector_store_type == "faiss":
            if directory is None:
                raise ValueError("Please specify the directory from which to load the FAISS vector store.")
            self._vector_store = FAISS.load_local(
                directory,
                embeddings,
                allow_dangerous_deserialization=True  # Enable deserialization
            )
            print(f"FAISS vector store loaded from {directory}")
        elif self.vector_store_type == "chroma":
            if not os.path.exists(self.chroma_persist_directory):
                raise ValueError(f"ChromaDB persist directory '{self.chroma_persist_directory}' does not exist.")
            self._vector_store = Chroma(
                persist_directory=self.chroma_persist_directory,
                embedding_function=embeddings
            )
            print(f"ChromaDB vector store loaded from {self.chroma_persist_directory}")
        elif self.vector_store_type == "pinecone":
            if not self.pinecone_api_key:
                raise ValueError("Pinecone API key is missing.")

            # Initialize Pinecone
            # pinecone.init(api_key=self.pinecone_api_key, environment="us-east-1")  # Replace with your Pinecone environment
            pc = Pinecone(api_key=self.pinecone_api_key)

            # Connect to the existing Pinecone index
            # existing_indexes = pc.list_indexes()
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

            # print(f"202 pinecone_index_name {self.pinecone_index_name}")
            # print(f"202 existing_indexes {existing_indexes}")

            if self.pinecone_index_name not in existing_indexes:
                # print(f"206 self.pinecone_index_name {self.pinecone_index_name}")
                raise ValueError(f"Pinecone index '{self.pinecone_index_name}' does not exist.")

            index = pc.Index(self.pinecone_index_name)

            # Create Pinecone vector store using LangChain's Pinecone from_existing_index
            # self._vector_store = LangChainPinecone.from_existing_index(index, embeddings)
            # print(f"214")
            self._vector_store = PineconeVectorStore(index=index, embedding=embeddings)
            # self._vectorstore  = PineconeVectorStore(index_name=self.pinecone_index_name, embedding=embeddings)

            print(f"Pinecone vector store loaded from Pinecone index '{self.pinecone_index_name}'.")

        # print(f"219 SELF.RETRIEVER LOADED")
        self._retriever = self._vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        # self._retriever = self._vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})


    def ask_question(self, query: str) -> str:
        """
        Uses a RetrievalQA chain to answer questions with RAG.
        """
        if not self._retriever:
            raise ValueError("Vector store not loaded. Call load_vector_store() first.")

        llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=self.api_key
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self._retriever
        )

        # Replace deprecated `run` with `invoke`
        result = qa_chain.invoke(query)
        return result


