from langchain_community.document_loaders import PyPDFLoader

import os
def load_split_pdf(filepath):
    path =  os.path.dirname(os.path.abspath(__file__))
    loader = PyPDFLoader(path + filepath)
    pages = loader.load_and_split()
    print(pages)