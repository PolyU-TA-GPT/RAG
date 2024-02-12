# import
from langchain_community.document_loaders import PyPDFLoader

import os

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

class Chroma:

    def file_process(self):
        # load the document and split it into chunks
        path =  os.path.dirname(os.path.abspath(__file__))
        loader = PyPDFLoader(path + "/../Lecture_notes/Lecture 6.pdf")
        pages = loader.load_and_split()
        print(pages[2])
        return pages

    def embedding():

        # create the open-source embedding function
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_function
    
    def save_disk(pages, embedding_function, persist_directory):

        # save the embedding into Chroma db (in my disk now)
        db = Chroma.from_documents(pages, embedding_function, persist_directory='./chroma_db')
        return db

    def load_disk(embedding_function):
        # load from disk 
        db_disk = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
        return db_disk
    
    def query(db_disk):
        # query it
        query = "What platforms can R programs run?"
        docs = db_disk.similarity_search(query)

        # print results
        print(docs[0].page_content)

    def run(self):
        pages = file_process()