import streamlit as st
import ollama
from PIL import Image
import io
import base64

st.set_page_config(
   page_title="Gemma-3 OCR",
   page_icon="🔎",
   layout="wide",
   initial_sidebar_state="expanded"
)

st.title("AI Document OCR")


col1, col2 = st.columns([6,1])
with col2:
   if st.button("Clear 🗑️"):
       if 'ocr_result' in st.session_state:
           del st.session_state['ocr_result']
       st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Gemma-3 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
   st.header("Upload Image")
   uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
  
   if uploaded_file is not None:
       image = Image.open(uploaded_file)
       st.image(image, caption="Uploaded Image")
      
       if st.button("Extract Text 🔍", type="primary"):
           with st.spinner("Processing image..."):
               try:
                   response = ollama.chat(
                       model= 'gemma3:4b',
                       messages=[{
                           'role': 'user',
                           'content': """You are an expert in Optical Character Recognition (OCR) and document analysis.

Carefully examine the image provided and extract **all visible and legible textual content**, ensuring no detail is missed — including headers, subheaders, tables, footnotes, watermarks, annotations, and small print.

Present the extracted information in a **structured and professional Markdown format**, using appropriate elements such as:

- `#` for main headings  
- `##` for subheadings  
- Bullet points or numbered lists for items  
- Tables where applicable  
- Code blocks for monospaced or technical text  
- Blockquotes if the image contains quotes or cited content

Also, maintain the **visual hierarchy and logical flow** as seen in the original layout. If any text is partially obscured or uncertain, mark it with `[UNCLEAR]`.

Your goal is to make the output as close as possible to a human-crafted, structured transcription that can be reused in digital documents or applications.

Now analyze the following image thoroughly and return the structured Markdown output""",
                           'images': [uploaded_file.getvalue()]
                       }]
                   )
                   st.session_state['ocr_result'] = response.message.content
               except Exception as e:
                   st.error(f"Error processing image: {str(e)}")

if 'ocr_result' in st.session_state:
   st.markdown(st.session_state['ocr_result'])
else:
   st.info("Upload an image and click 'Extract Text' to see the results here.")

st.markdown("---")
st.markdown("Made using Gemma-3 Vision Model")
