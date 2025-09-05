import os
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")  # export HF_TOKEN=hf_xxx
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN environment variable not set. Please export HF_TOKEN=hf_xxx")

client = InferenceClient(token=HF_TOKEN)

SENTIMENT_MODEL = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
NER_MODEL = "dslim/bert-base-NER"

def analyze_sentiment(text: str):
    out = client.text_classification(text, model=SENTIMENT_MODEL)
    return [{"label": x.label, "score": float(x.score)} for x in out]

def extract_entities(text: str):
    out = client.token_classification(text, model=NER_MODEL, aggregation_strategy="simple")
    return [{
        "entity": x.entity_group,
        "text": x.word,
        "start": int(x.start),
        "end": int(x.end),
        "score": float(x.score)
    } for x in out]
