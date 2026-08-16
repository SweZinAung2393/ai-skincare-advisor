import streamlit as st
import base64
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Skincare Advisor", layout="centered")

# Initialize Groq Client securely from Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("၁။ မျက်နှာအသားအရေ စစ်ဆေးမှု (မြန်မာဘာသာ သက်သက်)")

# Image Upload
uploaded_file = st.file_uploader("မျက်နှာပုံ တင်ပါ", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="တင်ထားသော ပုံ", use_column_width=True)
    
    if st.button("စစ်ဆေးမှု ပြီးစီးပါပြီ"):
        with st.spinner("အသားအရေကို စစ်ဆေးနေပါပြီ... ကျေးဇူးပြု၍ ခဏစောင့်ပါ..."):
            try:
                # Convert image to base64
                image_bytes = uploaded_file.getvalue()
                base64_image = base64.b64encode(image_bytes).decode("utf-8")
                
                # API Call using the updated vision model
                chat_completion = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "ဒီမျက်နှာပုံကို အခြေခံပြီး အသားအရေ အခြေအနေကို မြန်မာဘာသာဖြင့် အသေးစိတ် သုံးသပ်ပေးပါ။"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.4,
                    max_tokens=1024
                )
                
                # Display Result
                st.success("စစ်ဆေးမှု ပြီးဆုံးပါပြီ!")
                st.markdown(chat_completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"အမှားအယွင်း ဖြစ်ပေါ်နေပါသည်: {e}")
else:
    st.info("ကျေးဇူးပြု၍ မျက်နှာပုံ တင်ပေးပါ။")
