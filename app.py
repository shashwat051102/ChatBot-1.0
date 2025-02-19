import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

# Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot with OPENAI"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful; assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,llm, temperature,max_tokens):
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(groq_api_key=api_key,model = llm)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer
    

# Title of the app
st.title('Enhanced Q&A Chatbot using models of your own choice')

# Sidebar for settings
st.sidebar.title('Settings')
# api_key = st.sidebar.text_input("Enter your OPENAI API key:", type="password")

# api_key = os.getenv('OPENAI_API_KEY')



# Drop down to select various OPENAI model
llm = st.sidebar.selectbox("Select your model", ["Deepseek-R1-Distill-Llama-70b","Llama-3.3-70b-Versatile","Llama-3.3-70b-Specdec"])










# Adjust response temperature
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value = 300, value = 150)


# Main Interface for user input 
st.write("Ask your question here:")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the input")