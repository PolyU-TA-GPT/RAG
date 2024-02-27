'''
This class Retriever is used to store and load chunks with embeddings and metadata
It also integrates with the retrieval functionality to enable the match between queries and chunk embeddings

'''

from langchain_community.document_loaders import PyPDFLoader
import uuid
import os
import json
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import chromadb

class Retriever:
    client = None
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    chromadb_path = "{}/chromadb".format(cur_dir)

    def __init__ (self):
        '''
        initialize the persistent client based on chromadb_path \n
        heartbeat() return value will be printed out to test connection
        '''
        client = chromadb.PersistentClient(path=self.chromadb_path)
        print(client.heartbeat())
    
   

    def createCollection(self, collection_name: str):
        """
        Please create a collection for each independent ''topic'' (e.g., summer exchange information of PolyU)\n
        The Collection will be created with collection_name, the name must follow the rules:
        1. The length of the name must be between 3 and 63 characters.\n
        2. The name must start and end with a lowercase letter or a digit, and it can contain dots, dashes, and underscores in between.\n
        3. The name must not contain two consecutive dots.\n
        4. The name must not be a valid IP address.\n
        """
        collection = self.client.create_collection(name=collection_name)
        return collection



    def getCollection (self, collection_name: str):
        """
        return the created collection withe name collection_name\n
        The exception will be raised if no collection with specified collection_name has been created
        """
        collection = self.client.get_collection(name=collection_name)
        return collection
    
    def addDocuments (self, collection_name: str, embeddings_list: list[list[float]], documents_list: list[dict], metadata_list: list[dict]) :
        """
        Please make sure that embeddings_list and metadata_list is matched with documents_list\n
        Example of one metadata: {"chapter": "3", "verse": "16"}\n
        The id will be created automatically as uuid v4 
        The chunks content and metadata will be logged (appended) into ./assets/<collection_name>.json
        """
        collection = self.getCollection(collection_name)
        num = len(documents_list)
        ids=[str(uuid.uuid4()) for i in range(num) ]

        collection.add(
            documents= documents_list,
            metadatas= metadata_list,
            embeddings= embeddings_list,
            ids=ids 
        )

        with open ("{:0}/assets/{:1}.json".format(self.cur_dir, collection_name), "a") as chunklog:
            json.dump([{"chunk_id": ids[i], "metadata:": metadata_list[i], "page_content": documents_list[i]} \
                       for i in range(num)], chunklog, indent=4)
            
        
        


    
    def query (self, collection_name: str, query_embeddings: list[list[float]]):
        """return n (by now, set as top-3) closest results (chunks and metadatas) in order """
        collection = self.getCollection(collection_name)
        result = collection.query(
            query_embeddings=query_embeddings,
            n_results=10,
        )
        return result


    def update (self, collection_name: str, id_list: list[str], embeddings_list: list[list[float]], documents_list: list[dict], metadata_list: list[dict]):
        collection = self.getCollection(collection_name)
        collection.update(
            ids=id_list,
            embeddings=embeddings_list,
            metadatas=metadata_list,
            documents=documents_list,
        )


    def delete(self, collection_name: str, id_list: list[str]):
        """delete the collection by list of ids
        ### can NOT be undone"""
        collection = self.getCollection(collection_name)
        collection.delete(
            ids=id_list,
        )

    def test():
        """This function is just used for testing Retriever class, please don't use it outside this file"""
