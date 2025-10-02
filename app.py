import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

st.title("My First Agent Deployment")

# definition of the model
llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    groq_api_key = GROQ_API_KEY,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that engages into conversations and translates {input_language} to {output_language}.",
        ),
        ("human", "Translate the {input} from {input_language} to {output_language}."),  # revised prompt
    ]
)
# chain of action
chain = prompt | llm

def generate_response(input_text, input_language, output_language):
    st.info(chain.invoke(
                {
                    "input_language": input_language,
                    "output_language": output_language,
                    "input": input_text,
                }).content)


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    input_language = st.text_input("Input Language", "English")
    print(input_language)
    output_language = st.text_input("Output Language", "German")
    print(output_language )
    submitted = st.form_submit_button("Submit")
    if not GROQ_API_KEY or not GROQ_API_KEY.startswith("gsk_"):
        st.warning("Please enter your Groq API key!", icon="⚠")
    if submitted and GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"):
        generate_response(text, input_language, output_language)
