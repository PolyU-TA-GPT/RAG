from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch

class sentenceEmbeddings:
    def __init__(self, model = "all-MiniLM-L6-v2", max_seq_length = 128, huggingface = False):
        self.huggingface = huggingface
        if not self.huggingface:
            self.model = SentenceTransformer(model)
            self.model.max_seq_length = max_seq_length
            self.sentence_embeddings = []
            self.sentence_embeddings_dict = {}
            self.sentence_embeddings_dict['sentence'] = []
        else:
            self.model = AutoModel.from_pretrained(model)
            self.tokenizer = AutoTokenizer.from_pretrained(model)
            self.model.max_seq_length = max_seq_length
            self.sentence_embeddings = []
            self.sentence_embeddings_dict = {}
            self.sentence_embeddings_dict['sentence'] = []


    def encode(self, sentences):
        if not self.huggingface:
            self.sentence_embeddings = self.model.encode(sentences)
            self.sentence_embeddings_dict['sentence'] = sentences
            self.sentence_embeddings_dict['embeddings'] = self.sentence_embeddings
            return self.sentence_embeddings
        else:
            encoded_input = self.tokenizer(sentences, padding=True, truncation=True, max_length=self.model.max_seq_length, return_tensors="pt")
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            sentence_embeddings = self.mean_pooling(model_output, encoded_input["attention_mask"])
            self.sentence_embeddings = sentence_embeddings
            self.sentence_embeddings_dict['sentence'] = sentences
            self.sentence_embeddings_dict['embeddings'] = sentence_embeddings
            return sentence_embeddings

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask
  
    def finetune():
        pass   
    
if __name__ == "__main__":
    # Example usage
    sentences = ["This is an example sentence", "Each sentence is converted to a vector"]
    model = "sentence-transformers/all-MiniLM-L6-v2"
    max_seq_length = 128
    huggingface = True
    se = sentenceEmbeddings(model, max_seq_length, huggingface)
    embeddings = se.encode(sentences)
    for sentence, embedding in zip(sentences, embeddings):
        print("Sentence:", sentence)
        print("Embedding:", embedding)
        print("")
