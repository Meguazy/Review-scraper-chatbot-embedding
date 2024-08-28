from transformers import MT5Tokenizer, MT5ForConditionalGeneration

class ItalianTextGenerator:
    def __init__(self, model_name="google/mt5-large", max_input_length=1024, max_output_length=200):
        self.tokenizer = MT5Tokenizer.from_pretrained(model_name)
        self.model = MT5ForConditionalGeneration.from_pretrained(model_name)
        self.max_input_length = max_input_length
        self.max_output_length = max_output_length

    def generate_answer(self, prompt, num_beams=4):
        # Preprocess the input prompt
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=self.max_input_length)
        
        # Generate the output text
        generated_ids = self.model.generate(
            input_ids=input_ids,
            max_length=self.max_output_length,
            num_beams=num_beams,
            temperature=0.7,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            early_stopping=True
        )
        
        # Decode the generated tokens into the final output text
        generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        
        # Print diagnostic information
        print("Generated IDs:", generated_ids)
        print("Generated Token IDs:", generated_ids[0])
        
        # Convert generated token IDs to tokens and print them
        generated_tokens = [self.tokenizer.decode([token_id], skip_special_tokens=True) for token_id in generated_ids[0]]
        print("Generated Tokens:", generated_tokens)
        
        return generated_text
