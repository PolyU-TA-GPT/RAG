from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Lecture_notes/Lecture 1.pdf")
pages = loader.load_and_split()
print(pages[0])