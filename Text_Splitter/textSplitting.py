from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from llama_index.text_splitter import SentenceSplitter
from llama_index import SimpleDirectoryReader

class TextSplitting:
    def split_character(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            state_of_the_union = f.read()
        text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=300,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.create_documents([state_of_the_union])
        return texts
    
    def llama_index(self, file_path):
        splitter = SentenceSplitter(
            chunk_size=100,
            chunk_overlap=15,
        )
        documents = SimpleDirectoryReader(
            input_files=[file_path]
        ).load_data()
        nodes = splitter.get_nodes_from_documents(documents)
        return nodes

    def split_recursive_character(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            state_of_the_union = f.read()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 300, 
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.create_documents([state_of_the_union])
        return texts

    def split_single_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, 
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        splits = []
        for doc in docs:
            doc_splits = text_splitter.split_text(doc.page_content)
            splits.extend(doc_splits)
        return splits

if __name__ == "__main__":
    a1 = TextSplitting()

    texts = a1.split_character("./summer_exchange/summer_exchange_info.txt")
    # for text in texts:
    #     print(text)
    #     print("\n---------------\n")

    nodes = a1.llama_index("./summer_exchange/summer_exchange_info.txt")
    # for node in nodes:
    #     print(node)
    #     print("\n---------------\n")
    
    texts_recursive = a1.split_recursive_character("./summer_exchange/summer_exchange_info.txt")
    # for text in texts_recursive:
    #     print(text)
    #     print("\n---------------\n")

    single_pdf_chunks = a1.split_single_pdf("./summer_exchange/Summer_Outbound_Info_Session.pdf")
    for chunk in single_pdf_chunks:
        print(chunk)
        print("\n---------------\n")