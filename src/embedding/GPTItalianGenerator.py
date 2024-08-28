import transformers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class Falcon7BInstructModel:

    def __init__(self):
        # Model name
        model_name = "tiiuae/falcon-7b-instruct"
        self.pipeline, self.tokenizer = self.initialize_model(model_name)

    def initialize_model(self, model_name):
        # Tokenizer initialization
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Pipeline setup for text generation
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
            tokenizer=tokenizer,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto",
        )

        return pipeline, tokenizer

    def generate_answer(self, question, context=None):
        # Preparing the input prompt
        prompt = question if context is None else f"{context}\n\n{question}"

        # Generating responses
        sequences = self.pipeline(
            prompt,
            max_length=500,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
        )

        # Extracting and returning the generated text
        return sequences['generated_text']
