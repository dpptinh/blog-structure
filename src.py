import streamlit as st
import io
import ast
from dotenv import load_dotenv
# load_dotenv()
import os
import ast
import google.generativeai as genai
from crawler import get_context_from_website, get_text_from_pdf, convert_time_to_timestamp, get_tweets, get_tweet_content

from model import model_gemini, model_gpt_4o_mini
from prompts import summary_prompt, information_extraction_prompt
# Streamlit UI
st.title("Crawl và Generate Content")
links_input = st.text_area("Nhập các link (mỗi link trên một dòng, sử dụng nút enter để xuống dòng):")
project_name = st.text_input("Nhập tên dự án:")
twitter_link = st.text_input("Nhập link Twitter:")
year, month, day = str(st.date_input("Chọn ngày tháng năm:")).split("-")
pdf_file = st.file_uploader("Tải lên file PDF:", type=["pdf"])  # Thêm uploader cho file PDF
model_choice = st.selectbox("Chọn mô hình:", ["gpt_4o_mini", "gemini"], index=0)  # Thêm lựa chọn mô hình, mặc định là gpt_4o_mini

if st.button("Generate"):
    timestamp =  convert_time_to_timestamp(day, month, year)
    print(timestamp)
    tweets = get_tweets(twitter_link, timestamp)
    links_input = links_input.strip().strip("\n")
    links = links_input.splitlines()
    
    raw_content = "\n   <projection-information>"
    if links:
        blog_content = get_context_from_website(links)
        raw_content += f"\n{blog_content}"
    if pdf_file:
        pdf_content = get_text_from_pdf(pdf_file)
        raw_content += f"\n\n{pdf_content}"
    if twitter_link:
      count = 1
      for tweet in tweets:
        tweet_content = get_tweet_content(tweet, count)
        raw_content += f"\n\n{tweet_content}" 
    raw_content += "\n </projection-information>"
    
    if links or pdf_file or twitter_link:
      with st.spinner("Generating content..."):
        print(twitter_link)
        if model_choice == "gemini":
          summary = model_gemini.generate_content(summary_prompt.format(content = raw_content, project_name = project_name)).candidates[0].content.parts[0].text.strip().strip("\n")
        else:
          summary = model_gpt_4o_mini.invoke(summary_prompt.format(content = raw_content, project_name = project_name)).content
        # print(summary)
        st.markdown("\n\n # SUMMARY ")
        st.markdown(summary)
        
        st.markdown("\n\n # INFORMATION EXTRACTION")
        extraction_tables = []
        for tweet in tweets:
            tweet_content = get_tweet_content(tweet, count) 
            if model_choice == "gemini":
              information_extraction = model_gemini.generate_content(information_extraction_prompt.format(content = tweet_content, project_name = project_name)).candidates[0].content.parts[0].text.strip().strip("\n")
            else:
              information_extraction = model_gpt_4o_mini.invoke(information_extraction_prompt.format(content = tweet_content, project_name = project_name)).content
            # print(information_extraction)
            try:
              extraction_dict = ast.literal_eval(information_extraction)
            except Exception as e:
              st.error(f"Error parsing extraction for tweet on {tweet['post_created']}: {e}")
              continue
                
            st.markdown(f"## TWEET on {tweet['post_created']} ")
            if isinstance(extraction_dict, dict):
                  # Tạo tiêu đề bảng từ các khóa của dictionary
              headers = "| " + " | ".join(extraction_dict.keys()) + " |"
              separator = "| " + " | ".join(["---"] * len(extraction_dict)) + " |"
              # Tạo hàng dữ liệu từ các giá trị của dictionary
              values = "| " + " | ".join(str(v) for v in extraction_dict.values()) + " |"
              # Kết hợp thành bảng Markdown
              markdown_table  = f"{headers}\n{separator}\n{values}"
              st.markdown(markdown_table, unsafe_allow_html=True) 
              extraction_tables.append(markdown_table)


      # Prepare Markdown for download
      markdown_buffer = io.BytesIO()
      markdown_buffer.write(summary.encode())
      markdown_buffer.seek(0)
      
      extractions_content = "\n\n".join(extraction_tables)
      extractions_buffer = io.BytesIO()
      extractions_buffer.write(extractions_content.encode())
      extractions_buffer.seek(0)

    # Button to download Summary Markdown
      st.download_button("Tải xuống Tóm tắt", markdown_buffer, file_name="generated_summary.txt", mime="text/plain")
      
      # Button to download Extractions Markdown
      st.download_button("Tải xuống Trích xuất", extractions_buffer, file_name="generated_extractions.txt", mime="text/plain")
    else:
      st.error("Vui lòng nhập thông tin dự án!")
