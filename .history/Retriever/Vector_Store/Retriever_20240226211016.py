'''
This class Retriever is used to store and load chunks with embeddings and metadata
It also integrates with the retrieval functionality to enable the match between queries and chunk embeddings

'''

from langchain_community.document_loaders import PyPDFLoader
import uuid
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
    def createCollection(self, collection_name: str):
        collection = self.client.create_collection(name=collection_name)
        return collection


    # return the created collection withe name collection_name
    def getCollection (self, collection_name: str):
        collection = self.client.get_collection(name=collection_name)
        return collection

    # Please make sure that embeddings_list and metadata_list is matched with documents_list
    # example of one metadata: {"chapter": "3", "verse": "16"}
    # id will be created automatically as uuid v4 
    def addDocuments (self, collection_name: str, embeddings_list: list[list[float]], documents_list: list[dict], metadata_list: list[dict]) :
        collection = self.getCollection(collection_name)

        collection.add(
            documents=documents_list,
            metadatas=metadata_list,
            embeddings= embeddings_list,
            ids=[str(uuid.uuid4()) for i in range(len(documents_list)) ]
        )



