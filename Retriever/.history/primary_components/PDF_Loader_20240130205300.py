from langchain_community.document_loaders import PyPDFLoader
import os
path =  os.path.dirname(os.path.abspath(__file__))
loader = PyPDFLoader(path + "/../Lecture_notes/Lecture 6.pdf")
pages = loader.load_and_split()
print(pages[2])