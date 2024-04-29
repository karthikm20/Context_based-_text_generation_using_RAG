# importing required libraries
import os
# from apikey import apikey
import streamlit as st
import pandas as pd

# from  langchain.llms import OpenAI
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import find_dotenv, load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents.base import Document
import PyPDF2
from rag_prompt_template import rag_template
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser


from langchain.prompts import PromptTemplate

from langchain_community.vectorstores import DocArrayInMemorySearch


MODEL= "llama2"
embeddings = OllamaEmbeddings()

st.title("Context based content generation using RAG 🤖")
st.write("Hello👋 I'm your AI Assistant and Will help you in generating responses based on data you provide!🚀")

#Sidebar
# with st.sidebar:
#        st.write('''*Hi welcome to this interesting AI tool that helps you building your
#                 ML projects.*''')
#        st.caption('''**As you know all we are interested in Data and we love playing with Data. 
#                 Here I am helping you to perform Exploratory Data Analysis and possibly display
#                 potential patterns and sementic trends in your data 😊.** ''')
       
#        st.divider()
#        st.caption("*<p style = 'text-align:center'>Made with love Karthik!</p>*",unsafe_allow_html=True)

if 'clicked' not in st.session_state:
      st.session_state.clicked={1:False}

def clicked(button):
      st.session_state.clicked[button]=True

def load_pdf(file): # function used to load the uploaded PDF. 
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)
    content=[]
    documents = []
    for page_num in range(num_pages):
        print("page_NO:", page_num)
        page = pdf_reader.pages[page_num]
        page_content = page.extract_text().replace('\n', ' ')
        # st.write(f"Page {page_num + 1} Content:")
        # st.write(page_content)
        document = Document(page_content)
        content.append(document) 
        # should append  metadata={'source': 'diffusion_models.pdf', 'page': 12})
        # content.append({"page_number": page_num+1, "content": page_content})
    return content


st.button("Lets get Started!", on_click=clicked, args=[1])

if st.session_state.clicked[1]:   
    st.header("Upload your file and we can get started!")
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    
    if uploaded_file is not None:
        uploaded_file.seek(0)
        pages = load_pdf(uploaded_file)
        # pages = loader.load_and_split()
        # print("Hi these are the pages--->:", pages)
        vectorstore= DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()


user_query = st.text_input("Enter your query here:")

model = Ollama(model=MODEL)



parser= StrOutputParser()

# prompt= rag_template(context="I have studied at University at Buffalo!", question= user_query)
template= """
Answer the Question based on the context below. 
If you cant answer the question, reply "I don't know!" also dont start the answer with "Based on the context" 

Context:{context}

Question:{question}

"""

prompt= PromptTemplate.from_template(template)
if st.session_state.clicked[1] and uploaded_file and user_query:   
    # print(retriever.invoke("What is strictDictionaryInference?"))# Control the number of documents using retriever top_key=2
    chain = ({"context": itemgetter("question") | retriever, "question": itemgetter("question")} 
        | prompt
        | model
        | parser 
        )

    st.write(chain.invoke({"question": user_query}))
