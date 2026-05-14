# ================================
# FILE: ai_helper.py
# ================================

from openai import OpenAI
from dotenv import load_dotenv
import os

# --------------------------------
# LOAD ENV VARIABLES
# --------------------------------

load_dotenv()

# --------------------------------
# OPENAI CLIENT
# --------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# --------------------------------
# AI FUNCTION
# --------------------------------

def ask_ai(question, df):

    preview = df.head(10).to_string()

    prompt = f"""
    You are a professional business data analyst.

    Dataset Preview:
    {preview}

    User Question:
    {question}

    Give short analytical insights based on the dataset.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content