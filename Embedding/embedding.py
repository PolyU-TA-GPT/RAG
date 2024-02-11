import sentenceEmbeddings
import argparse

def main():
    parser = argparse.ArgumentParser(description='Encode sentences to sentence embeddings')
    parser.add_argument('sentences', type=str, nargs='+', help='Sentences to encode')
    parser.add_argument('--model', type=str, default="all-MiniLM-L6-v2", help='Model to use for encoding')
    parser.add_argument('--max_seq_length', type=int, default=128, help='Maximum sequence length')
    parser.add_argument('--huggingface', action=argparse.BooleanOptionalAction, default=False, help='Use huggingface model')
    args = parser.parse_args()
    se = sentenceEmbeddings.sentenceEmbeddings(args.model, args.max_seq_length, args.huggingface)
    embeddings = se.encode(args.sentences)
    for sentence, embedding in zip(args.sentences, embeddings):
        print("Sentence:", sentence)
        print("Embedding:", embedding)
        print("")

if __name__ == "__main__":
    main()