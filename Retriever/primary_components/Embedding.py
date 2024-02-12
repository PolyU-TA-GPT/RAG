from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")