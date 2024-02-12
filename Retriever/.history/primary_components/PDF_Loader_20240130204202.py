from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("../")
pages = loader.load_and_split("Lecture_notes/Lecture 1.pdf")
print(pages[0])