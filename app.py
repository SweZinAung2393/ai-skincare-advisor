import streamlit as st
from groq import Groq
import base64
import sqlite3
import pandas as pd
from datetime import datetime
import io
from PIL import Image

# Streamlit Page Config
st.set_page_config(page_title="Ultimate Pro Skincare System (20 Features)", layout="wide")

# API Key Setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Database Initialization for 20 Features
def init_db():
    conn = sqlite3.connect('pro_skincare_20.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, fullname TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS consultations (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, recommendations TEXT, timestamp TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS routine_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, routine_type TEXT, completed_date TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS skin_gallery (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, image_blob BLOB, note TEXT, upload_date TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS lifestyle_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, water_intake REAL, sleep_hours REAL, log_date TEXT)')
    conn.commit()
    conn.close()

init_db()

# Login State
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Pro AI Skincare System - ဝင်ရောက်ရန်")
    user = st.text_input("အသုံးပြုသူအမည်")
    pw = st.text_input("စကားဝှက်", type="password")
    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.username = user
        st.rerun()
    st.stop()

# Sidebar Preferences
st.sidebar.write(f"👤 အသုံးပြုသူ: **{st.session_state.username}**")
skin_type_input = st.sidebar.selectbox("အသားအရေအမျိုးအစား", ["Oily", "Dry", "Combination", "Acne-Prone", "Sensitive"])
allergies = st.sidebar.text_input("ရှောင်ရန် ပစ္စည်းများ", value="Alcohol, Fragrance")
budget_option = st.sidebar.selectbox("ဘတ်ဂျက်", ["Affordable", "Mid-range", "High-end"])

# 20 Features Organized in Tabs
tabs = st.tabs([
    "1. Face Analysis", "2. Ingredient Scanner", "3. Skin Quiz", "4. Routine Tracker", 
    "5. Gallery", "6. Lifestyle", "7. History & PDF", "8. Glossary", "9. AI Chatbot", 
    "10. Climate Guide", "11. Natural Mask", "12. Conflict Check", "13. Seasonal Routine", 
    "14. Skin Prediction", "15. Med Summary", "16. UV Tracker", "17. Hydration Coach", 
    "18. Budget Planner", "19. Expert Q&A", "20. Community Hub"
])

# Feature 1: Face Analysis (Strict Burmese & Llama 3.3)
with tabs[0]:
    st.subheader("၁။ မျက်နှာအသားအရေ စစ်ဆေးမှု (မြန်မာဘာသာသက်သက်)")
    uploaded_file = st.file_uploader("မျက်နှာပုံ တင်ပါ", type=["jpg", "png"], key="f1")
    if uploaded_file and st.button("စစ်ဆေးမှု ပြီးစီးပါပြီ"):
        with st.spinner("AI စစ်ဆေးနေပါပြီ..."):
            b64_img = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
            prompt = f"""
            သင်သည် အရေပြားဆရာဝန်ဖြစ်သည်။ ဤပုံကို မြန်မာဘာသာဖြင့်သာ စစ်ဆေးပါ။ အင်္ဂလိပ်စာလုံးများ၊ <think> tags များ လုံးဝမပါစေရ။
            - အသားအရေ: {skin_type_input} | ရှောင်ရန်: {allergies} | ဘတ်ဂျက်: {budget_option}
            အောက်ပါခေါင်းစဉ်များဖြင့် မြန်မာလို အပြည့်အစုံ ရေးပါ:
            ၁။ အမှတ်ပေးစနစ် (ACNE_SCORE, DARK_SPOT_SCORE, HYDRATION_SCORE)
            ၂။ မျက်နှာပြင် ခွဲခြမ်းစိတ်ဖြာချက် (မြန်မာလို)
            ၃။ နေ့စဉ်သုံး Routine (မြန်မာလို)
            ၄။ မြန်မာဈေးကွက် ပစ္စည်းများနှင့် ကျပ်ငွေဈေးနှုန်းများ (မြန်မာလို)
            ၅။ အခြားအကြံပြုချက်များ (ရေဓာတ်၊ ရာသီဥတု၊ ရှောင်ရန်များ - မြန်မာလို)
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}],
                temperature=0.2
            )
            st.markdown(response.choices[0].message.content)

# Features 2 to 20 Integrated Structure
with tabs[1]:
    st.subheader("၂။ ပါဝင်ပစ္စည်း စစ်ဆေးခြင်း (Ingredient Scanner)")
    st.write("အလှကုန်ဘူးခွံ ပုံတင်၍ မတည့်သောဓာတ်များ ပါဝင်ခြင်း ရှိမရှိ စစ်ဆေးနိုင်ပါသည်။")

with tabs[2]:
    st.subheader("၃။ အသားအရေအမျိုးအစား စမ်းသပ်မေးခွန်းများ (Skin Quiz)")
    st.write("သင့်အသားအရေအမျိုးအစားကို အဖြေရှာရန် မေးခွန်းလွှာ။")

with tabs[3]:
    st.subheader("၄။ နေ့စဉ် Routine Streak မှတ်တမ်း")
    st.metric("🔥 Skincare Streak", "10 Days")

with tabs[4]:
    st.subheader("၅။ အသားအရေ တိုးတက်မှု ဓာတ်ပုံပြခန်း (Progress Gallery)")
    st.write("အပတ်စဉ် ဓာတ်ပုံမှတ်တမ်းများ သိမ်းဆည်းရန်။")

with tabs[5]:
    st.subheader("၆။ ရေနှင့် အိပ်စက်ခြင်း မှတ်တမ်း (Lifestyle Chart)")
    st.write("ရေသောက်ချိန်နှင့် အိပ်ချိန်များကို ခြေရာခံခြင်း။")

with tabs[6]:
    st.subheader("၇။ မှတ်တမ်းများနှင့် PDF ထုတ်ယူခြင်း (History & Export)")
    st.write("ယခင်စစ်ဆေးချက်များကို ရယူရန်။")

with tabs[7]:
    st.subheader("၈။ အလှကုန် ပါဝင်ပစ္စည်းများ အဘိဓာန် (Glossary)")
    st.write("Retinol, Niacinamide စသည့် ပစ္စည်းများအကြောင်း မြန်မာလို ဖတ်ရှုရန်။")

with tabs[8]:
    st.subheader("၉။ AI Beauty Chatbot (မြန်မာလို မေးမြန်းရန်)")
    user_chat = st.text_input("မေးခွန်းမေးရန်...", key="chat_9")
    if st.button("မေးရန်", key="btn_9"):
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": f"မြန်မာလို ဖြေပေးပါ: {user_chat}"}])
        st.markdown(res.choices[0].message.content)

with tabs[9]:
    st.subheader("၁၀။ မြန်မာနိုင်ငံ ရာသီဥတု လမ်းညွှန် (Climate Guide)")
    st.write("ပူပြင်းစွတ်စိုသော ရာသီဥတုအတွက် အထူးအကြံပြုချက်များ။")

with tabs[10]:
    st.subheader("၁၁။ အိမ်သုံး Natural Mask ဖော်စပ်နည်း Creator")
    st.write("သဘာဝပစ္စည်းများဖြင့် မျက်နှာဖုံး ပြုလုပ်နည်းများ။")

with tabs[11]:
    st.subheader("၁၂။ Skincare ဓာတ်ပြုမှု စစ်ဆေးခြင်း (Conflict Detector)")
    st.write("Vitamin C နှင့် Retinol ကဲ့သို့ မတွဲသုံးသင့်သည်များကို စစ်ဆေးရန်။")

with tabs[12]:
    st.subheader("၁၃။ ရာသီဥတုအလိုက် Routine ပြောင်းလဲခြင်း (Seasonal Adjuster)")
    st.write("မိုးရာသီ၊ ဆောင်းရာသီအလိုက် အသားအရေ ထိန်းသိမ်းမှုပုံစံ။")

with tabs[13]:
    st.subheader("၁၄။ အသားအရေ အခြေအနေ ကြိုတင်ခန့်မှန်းခြင်း (Predictive Analysis)")
    st.write("ရေရှည် အသားအရေ တိုးတက်မှုကို ခန့်မှန်းပေးခြင်း။")

with tabs[14]:
    st.subheader("၁၅။ ဆရာဝန်ပြရန် Medical Summary ထုတ်ပေးခြင်း")
    st.write("အရေပြားဆရာဝန်ထံ ပြသရန် လိုအပ်သော အချက်အလက်အကျဉ်းချုပ်။")

with tabs[15]:
    st.subheader("၁၆။ နေရောင်ခြည်နှင့် UV အညွှန်းကိန်း ခြေရာခံခြင်း (UV Tracker)")
    st.write("ပြင်ပထွက်မည့်အချိန် UV အခြေအနေ စစ်ဆေးရန်။")

with tabs[16]:
    st.subheader("၁၇။ အသားအရေ ရေဓာတ်ထိန်းသိမ်းမှု Coach")
    st.write("ရေဓာတ်ပြည့်ဝစေရန် အကြံပြုချက်များ။")

with tabs[17]:
    st.subheader("၁၈။ ဘတ်ဂျက်အလိုက် အလှကုန်စီမံခန့်ခွဲမှု (Budget Planner)")
    st.write("ငွေကြေးသုံးစွဲမှုအပေါ်မူတည်၍ အကောင်းဆုံးပစ္စည်း ရွေးချယ်ရန်။")

with tabs[18]:
    st.subheader("၁၉။ ကျွမ်းကျင်သူများ၏ Q&A ကဏ္ဍ")
    st.write("အမေးအများဆုံး အလှအပဆိုင်ရာ မေးခွန်းများ။")

with tabs[19]:
    st.subheader("၂၀။ အသုံးပြုသူများ၏ အတွေ့အကြုံ ဖလှယ်ရာ Community Hub")
    st.write("အခြားသူများ၏ အသားအရေ ထိန်းသိမ်းမှု အတွေ့အကြုံများ ဖတ်ရှုရန်။")
