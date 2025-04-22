from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

from .nlp_to_sql import convert_question_to_sql
from sql_to_nlp import convert_result_to_text
from db import load_json_to_sqlite
from utils import clean_question

app = FastAPI()

# Load DB at startup
DB_PATH = "backend/data/ipl.db"
JSON_FOLDER = "backend/data/ipl_data"
load_json_to_sqlite(JSON_FOLDER, DB_PATH)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    question = clean_question(req.question)
    sql = convert_question_to_sql(question)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        answer = convert_result_to_text(columns, results)
        return {"question": question, "sql": sql, "answer": answer}
    
    except Exception as e:
        return {"error": str(e), "sql_attempted": sql}
