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
        self.loader = PyPDFLoader(self.path + "/../Lecture_notes/Lecture 6.pdf")

    def init_path(self, file_path):
        self.loader = PyPDFLoader(self.path + file_path)

    

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

    def update(self):
        #load and process to get new pages (schedule file)
        pages = self.file_process("/../Lecture_notes/Schedule.pdf")

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


    def run(self):
        pages = self.file_process()
        embedding_function = self.embedding()
        self.save_disk(pages,embedding_function)
        db_disk = self.load_disk(embedding_function)
        self.query(db_disk)


if __name__ == '__main__':
    chroma_test_run = chroma_test()
    chroma_test_run.run()
    chroma_test_run.update()