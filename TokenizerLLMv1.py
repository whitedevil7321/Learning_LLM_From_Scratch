import re

class TokenizerV1:
    def __init__(self, vocabulary):
        # Maps token to integer
        self.str_to_int = {token: idx for idx, token in enumerate(vocabulary)}
        # Maps integer to token
        self.int_to_str = {idx: token for token, idx in self.str_to_int.items()}

    def encode(self, text_tokens):
        """
        Converts tokens to their corresponding integers.
        Raises a ValueError if an unknown token is encountered.
        """
        return [self.str_to_int[token] for token in text_tokens]

    def decode(self, encoded_tokens):
        """
        Converts integers back to their corresponding tokens.
        Normalizes spaces around punctuation and ensures no space after "--".
        """
        text = " ".join([self.int_to_str[idx] for idx in encoded_tokens])
        # Normalize spaces around punctuation and remove space after "--"
        text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)  # Removes space before punctuation
        text = re.sub(r'\s*--\s*', '--', text)  # Ensures no spaces around "--"
        return text

if __name__ == "__main__":
    with open("the-verdict.txt", "r") as f:
        raw_text = f.read()

    # Preprocess the text
    preprocessed = re.split(r'(\s+|[,.:;?_!"()\']|--)', raw_text)  # Split on punctuation and whitespace
    preprocessed = [item.strip() for item in preprocessed if item.strip()]  # Remove empty strings

    # Get unique vocabulary
    all_words = sorted(set(preprocessed))
    print("Initial Vocabulary Size:", len(all_words))

    # Extend the vocabulary with special tokens
    all_words.extend(["|<endoftext>|", "|<unk>|"])
    print("Final Vocabulary Size:", len(all_words))

    # Initialize tokenizer
    tokenizer = TokenizerV1(all_words)
    print("Original Text:\n", raw_text[:99])

    # Encode the text
    encoded_text = tokenizer.encode(preprocessed)
    print("Encoded Text:", encoded_text[:99])

    # Decode the text back
    decoded_text = tokenizer.decode(encoded_text)
    print("Decoded Text:\n", decoded_text[:99])

    