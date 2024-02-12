# import
from langchain_community.document_loaders import PyPDFLoader

import os

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

class chroma_test:
    path =  os.path.dirname(os.path.abspath(__file__))
    loader = PyPDFLoader(path + "/../Lecture_notes/Lecture 6.pdf")
    persist_directory = './chroma_db'

    def file_process(self):
        # load the document and split it into chunks
        
        pages = self.loader.load_and_split()
        print(pages[2])
        return pages

    def embedding(self):

        # create the open-source embedding function
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_function
    
    def save_disk(self, pages, embedding_function):

        # save the embedding of documents into Chroma db (in my disk now)
        db = Chroma.from_documents(pages, embedding_function, persist_directory=self.persist_directory)
    

    def load_disk(self, embedding_function):
        # load from disk 
        db_disk = Chroma(persist_directory=self.persist_directory, embedding_function=embedding_function)
        return db_disk
    
    def query(self, db_disk):
        # query it
        query = "What platforms can R programs run?"
        docs = db_disk.similarity_search(query)

        # print results
        print(docs[0].page_content)

    def run(self):
        pages = self.file_process()
        embedding_function = self.embedding()
        self.save_disk(pages,embedding_function)
        db_disk = self.load_disk(pages,embedding_function)
        self.query(db_disk)

if __name__ == '__main__':
    chroma_test_prime = chroma_test()
    chroma_test_prime.run()