# Import the main classes/functions from each module to make them accessible directly from the package
from .document_loader import DocumentLoader
from .retriever import Retriever
from .vector_store import VectorStore

# Optionally, you can define what should be imported when someone uses `from knowledge_base import *`
__all__ = ['DocumentLoader', 'Retriever', 'VectorStore']