import streamlit as st
from openai import OpenAI
client = OpenAI(api_key="---")

def generate_mcq(difficulty):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a computer science teacher."},
            {"role": "user", "content": f"""
Generate one {difficulty} level MCQ on computer science in this EXACT format:

Question: <question>
A: <option>
B: <option>
C: <option>
D: <option>
Answer: <A/B/C/D>
"""}
        ]
    )
    return completion.choices[0].message.content


def evaluate_mcq(question, user_answer):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a teacher explaining answers."},
            {"role": "user", "content": f"Question: {question}\nUser Answer: {user_answer}\nExplain the correct answer briefly."}
        ]
    )
    return completion.choices[0].message.content


def parse_mcq(mcq_text):
    lines = mcq_text.split("\n")
    data = {}

    for line in lines:
        if line.startswith("Question:"):
            data["question"] = line.replace("Question:", "").strip()
        elif line.startswith("A:"):
            data["A"] = line.replace("A:", "").strip()
        elif line.startswith("B:"):
            data["B"] = line.replace("B:", "").strip()
        elif line.startswith("C:"):
            data["C"] = line.replace("C:", "").strip()
        elif line.startswith("D:"):
            data["D"] = line.replace("D:", "").strip()
        elif line.startswith("Answer:"):
            data["answer"] = line.replace("Answer:", "").strip()

    return data


def app():
    st.header("MCQ Practice (CS)")

    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    if "mcq" not in st.session_state:
        st.session_state.mcq = None

    if st.button("Generate Question"):
        st.session_state.mcq = generate_mcq(difficulty)

    if st.session_state.mcq:
        mcq_data = parse_mcq(st.session_state.mcq)

        st.subheader("Question:")
        st.write(mcq_data["question"])

        user_choice = st.radio(
            "Choose your answer:",
            [
                f"A: {mcq_data['A']}",
                f"B: {mcq_data['B']}",
                f"C: {mcq_data['C']}",
                f"D: {mcq_data['D']}"
            ]
        )

        selected_option = user_choice[0]  # A/B/C/D
        correct_answer = mcq_data["answer"]

        if st.button("Submit Answer"):

            # Instant result
            if selected_option == correct_answer:
                st.success("Correct Answer!")
            else:
                st.error(f"Wrong! Correct answer is {correct_answer}")

            # AI explanation
            explanation = evaluate_mcq(st.session_state.mcq, selected_option)

            st.subheader("Explanation:")
            st.write(explanation)
