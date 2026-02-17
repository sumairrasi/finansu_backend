from langchain_qwq import ChatQwen
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

#this is part for qwene

os.environ["OPENAI_API_KEY"] = "local" 

llm = ChatQwen(
    base_url=""
)

# this is for openai
# llm=ChatOpenAI()