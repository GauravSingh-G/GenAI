import streamlit as st
import requests
import numpy as np
import sounddevice as sd
import io
from scipy.io.wavfile import write
import wave
from openai import OpenAI
client = OpenAI(api_key="---")



def generate_sql(question):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert SQL teacher."},
            {"role": "user", "content": f"Convert this English question into SQL query:\n{question}"}
        ]
    )
    return completion.choices[0].message.content
    
def evaluate_sql(question, correct_sql, user_sql):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL teacher. Evaluate the user's SQL query."},
            {"role": "user", "content": f"""
Question: {question}

Correct SQL: {correct_sql}

User SQL: {user_sql}

Tell:
- Is it correct or not
- Mistakes (if any)
- Suggest improvements
"""}
        ]
    )
    return completion.choices[0].message.content
    
def app():
    st.header("SQL Practice (English → SQL)")

    question = st.text_area("Enter your question in English")

    if "correct_sql" not in st.session_state:
        st.session_state.correct_sql = None

    if st.button("Generate SQL"):
        if question:
            correct_sql = generate_sql(question)
            st.session_state.correct_sql = correct_sql

            st.subheader("AI Generated SQL:")
            st.code(correct_sql, language="sql")
        else:
            st.error("Please enter a question")

    if st.session_state.correct_sql:
        user_sql = st.text_area("Write your SQL query")

        if st.button("Check Answer"):
            if user_sql:
                feedback = evaluate_sql(
                    question,
                    st.session_state.correct_sql,
                    user_sql
                )

                st.subheader("Feedback:")
                st.write(feedback)
            else:
                st.error("Please write your SQL query")
