# from langchain_qwq import ChatQwen
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

#this is part for qwene

# os.environ["OPENAI_API_KEY"] = "local" 

# llm = ChatQwen(
#     base_url=""
# )

# this is for openai
# llm=ChatOpenAI()

#try with qwene model
llm = ChatOpenAI(
    model="Qwen/Qwen2-VL-2B-Instruct",
    base_url="http://111.92.62.192:5072/v1",
    api_key="EMPTY"   
)
