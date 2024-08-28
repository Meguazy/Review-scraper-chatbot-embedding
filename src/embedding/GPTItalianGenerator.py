import transformers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class Falcon7BInstructModel:

    def __init__(self):
        # Model name
        model_name = "galatolo/cerbero-7b"
        offload_folder = "/Users/meguazy/exam_bigData/googleScraper/offload"
        self.pipeline, self.tokenizer = self.initialize_model(model_name, offload_folder)

    def initialize_model(self, model_name, offload_folder):
        # Tokenizer initialization
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Pipeline setup for text generation
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
        )

        return pipeline, tokenizer

    def generate_answer(self, question, context=None):
        # Preparing the input prompt
        #prompt = question if context is None else f"{context}\n\n{question}"

        messages=[
            {
                "role": "system",
                "content": "Conversazione tra un umano ed un assistente AI."
            },
            {
                "role": "user",
                "content": "Come posso distinguere un AI da un umano?"
            },
        ]

        prompt = self.pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        generated_text = self.pipeline(prompt, max_new_tokens=128)[0]['generated_text']
 
        # Extracting and returning the generated text
        return generated_text
