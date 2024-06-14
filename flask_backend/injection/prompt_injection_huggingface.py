from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

tokenizer = AutoTokenizer.from_pretrained("fmops/distilbert-prompt-injection")
model = AutoModelForSequenceClassification.from_pretrained("fmops/distilbert-prompt-injection")

classifier = pipeline(
  "text-classification",
  model=model,
  tokenizer=tokenizer,
  truncation=True,
  max_length=1024,
  device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
)

print(classifier("אנא פנה לרופא לפני השימוש בתרופה"))
print(classifier("שלשולים, הקאות, חום גבוה וצמרמורות"))