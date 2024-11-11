import tiktoken  # Importing the tiktoken library

class TokenizationHandler:
    def __init__(self):
        # Initialize a dictionary of available models
        self.models = {
            'r50k_base': tiktoken.get_encoding('r50k_base'),  # Model for r50k_base
            'p50k_base': tiktoken.get_encoding('p50k_base'),  # Model for p50k_base
            'cl100k_base': tiktoken.get_encoding('cl100k_base'),  # Model for cl100k_base
            'o200k_base': tiktoken.get_encoding('o200k_base'),  # Model for o200k_base
            'gpt2': tiktoken.get_encoding('gpt2'),  # Model for GPT-2
            # Add more models as needed
        }

    def tokenize(self,text, model_name):
        
        if model_name not in self.models:
            raise ValueError("Unsupported model name")  # Raise an error if the model is not supported

        #raw_text = file.read().decode('utf-8')
        print(f"Raw text : {text}")
        
        encoding = self.models[model_name]  # Get the selected model's encoding
        tokens = encoding.encode(text)  # Tokenize the input text
        token_ids = tokens  # Token IDs are the same as the encoded tokens
        
        # Calculate token bytes
        token_bytes = [list(encoding.decode_single_token_bytes(token)) for token in tokens]
        
        num_tokens = len(tokens)  # Calculate the number of tokens
        return tokens, token_ids, token_bytes, num_tokens  # Return tokens, token IDs, token bytes, and number of tokens