import transformers
import torch
from transformers import AutoTokenizer, FalconForCausalLM

class Falcon7BInstructModel:

    def __init__(self, model_name = "tiiuae/falcon-7b-instruct"):
        # Model name
        self.model_name = model_name
        self.pipeline, self.tokenizer = self.initialize_model()

    def initialize_model(self):
        # Tokenizer initialization
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")

        # Load the tokenizer and model
        model = FalconForCausalLM.from_pretrained(self.model_name)

        # Move the model to the GPU
        model.to(device)

        # Pipeline setup for text generation
        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device=0 if torch.cuda.is_available() else -1,
        )

        return pipeline, tokenizer

    def generate_answer(self, question, context=None):
        # Preparing the input prompt
        prompt = question if context is None else f"{context}\n\n{question}"

        # Generating responses
        sequences = self.pipeline(
            prompt,
            max_length=1000,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
        )

        # Extracting and returning the generated text
        return sequences
