from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langserve import add_routes
from fastapi import FastAPI


load_dotenv()

groq_api_key = os.getenv("groq_api_key")
model = ChatGroq(model="Llama3-8b-8192",api_key=groq_api_key)

parser = StrOutputParser()

generic = 'Translate the follwing into {language}'

prompt = ChatPromptTemplate.from_messages([
    ('system',generic),
    ('user','{text}')
])

chain = prompt | model | parser


app = FastAPI(title="LangChain server",version="1.0")

add_routes(
    app,chain,path="/chain"
)

if __name__=="__main__" : 
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)