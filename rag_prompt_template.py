
# Sample prompt template 
from langchain.prompts import PromptTemplate

def rag_template(context, question): 
    template= """
    Generate queries to the Question based on the context provided below. 
    If you cant answer the question, reply "I don't know!"

    Context: {context}

    Question: {question}

    """
    prompt= PromptTemplate.from_template(template)
    new_prompt= prompt.format(context= context, question= question)
    print("Response from rag template!", type(new_prompt))
    return new_prompt
    # print(prompt.format(context="Here is a context", question="Here is a question"))