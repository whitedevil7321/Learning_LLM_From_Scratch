import re

class SimpleTokenizerV2:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}
    
    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [
            item if item in self.str_to_int 
            else "<|unk|>" for item in preprocessed
        ]

        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
        
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        # Replace spaces before the specified punctuations
        text = re.sub(r'\s+([,.:;?!"()\'])', r'\1', text)
        return text
    
if __name__ == "__main__":

    with open("the-verdict.txt", "r") as f:
        raw_text = f.read()
    
    # Preprocess the text
    preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
    
    # Get unique vocabulary (all words in the text)
    all_words = sorted(set(preprocessed))
    
    # Extend the vocabulary with special tokens
    all_words.append("<|endoftext|>")
    all_words.append("<|unk|>")
    vocab = {token: integer for integer, token in enumerate(all_words)}
        
    # Initialize tokenizer
    tokenizer = SimpleTokenizerV2(vocab)

    text1 = "Hello, do you like tea?"
    text2 = "In the sunlit terraces of the palace."

    text = " <|endoftext|> ".join((text1, text2))
    encoded_text = tokenizer.encode(text)
    decoded_text = tokenizer.decode(encoded_text)
    
    print("Decoded Text:")
    print(decoded_text)
    print("\nOriginal Text:")
    print(text)
