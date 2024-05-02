# Code to print out log likelihood of sentence passed through HF model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np

def get_log_likelihood(model, tokenizer, sentence):
     inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
     input_ids = inputs.input_ids
     attention_mask = inputs.attention_mask
     with torch.no_grad():
          outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
     log_likelihood = outputs.loss.item()
     return log_likelihood

model_name = "google/mt5-large"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
sentence = "इन सरल आठ तकनीकों का उपयोग कर के, आप घर पर आराम से समाचार वृतान्त बना सकते हैं।, सही? हाँ, न्यूज़रूम में केवल संवाददाता ही समाचार कहानी लिख सकते हैं, और इसे करने में २० क़दमों की ज़रूरत होती है।"
log_likelihood = get_log_likelihood(model, tokenizer, sentence)

print(log_likelihood)