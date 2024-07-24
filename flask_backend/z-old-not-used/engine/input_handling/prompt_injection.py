from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from models.model_config import model_config

class PromptInjectionModel:
    def __init__(self) -> None:
        self.prompt_injection_model_name = "ProtectAI/deberta-v3-base-prompt-injection"
        self.prompt_injection_model = None
        self.prompt_injection_model_tokenizer = None

    def load_model(self):    
        self.prompt_injection_model_tokenizer = AutoTokenizer.from_pretrained(self.prompt_injection_model_name)
        self.prompt_injection_model = AutoModelForSequenceClassification.from_pretrained(self.prompt_injection_model_name)        

    def is_injection(self, input_prompt: str) -> bool:   
        if self.prompt_injection_model and self.prompt_injection_model_tokenizer:     
            classifier = pipeline(
            "text-classification",
            model=self.prompt_injection_model,
            tokenizer=self.prompt_injection_model_tokenizer,
            truncation=True,
            max_length=model_config.MAX_TOKENS_LIMIT,
            device=model_config.DEVICE,
            )

            response = classifier(input_prompt) 
            return response[0]['label'] ==  "INJECTION"  
        
        # [ # return 1 dict out of these two
            # [
            #     {
            #     "label": "SAFE",
            #     "score": 0.9999998807907104
            #     },
            #     {
            #     "label": "INJECTION",
            #     "score": 1.313596982299714e-7
            #     }
            # ]
        # ]    
