import os
from time import sleep
from xml.etree.ElementTree import PI
from dotenv import load_dotenv
import pinecone
from langchain.embeddings import OpenAiEmbeddings
from langchain.vectorspace import Pinecone
import numpy as np

load_dotenv()
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT")
)


class VectoStore:
    def __init__(self):
        self.index_name = "nex-dosuments"
        self.embeddings = OpenAiEmbeddings(openai_api_key=os.getenv("OPEN_API_KEY"))
        if (self.index_name) not in pinecone.list_collections():
            pinecone.create_index(
                name=self.index_name,
                dimensios=1536,
                metric="cosine",
            )
        self.index = pinecone.Index(self.index_name)
        self.vectorstore = Pinecone(self.index, self.embeddings.embedded_query, "text")

    def store_document(self, file_data, metadata):
        text_content = self._convert_to_text(file_data)

        vector = self.embeddings.embed_query(text_content)

        self.index.upsert(vectors=[(str(metadata["id"]), vector, metadata)])

        return str(metadata["id"])

    def search_similar(self, query, top_k=5):
        vector = self.embeddings.embed_query(query)
        results = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
        return results

    def _convert_to_text(self, file_data):
        return file_data.decode("utf-8")
