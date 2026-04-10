
import streamlit as st
from pages import home, generate_image, generate_mcqs, sql_question

PAGES = {
    "Home": home,
    "SQL question": sql_question,
    "Generate Image": generate_image,
    "Generate MCQs": generate_mcqs
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()
