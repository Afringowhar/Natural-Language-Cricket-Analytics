from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load actual model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("tscholak/optical-small")
model = AutoModelForSeq2SeqLM.from_pretrained("tscholak/optical-small")

def convert_question_to_sql(question: str) -> str:
    inputs = tokenizer(question, return_tensors="pt")
    outputs = model.generate(**inputs)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql
