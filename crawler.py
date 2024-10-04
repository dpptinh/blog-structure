from datetime import datetime
import trafilatura
import fitz  # PyMuPDF
from datetime import datetime
import requests
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
twitter_api = st.secrets['TWITTER_API']
def convert_time_to_timestamp(day, month, year):
    # Tạo đối tượng datetime từ ngày, tháng, năm
    time_obj = datetime(int(year), int(month), int(day))
    # Chuyển đổi đối tượng datetime thành timestamp
    timestamp = int(time_obj.timestamp())
    return timestamp
  
def get_context_from_website(links: list) -> str:
    full_context = '      <blog-collection>'
    count = 1
    for link in links:
        html =  trafilatura.fetch_url(link)
        context =  trafilatura.extract(html, output_format = "markdown", include_formatting= True, include_tables= True, include_images=True, include_links=True)
        full_context += f"""\n        <blog-post-{count}>
                <content>
                {context}
                </content>
            </blog-post>"""
        count += 1
    full_context += "\n       </blog-collection>"
    return full_context

def get_tweets(link_twitter: str, last_timestamp: int) -> str:
    print(twitter_api.format(link_twitter.split("/")[-1], last_timestamp))
    tweets = requests.get(twitter_api.format(link_twitter.split("/")[-1], last_timestamp))
    print(tweets)
    return tweets.json()
    
def get_tweet_content(tweet, index) -> str:
    context = f"""<tweet id="{index}">
    <date>{tweet['last_updated']}</date>
    <content>\n{tweet['post_title']}\n</content>
</tweet>
"""
    return context
    
def get_text_from_pdf(pdf_file) -> str:
   text = "      <white-paper>: \n"
   # Đảm bảo rằng pdf_file là một đối tượng BytesIO
   pdf_file.seek(0)  # Đặt con trỏ về đầu file
   with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
     count = 1
     for page in doc:
         text += f"\n\n============================== PAGE {count}: =============================\n" + page.get_text()
         count += 1
   print("PDF CONTENT: \n", text)
   return text + "\n       </white-paper>"
