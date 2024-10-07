import google.generativeai as genai
import streamlit as st
from langchain_openai import AzureChatOpenAI, AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv('GENAI_API_KEY')) 
# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.3,
  "top_p": 1.0,
  "top_k": 100,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model_gemini = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  generation_config=generation_config)
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings)
model_gpt_4o_mini = AzureChatOpenAI(
          model="gpt-4o-mini",
          openai_api_version=os.getenv('OPENAI_API_VERSION'),
          azure_deployment='gpt4o-mini',
          max_tokens=16300,
          temperature=0.3,
          api_key=os.getenv('AZURE_OPENAI_API_KEY'),
          azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
      )

