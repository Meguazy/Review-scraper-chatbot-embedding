from huggingface_hub import InferenceClient

class TextGenerator:
    def __init__(self, model_name, api_key = ""):
        self.client = InferenceClient(token=api_key)
        self.model_name = model_name

    def text_generation(self, prompt):
        result = self.client.text_generation(prompt, model="mistralai/Mistral-Nemo-Instruct-2407", return_full_text=False, max_new_tokens=1000)
        return result
    
    def build_prompt(self, query_text, context = None, type="long"):
        """
        Constructs the prompt for the text generation model.
        """
        if context:
            if type == "long":
                prompt = f"Recensioni dell'azienda chiamata Fastweb:\n{context}\nLa domanda è: {query_text} \n rispondi in modo dettagliato, tenendo conto delle recensioni. La tua risposta deve essere di massimo 50 parole, non ignorare questa istruzione."
            elif type == "short":
                prompt = f"Recensioni dell'azienda chiamata Fastweb:\n{context}\nDomanda: Considerando le recensioni, {query_text} Rispondi in massimo 50 parole e rispondi solo alla domanda senza aggiungere ulteriori informazioni."
        else:
            prompt = query_text
        return prompt