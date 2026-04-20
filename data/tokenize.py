# tokenize.py
# RAG chunking + embedding using Voyage AI (class-based)

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import voyageai


class RAGTOKENGENERATOR:
    def __init__(self, chunk_size=500, chunk_overlap=100, model="voyage-2"):
        # Store config
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = model

        # Text splitter for smart chunking
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        # Voyage client setup
        self.client = voyageai.Client(
            api_key=os.getenv("VOYAGE_API_KEY")
        )

    def split_text(self, text):
        # Break text into chunks
        return self.splitter.split_text(text)

    def embed_chunks(self, chunks):
        # Generate embeddings
        response = self.client.embed(
            texts=chunks,
            model=self.model
        )
        return response.embeddings

    def process_document(self, text):
        # Full pipeline: split → embed → combine
        chunks = self.split_text(text)
        embeddings = self.embed_chunks(chunks)

        return [
            {"text": chunk, "embedding": emb}
            for chunk, emb in zip(chunks, embeddings)
        ]

    def process_documents(self, text_list):
        # Handle multiple documents
        all_docs = []

        for text in text_list:
            all_docs.extend(self.process_document(text))

        return all_docs
