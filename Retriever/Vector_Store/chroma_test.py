# import
from langchain_community.document_loaders import PyPDFLoader

import os

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

class chroma_test:
    path =  os.path.dirname(os.path.abspath(__file__))
    loader = ''
    persist_directory = './chroma_db'

    def __init__ (self):
        # self.loader = PyPDFLoader(self.path + "/../Lecture_notes/Lecture 6.pdf")
        # self.loader = PyPDFLoader(self.path + "/../../Doc_Loader/Data/syllabus/SDFAAE1001Introduction to Artificial Intelligence and Data Analytics in Aerospace and Aviation Engin.pdf")
        self.loader = PyPDFLoader(self.path + "/../../Doc_Loader/Data/summer_exchange/Summer_Outbound_Info_Session.pdf")

    def init_path(self, file_path):
        self.loader = PyPDFLoader(self.path + file_path)

    

    def file_process(self):
        # load the document and split it into chunks
        
        pages = self.loader.load_and_split()
        # print(pages[2])
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
    
    def query(self, db_disk, query):
        # query it
        docs = db_disk.similarity_search(query, k=3)

        # print results
        for doc in docs:
            print(doc.page_content)
            print("------------------")

    def update(self):
        #load and process to get new pages (schedule file)
        pages = self.file_process()

        # create simple ids
        ids = [str(i) for i in range(1, len(pages) + 1)]

        # add data
        example_db = Chroma.from_documents(pages, self.embedding(), ids)
        query = "When is the quiz1"
        docs = example_db.similarity_search(query)
        print(docs[0].metadata)

        # update the metadata for a document
        docs[0].metadata = {
            "source": "test update Source",
            "new_value": "test update Value",
        }

        print(docs[0].metadata)

        # delete the last document
        print("count before", example_db._collection.count())
        example_db._collection.delete(ids=[ids[-1]])
        print("count after", example_db._collection.count())


        



    def run(self):
        pages = self.file_process()
        embedding_function = self.embedding()
        self.save_disk(pages,embedding_function)
        db_disk = self.load_disk(embedding_function)
        print("Please enter your query: ")
        query = input()
        self.query(db_disk, query)




if __name__ == '__main__':
    chroma_test_prime = chroma_test()

    #test vector store based on a prime RAG pipeline
    chroma_test_prime.run()
    print()

    # #test update of vector store
    # chroma_test_prime.init_path("/../Lecture_notes/Schedule.pdf")
    # chroma_test_prime.update()