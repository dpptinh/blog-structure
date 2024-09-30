import streamlit as st
import trafilatura
import google.generativeai as genai
import io
import ast
import fitz  # PyMuPDF


import trafilatura
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from googlesearch import search
prompt = """<ROLE>You are an expert SEO blog post writer. You can extract, synthesize, and rewrite AI and SEO content in MARKDOWN format while strictly preserving key original elements.</ROLE>

<INPUT>
ORIGINAL BLOG: \n{content}
</INPUT>

<TASK>
Rewrite, paraphrase the information from the provided blog post into a new, detailed blog post in Vietnamese.
Your professionally rewritten content will enhance SEO while rigorously maintaining the integrity of original data, key phrases, and quoted content.
</TASK>

<CONSTRAINTS>
1. **Preserve Original Elements:** (Importance: Critical)
   - KEEP and RETAIN ALL STATISTICS, NUMERICAL DATA, LINKS, AND FACTUAL INFORMATION exactly as stated in the original content.
   - KEEP ALL LINKS (image links - .png, .jpeg, .jpg, ..., external links) in the original content.
   - Maintain the original language for:
     a) Technical terms and industry-specific jargon
     b) Proper nouns and brand names
     c) Direct quotes from individuals or organizations
     d) ALL content enclosed in quotation marks (" ", ' ') - DO NOT TRANSLATE THESE UNDER ANY CIRCUMSTANCES
     e) Hyphenated compounds and terms containing hyphens
   - This applies to all types of quoted content, regardless of length or context.
   - If a section lacks information, you must include a sentence indicating that the information is not available. Something like "chưa có thông tin chính thức về........."

2. **Language and Tone:** (Importance: Critical)
   - Write in Vietnamese, except for the elements specified to be preserved in their original language.
   - Maintain a tone suitable for adults with a university education or higher.
   - Incorporate a friendly and engaging style, using emojis and casual language where appropriate.

3. **Structure and Length:** (Importance: Critical)
   - The first section of the blog must be titled "Tổng quan."
   - The content of "Tổng quan" section and "Kết luận" section should be consice texts while the remaining sections (Mô hình kinh doanh, Đội ngũ dự án, Định hướng phát triển, Đối thủ cạnh tranh, Thực tế đạt được/Tình hình hoạt động, Tokenomic, Mua token ở đâu?) should be long, detailed and comprehensive.
   - The content of each header and section should contain multiple paragraphs.
   - The length of the blog content should be comprehensive and detailed, reflecting the content related to the chapter titles in the original blog. However, it should not exceed 8100 tokens.

4. **Final Review:** (Importance: High)
   - Double-check the blog outline. If the outline or structure is incorrect, you must regenerate the blog.
   - Double-check all preserved elements (statistics, numerical data, links, terms, quotes) as mentioned in Constraints 1, 2, and 3 to ensure accuracy.
   - Ensure no content within quotation marks has been translated or altered.
   - Remove any content unrelated to the main topic, such as advertisements.
   - Review for overall coherence, SEO optimization, and strict adherence to content preservation rules.
</CONSTRAINTS>

<blog-outline>
  <section>
    <title>Tổng quan</title>
  </section>
  <section>
    <title>Mô hình kinh doanh</title>
  </section>
  <section>
    <title>Đội ngũ dự án</title>
  </section>
  <section>
    <title>Định hướng phát triển</title>
  </section>
  <section>
    <title>Đối thủ cạnh tranh</title>
  </section>
  <section>
    <title>Thực tế đạt được/Tình hình hoạt động</title>
  </section>
  <section>
    <title>Tokenomic</title>
  </section>
  <section>
    <title>Mua token ở đâu?</title>
  </section>
  <section>
    <title>Kết luận</title>
  </section>
</blog-outline>

<FORMAT>
  Provide only the detailed blog post in Vietnamese in MARKDOWN format with valid JSON (keys: "title" and "content"). Do not add any other explanations or notes, and do not repeat the title in the content.
</FORMAT>
"""

import os
import ast
import google.generativeai as genai

genai.configure(api_key=st.secrets['GENAI_API_KEY'])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.21,
  "top_p": 1.0,
  "top_k": 120,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model_gemini = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  generation_config=generation_config)
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings)
  
# Function to crawl content from links
def get_context(links: list) -> str:
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
    full_context += "\n     </blog-collection>"
    return full_context

def extract_text_from_pdf(pdf_file) -> str:
   text = ""
   # Đảm bảo rằng pdf_file là một đối tượng BytesIO
   pdf_file.seek(0)  # Đặt con trỏ về đầu file
   with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
     count = 1
     for page in doc:
         text += f"\n\n============================== PAGE {count}: =============================\n" + page.get_text()
         count += 1
   print("PDF CONTENT: \n")
   return text

# Streamlit UI
st.title("Crawl và Generate Content")
links_input = st.text_area("Nhập các link (mỗi link trên một dòng, sử dụng nút enter để xuống dòng):")
project_name = st.text_area("Nhập tên dự án:")
pdf_file = st.file_uploader("Tải lên file PDF:", type=["pdf"])  # Thêm uploader cho file PDF

if st.button("Generate"):
    links = links_input.splitlines()
    raw_content = get_context(links)
    if pdf_file:
        pdf_content = extract_text_from_pdf(pdf_file)
        raw_content += f"\n\n{pdf_content}"
    try:
      for page in search( "website" + " of " + project_name, num =1, start=0, stop=1):
          website = page
          break
      for page in search( "twitter" + " of " + project_name, num =1, start=0, stop=1):
          twitter = page
          break
      community = f"""[Website]({website})
      
  [Twitter]({twitter})"""
    except:
      for page in search( "website" + " of " + project_name + " in web3", num_results =1):
        website = page
        break
      for page in search( "twitter" + " of " + project_name + " in web3", num_results =1):
          twitter = page
          break
      community = f"""[Website]({website})
    
[Twitter]({twitter})"""
    # Generate content using the model
    blog = model_gemini.generate_content(prompt.format(content = raw_content))
    
    # Display the generated content in Markdown
    with st.spinner("Generating content..."):
      generated_content = blog.candidates[0].content.parts[0].text.strip()
      a = ast.literal_eval(blog.candidates[0].content.parts[0].text.strip().strip("\n"))
      final_blog = f"# {a['title']} \n {a['content']} \n\n## Cộng đồng: \n\n{community}"
      print(final_blog)
      st.markdown(final_blog)

    # Prepare Markdown for download
    markdown_buffer = io.BytesIO()
    markdown_buffer.write(final_blog.encode())
    markdown_buffer.seek(0)

    # Button to download Markdown
    st.download_button("Tải xuống", markdown_buffer, file_name="generated_content.txt", mime="text/plain")
