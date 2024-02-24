import sys  
sys.path.append(r'./Text_Splitter')  
from textSplitting import TextSplitting
from sentenceEmbeddings import sentenceEmbeddings
a1 = TextSplitting()
texts_recursive = a1.split_recursive_character("./Embedding/output.txt")
result = []
result_sentence = []
result_embedding = []
encoder = sentenceEmbeddings("sentence-transformers/all-MiniLM-L6-v2", 128, True)

'''Compute the embeddings one by one
return a list of dictionaries, each dictionary contains a sentence and its embedding'''

# for text in texts_recursive:
#     dict = {}
#     dict['sentence'] = text.page_content
#     dict['embedding'] = encoder.encode(text.page_content)
#     result.append(dict)
# print(len(result))
# print(result[0:5])


'''Compute the embeddings in batches
return a list of sentences, a list of embeddings'''

for text in texts_recursive:
    result_sentence.append(text.page_content)

result_embedding.append(encoder.encode(result_sentence))
print(len(result_sentence))
print(result[0:5])
