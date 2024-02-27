import sys  
sys.path.append(r'./Text_Splitter')  
from textSplitting import TextSplitting
from sentenceEmbeddings import sentenceEmbeddings

class TAembedding:



    '''This class is used to split the text and encode the text into embeddings.'''
    def __init__(self, model = "sentence-transformers/all-MiniLM-L6-v2", max_seq_length = 512, huggingface = True):
        self.text_splitter = TextSplitting()
        self.encoder = sentenceEmbeddings("sentence-transformers/all-MiniLM-L6-v2", max_seq_length, huggingface)
        self.result = []



    '''This function is used to split the text into sentences and encode the sentences into embeddings.'''
    def split_recursive(self, file_path):
        texts_recursive = self.text_splitter.split_recursive_character(file_path)
        for text in texts_recursive:
            dict = {}
            dict['sentence'] = text.page_content
            dict['embedding'] = self.encoder.encode(text.page_content)
            self.result.append(dict)
        return self.result
    


    '''This function is used to split the single pdf into sentences and encode the sentences into embeddings.'''
    def split_pdf(self, file_path):
        single_pdf_chunks = self.text_splitter.split_single_pdf(file_path)
        for chunk in single_pdf_chunks:
            dict = {}
            dict['sentence'] = chunk
            dict['embedding'] = self.encoder.encode(chunk)
            self.result.append(dict)
        return self.result

if __name__ == "__main__":
    a1 = TAembedding()
    # texts_recursive = a1.split_recursive_character("./Embedding/output.txt")
    # print(len(texts_recursive))
    # print(texts_recursive[0:5])
    single_pdf_chunks = a1.split_pdf("./Text_Splitter/summer_exchange/Summer_Outbound_Info_Session.pdf")
    print(len(single_pdf_chunks))
    print(single_pdf_chunks[0:5])
    print(single_pdf_chunks[0]['embedding'].shape)