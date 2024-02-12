# import
from langchain_community.document_loaders import PyPDFLoader

import os

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

# load the document and split it into chunks
path =  os.path.dirname(os.path.abspath(__file__))
loader = PyPDFLoader(path + "/../Lecture_notes/Lecture 6.pdf")
pages = loader.load_and_split()
print(pages[2])



# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
db = Chroma.from_documents(pages, embedding_function)

# query it
query = "What platforms can R programs run?"
docs = db.similarity_search(query)

# print results
print(docs)