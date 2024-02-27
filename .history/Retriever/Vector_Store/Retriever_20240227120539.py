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
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

##### TO BE REMOVED #####
import sys
sys.path.append('../..')
import torch
import time
from Generator.src.test import generate
from Embedding.sentenceEmbeddings import sentenceEmbeddings

###### TO BE REMOVED ######

class Retriever:
    client = None
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    chromadb_path = "{}/chromadb".format(cur_dir)

    def __init__ (self):
        '''
        initialize the persistent client based on chromadb_path \n
        heartbeat() return value will be printed out to test connection
        '''
        self.client = chromadb.PersistentClient(path=self.chromadb_path)
        print("client connection heartbeat code: ", self.client.heartbeat())
    
   

    def createCollection(self, collection_name: str):
        """
        Please create a collection for each independent ''topic'' (e.g., summer exchange information of PolyU)\n
        The Collection will be created with collection_name, the name must follow the rules:
        0. Collection name must be unique, if the name exists then try to get this collection 
        1. The length of the name must be between 3 and 63 characters.\n
        2. The name must start and end with a lowercase letter or a digit, and it can contain dots, dashes, and underscores in between.\n
        3. The name must not contain two consecutive dots.\n
        4. The name must not be a valid IP address.\n
        """
        try: 
            self.client.create_collection(name=collection_name)
        except chromadb.db.base.UniqueConstraintError: 
            self.getCollection(collection_name)
        return collection_name



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
        The chunks content and metadata will be logged (appended) into ./assets/log/<collection_name>.json
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
        logpath = "{:0}/assets/log/{:1}.json".format(self.cur_dir, collection_name)

        logs = []
        try:  
            with open (logpath, 'r') as chunklog:
                logs = json.load(chunklog)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            logs = [] # old_log does not exist or empty
       
        added_log= [{"chunk_id": ids[i], "metadata": metadata_list[i], "page_content": documents_list[i]} \
                       for i in range(num)]
      
        logs.extend(added_log)

        # write back
        with open (logpath, "w") as chunklog:
            json.dump(logs, chunklog, indent=4)
            
        
        


    
    def query (self, collection_name: str, query_embeddings: list[list[float]]) -> dict:
        """return n (by now, set as top-3) closest results (chunks and metadatas) in order """
        collection = self.getCollection(collection_name)
        result = collection.query(
            query_embeddings=query_embeddings,
            n_results=3,
        )
        return result


    def update (self, collection_name: str, id_list: list[str], embeddings_list: list[list[float]], documents_list: list[dict], metadata_list: list[dict]):
        collection = self.getCollection(collection_name)
        num = len(documents_list)
        collection.update(
            ids=id_list,
            embeddings=embeddings_list,
            metadatas=metadata_list,
            documents=documents_list,
        )

        update_list = [{"chunk_id": id_list[i], "metadata": metadata_list[i], "page_content": documents_list[i]} \
                        for i in range(num)]
        
        # update the chunk log 
        logs = []
        logpath = "{:0}/assets/log/{:1}.json".format(self.cur_dir, collection_name)
        try:  
            with open (logpath, 'r') as chunklog:
                logs = json.load(chunklog)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            logs = [] # old_log does not exist or empty, then no need to update
        else:
            for i in range(num):
                for log in logs:
                    if (log["chunk_id"] == update_list[i]["chunk_id"]):
                        log["metadata"] = update_list[i]["metadata"]
                        log["page_content"] = update_list[i]["page_content"]
                        break

        # write back
        with open (logpath, "w") as chunklog:
            json.dump(logs, chunklog, indent=4)

    def delete(self, collection_name: str, id_list: list[str]):
        """delete the collection by list of ids
        ### can NOT be undone"""
        collection = self.getCollection(collection_name)
        collection.delete(
            ids=id_list,
        )





def load_split_pdf(filepath: str) :
    loader = PyPDFLoader(filepath)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=200, 
        chunk_overlap=20,
    )
    splits = []
    for doc in docs:
        doc_splits = text_splitter.split_text(doc.page_content)
        splits.extend(doc_splits)
    #print(splits)
    return splits

    

def test():
    """This function is just used for testing Retriever class, please don't use it outside the Retriever.py file"""
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    retriever = Retriever()

    # load and split the sample pdf
    spliter_result = load_split_pdf("{}/assets/Summer_Outbound_Info_Session.pdf".format(cur_dir)) # list of page contents
    
    # embed the chunks
    embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2", 
                                  max_seq_length=128, huggingface=True)
    collection_name = retriever.createCollection("SummerExchange")
    embed_result = embedder.encode(spliter_result).tolist() # tensor to list
    
    num = len(spliter_result)
    embeddings_list = embed_result
    documents_list = spliter_result

    # The metadata_list should be provided from embedding / text splitter, provisionally use file title

    metadata_list = [{"doc_name": "Summer_Outbound_Info_Session.pdf"} for i in range(num)]
    
    # No need to repeatedly add documents 
    # Please comment out the following two lines if you did not change the file path to a new one
    #retriever.addDocuments(collection_name=collection_name, embeddings_list=embeddings_list, \
    #                     documents_list=documents_list, metadata_list=metadata_list)
    
    query_text = "What are available summer exchange in PolyU?"
    query_embeddings = embedder.encode(query_text).tolist() # tensor to list
    query_result = retriever.query(collection_name = collection_name, query_embeddings= query_embeddings)
    
    print("The following is the full query result as a dictionary:")
    print(query_result, "\n")


    print("The following is the chunk content in the result:")
    query_result_chunks = query_result["documents"][0]
    query_result_ids = query_result["ids"][0]
    for chunk in query_result_chunks:
        print(chunk)
    
    num = len(query_result_chunks)
    context = '//\n'.join(["@" + query_result_ids[i] + "//" + query_result_chunks[i].replace("\n", ".") for i in range (num)])
                
    print("context is: ", context)
    result = generate(context=context,question=query_text,temp=0)
    print(result)
    for i in range(1,10,2):
        if result.find('FINAL ANSWER:')<0:
            time.sleep(5)
            result = generate(context=context,question=query_text,temp=i/10)
            print(i/10,result)
        else:
            break
    result = result[result.find('FINAL ANSWER:')+14:]
    print()
    print('- '*40)
    print(result)
    print('- '*40)
    


if __name__ == "__main__":
    test()
    