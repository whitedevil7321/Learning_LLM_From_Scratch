import re

class TokenizerV1:
    def __init__(self, vocabulary):
        # Extend vocabulary with special tokens
        self.special_tokens = ["<|unk|>", "<|endoftext|>"]
        vocabulary = sorted(set(vocabulary + self.special_tokens))
        
        # Maps token to integer
        self.str_to_int = {token: idx for idx, token in enumerate(vocabulary)}
        # Maps integer to token
        self.int_to_str = {idx: token for token, idx in self.str_to_int.items()}

    def encode(self, text_tokens):
        """
        Converts tokens to their corresponding integers.
        Unknown tokens are replaced with "<|unk|>".
        Appends "<|endoftext|>" at the end of the encoded sequence.
        """
        encoded_tokens = []
        for token in text_tokens:
            if token in self.str_to_int:
                encoded_tokens.append(self.str_to_int[token])
            else:
                encoded_tokens.append(self.str_to_int["<|unk|>"])  # Append <|unk|> for unknown tokens
        
        # Append <|endoftext|> at the end
        encoded_tokens.append(self.str_to_int["<|endoftext|>"])
        return encoded_tokens

    def decode(self, encoded_tokens):
        """
        Converts integers back to their corresponding tokens.
        Normalizes spaces around punctuation and ensures no space after "--".
        """
        text = " ".join(
            self.int_to_str[idx] if idx in self.int_to_str else "<|unk|>" 
            for idx in encoded_tokens
        )
        # Normalize spaces around punctuation and remove space after "--"
        text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)  # Removes space before punctuation
        text = re.sub(r'\s*--\s*', '--', text)  # Ensures no spaces around "--"
        return text.strip()

if __name__ == "__main__":
    with open("the-verdict.txt", "r") as f:
        raw_text = f.read()

    # Preprocess the text: split into words while keeping punctuation as separate tokens
    preprocessed = re.findall(r'\w+|[,.:;?_!"()\']|--', raw_text)
    
    # Get unique vocabulary (all words in the text)
    all_words = sorted(set(preprocessed))
    print("Initial Vocabulary Size:", len(all_words))

    # Initialize tokenizer
    tokenizer = TokenizerV1(all_words)

    print("Final Vocabulary Size:", len(tokenizer.str_to_int))
    
    # Encode the text
    encoded_text = tokenizer.encode(preprocessed)
    print("\nEncoded Text:", encoded_text[:99])

    # Decode the text back
    decoded_text = tokenizer.decode(encoded_text)
    print("\nDecoded Text:", decoded_text[:99])

    # Accessing a specific part of the decoded text
    print("\nDecoded Character at Position 120 (if exists):", decoded_text[120] if len(decoded_text) > 120 else "Out of range")
