from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv


env_file = "travelagent.env"
load_dotenv(dotenv_path=env_file)

gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))