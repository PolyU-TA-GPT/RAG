'''
This class Retriever is used to store and load chunks with embeddings and metadata
It also integrates with the retrieval functionality to enable the match between queries and chunk embeddings

'''

from langchain_community.document_loaders import PyPDFLoader

import os

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import chromadb

class Retriever:
    client = None
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    chromadb_path = "{}/chromadb".format(cur_dir)

    def __init__ (self):
        client = chromadb.PersistentClient(path="/path/to/save/to")
        print(client.heartbeat())
    
    '''
    The Collection will be created with collection_name, the name must follow the rules:
    # The length of the name must be between 3 and 63 characters.
    # The name must start and end with a lowercase letter or a digit, and it can contain dots, dashes, and underscores in between.
    # The name must not contain two consecutive dots.
    # The name must not be a valid IP address.
    ''' 
    def createCollection(self, collection_name):
        collection = self.client.create_collection(name=collection_name)
        return collection


    # return the created collection withe name collection_name
    def getCollection (self, collection_name):
        collection = self.client.get_collection(name=collection_name)
        return collection

    def addDocuments (self, collection_name,  ) :
        collection = self.getModule()
        collection.add(
            documents=["lorem ipsum...", "doc2", "doc3", ...],
            metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
            ids=["id1", "id2", "id3", ...]
        )
