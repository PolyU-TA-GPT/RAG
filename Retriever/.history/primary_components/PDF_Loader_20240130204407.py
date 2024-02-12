from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Lecture_notes/Schedule.pdf")
pages = loader.load_and_split()
print(pages[2])