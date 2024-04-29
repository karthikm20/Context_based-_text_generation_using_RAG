# importing required libraries
import os
# from apikey import apikey
import streamlit as st
from langchain_core.documents.base import Document
# from dotenv import find_dotenv, load_dotenv
# import pdfplumber
import PyPDF2

if 'clicked' not in st.session_state:
      st.session_state.clicked={1:False}

def clicked(button):
      st.session_state.clicked[button]=True

# def extract_data(feed):
#     data = []
#     with pdfplumber.load(feed) as pdf:
#         pages = pdf.pages
#         for p in pages:
#             data.append(p) #.extract_tables()
#     return None

def load_pdf(file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)
    content=[]
    documents = []
    for page_num in range(num_pages):
        print("page_NO:", page_num)
        page = pdf_reader.pages[page_num]
        page_content = page.extract_text().replace('\n', ' ')
        st.write(f"Page {page_num + 1} Content:")
        st.write(page_content)
        document = Document(page_content)
        content.append(document) 
        # should append  metadata={'source': 'diffusion_models.pdf', 'page': 12})
        # content.append({"page_number": page_num+1, "content": page_content})

    # for item in content:
    #     page_number = item['page_number']
    #     page_content = item['content']  # Rename 'content' to 'page_content'
    #     document = Document(page_content)
    #     documents.append(document)
    return content


st.button("Lets get Started!", on_click=clicked, args=[1])

if st.session_state.clicked[1]:   
    st.header("Exploratory Data Analysis")
    st.subheader("Solution") 
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    
    if uploaded_file is not None:
        pages = load_pdf(uploaded_file)
        # pages = loader.load_and_split()
        print("Hi these are the pages--->:", pages)
    
    


#     if user_csv is not None: 
#           user_csv.seek(0)
#           df= pd.read_csv(user_csv, low_memory=False)
    
# with st.sidebar:
#     with st.expander("Steps in EDA"):
#         st.write(llm("What are the steps in EDA"))