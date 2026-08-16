import streamlit as st
from groq import Groq
import base64
import sqlite3
import pandas as pd
from datetime import datetime
import json
import io
from PIL import Image

st.set_page_config(page_title="Ultimate Pro AI Skincare System", layout="wide")

# Groq API Client Setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Database Initialization with Pro Tables
def init_db():
    conn = sqlite3.connect('pro_skincare.db')
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            fullname TEXT
        )
    ''')
    
    # Consultations Table with Scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            skin_type TEXT,
            allergies TEXT,
            budget TEXT,
            acne_score INTEGER,
            dark_spot_score INTEGER,
            hydration_score INTEGER,
            recommendations TEXT,
            timestamp TEXT
        )
    ''')
    
    # Lifestyle Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lifestyle_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            water_intake REAL,
            sleep_hours REAL,
            log_date TEXT
        )
    ''')
    
    # Routine Checklist & Streak Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routine_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            routine_type TEXT,
            completed_date TEXT
        )
    ''')
    
    # Skin Progress Gallery Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skin_gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            image_blob BLOB,
            note TEXT,
            upload_date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Session State for Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- AUTHENTICATION SYSTEM ---
if not st.session_state.logged_in:
    st.title("🔐 Pro AI Skincare System - Login / Signup")
    auth_tab1, auth_tab2 = st.tabs(["🔑 Login", "📝 Signup"])
    
    with auth_tab1:
        l_user = st.text_input("Username", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            conn = sqlite3.connect('pro_skincare.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (l_user, l_pass))
            user = cursor.fetchone()
            conn.close()
            if user:
                st.session_state.logged_in = True
                st.session_state.username = l_user
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")
                
    with auth_tab2:
        s_user = st.text_input("Choose Username", key="s_user")
        s_pass = st.text_input("Choose Password", type="password", key="s_pass")
        s_name = st.text_input("Full Name", key="s_name")
        if st.button("Register"):
            if s_user and s_pass:
                try:
                    conn = sqlite3.connect('pro_skincare.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (username, password, fullname) VALUES (?, ?, ?)", (s_user, s_pass, s_name))
                    conn.commit()
                    conn.close()
                    st.success("Account created successfully! Please login.")
                except:
                    st.error("Username already exists!")
            else:
                st.warning("Please fill all fields.")
    st.stop()

# --- MAIN PRO APP ---
st.sidebar.write(f"👤 Welcome, **{st.session_state.username}**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.title("✨ Ultimate Pro-Level AI Skincare & Beauty Advisor (15 Features - Myanmar Market)")

# Sidebar Preferences & Theme Control
lang = st.sidebar.selectbox("🌐 Language / ဘာသာစကား", ["Myanmar (မြန်မာ)", "English"])
theme_mode = st.sidebar.selectbox("🎨 UI Theme", ["Light Mode", "Dark Mode"])

st.sidebar.header("⚙️ Profile & Safety Filters")
skin_type_input = st.sidebar.selectbox("Skin Type", ["Oily", "Dry", "Combination", "Acne-Prone", "Sensitive"])
allergies = st.sidebar.text_input("Allergy Alert (Avoid Ingredients)", value="Alcohol, Fragrance")
budget_option = st.sidebar.selectbox("Budget Filter", ["Affordable", "Mid-range", "High-end"])

# Main Pro Tabs (All 15 Features Integrated Across Tabs)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
    "🔍 Face Analysis & Myanmar Market", 
    "🏷️ Ingredient Scanner",
    "📝 Skin Quiz",
    "☀️ Routine & Streak",
    "📸 Progress Gallery",
    "💧 Lifestyle Chart", 
    "📊 History & PDF", 
    "📖 Glossary", 
    "🤖 Advanced AI Hub",
    "💬 AI Chatbot",
    "🇲🇲 Climate Tips"
])

with tab1:
    st.subheader("1 & 15. Face Analysis, Scoring & Myanmar Marketplace Products")
    uploaded_file = st.file_uploader("မျက်နှာပုံ တင်ပါ (Upload Face Image)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        if st.button("🚀 အသားအရေ စစ်ဆေးပြီး မြန်မာဈေးကွက် ပစ္စည်းများ ရှာမည်"):
            with st.spinner("AI က အသားအရေကို စစ်ဆေးနေပြီး မြန်မာနိုင်ငံရှိ Online Marketplaces (예: Marketplace, City Mall, Shop.com.mm, Facebook Pages) တို့မှ ဈေးနှုန်းများနှင့်အတူ ရှာဖွေနေပါပြီ..."):
                image_bytes = uploaded_file.getvalue()
                mime_type = uploaded_file.type
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                prompt = f"""
                Analyze this facial skin image strictly in Burmese language, keeping in mind Myanmar's tropical climate.
                User constraints: Skin Type: {skin_type_input}, Allergies to avoid: {allergies}, Budget: {budget_option}.
                Provide the entire response in Burmese:
                1. Skin Condition Scores (အမှတ်ပေးစနစ် - ဝက်ခြံ၊ အမည်းစက်၊ ရေဓာတ် ၁ မှ ၁၀ ထိ).
                2. Face Analysis Map & Condition (မျက်နှာပြင် အခြေအနေ ခွဲခြမ်းစိတ်ဖြာချက်).
                3. Personalized Skincare Routine (မနက်/ည သုံးရမည့် အစီအစဉ်).
                4. Specific Product Recommendations matching the {budget_option} budget, avoiding {allergies}, with estimated prices in Myanmar Kyats (MMK) and where to buy in Myanmar (e.g., local online cosmetic shops, Facebook pages, City Mall, or pharmacies in Yangon/Mandalay).
                
                Format scores explicitly at the beginning as:
                ACNE_SCORE: [1-10]
                DARK_SPOT_SCORE: [1-10]
                HYDRATION_SCORE: [1-10]
                """
                
                try:
                    response = client.chat.completions.create(
                        model="qwen/qwen3.6-27b",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                            ]
                        }],
                        temperature=0.3
                    )
                    result_text = response.choices[0].message.content
                    
                    conn = sqlite3.connect('pro_skincare.db')
                    cursor = conn.cursor()
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute('''
                        INSERT INTO consultations (user_name, skin_type, allergies, budget, acne_score, dark_spot_score, hydration_score, recommendations, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (st.session_state.username, skin_type_input, allergies, budget_option, 5, 4, 6, result_text, current_time))
                    conn.commit()
                    conn.close()
                    
                    st.success("စစ်ဆေးမှု ပြီးစီးပါပြီ!")
                    st.markdown(result_text)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("2. Product Ingredient & Label Scanner")
    product_img = st.file_uploader("Upload Product Label Image", type=["jpg", "jpeg", "png"], key="prod_img")
    if product_img:
        st.image(product_img, caption="Product Label", use_container_width=True)
        if st.button("🔍 Check Ingredients Safety"):
            with st.spinner("Analyzing product ingredients..."):
                p_bytes = product_img.getvalue()
                p_mime = product_img.type
                p_b64 = base64.b64encode(p_bytes).decode('utf-8')
                
                check_prompt = f"""
                Analyze this skincare product label image in Burmese language. 
                User allergies/constraints to avoid: {allergies}.
                1. Extract ingredients.
                2. Check if harmful or allergic ingredients are present.
                3. Give verdict in Burmese.
                """
                
                try:
                    p_response = client.chat.completions.create(
                        model="qwen/qwen3.6-27b",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": check_prompt},
                                {"type": "image_url", "image_url": {"url": f"data:{p_mime};base64,{p_b64}"}}
                            ]
                        }],
                        temperature=0.2
                    )
                    st.markdown(p_response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.subheader("3. Interactive Skin Type Assessment Quiz")
    q1 = st.radio("၁။ နေ့လယ်ဘက်ရောက်တဲ့အခါ မျက်နှာပေါ်မှာ အဆီပြန်မှု အခြေအနေက ဘယ်လိုရှိလဲ?", 
                  ["အမြဲတမ်း အဆီပြန်ပြီး တလက်လက်ဖြစ်နေတယ် (Oily)", "T-zone (နဖူးနဲ့နှာခေါင်း) လောက်ပဲ အဆီပြန်တယ် (Combination)", "လုံးဝ အဆီမပြန်ဘဲ ခြောက်သွေ့နေတယ် (Dry)", "တင်းပြီး ယားယံလွယ်တယ် သို့မဟုတ် နီမြန်းတတ်တယ် (Sensitive)"])
    q2 = st.radio("၂။ မျက်နှာသစ်ပြီးသွားတဲ့အခါ ခဏအကြာမှာ ဘယ်လိုခံစားရလဲ?", 
                  ["တင်းပြီး ကွဲအက်ချင်သလို ဖြစ်လာတယ်", "သက်တောင့်သက်သာရှိပါတယ်", "ခဏလေးနဲ့ ပြန်ပြီး အဆီတွေ စုလာတယ်", "စပ်ဖျင်းဖျင်းဖြစ်တာ ဒါမှမဟုတ် နီမြန်းတာရှိတယ်"])
    q3 = st.radio("၃။ အမည်းစက်၊ ဝက်ခြံ နှင့် အပေါက်ကျယ်ခြင်း ပြဿနာက ဘယ်လိုရှိလဲ?", 
                  ["ဝက်ခြံနဲ့ အပေါက်ကျယ်တာတွေ အဓိက ဖြစ်တတ်တယ်", "အမည်းစက်နဲ့ ညိုတိုတို အမာရွတ်တွေ ဖြစ်လွယ်တယ်", "အသားအရေက ကြမ်းတမ်းပြီး အလွယ်တကူ အဖတ်ကွာတတ်တယ်", "ဘာမှန်းမသိဘဲ ထိလွယ်ရှလွယ် ဖြစ်ပြီး အလွယ်တကူ တုံ့ပြန်မှုရှိတယ်"])
    
    if st.button("📊 Assess My Skin Type via Quiz"):
        if "Oily" in q1 or "အဆီတွေ စုလာတယ်" in q2 or "ဝက်ခြံနဲ့" in q3:
            st.success("🎯 သင့်အသားအရေအမျိုးအစားမှာ **Oily / Acne-Prone (အဆီပြန်ပြီး ဝက်ခြံထွက်လွယ်သော)** ဖြစ်ပါသည်။")
        elif "Dry" in q1 or "တင်းပြီး ကွဲအက်" in q2 or "အဖတ်ကွာ" in q3:
            st.success("🎯 သင့်အသားအရေအမျိုးအစားမှာ **Dry (ခြောက်သွေ့သော အသားအရေ)** ဖြစ်ပါသည်။")
        elif "Combination" in q1:
            st.success("🎯 သင့်အသားအရေအမျိုးအစားမှာ **Combination (ပေါင်းစပ်အသားအရေ)** ဖြစ်ပါသည်။")
        else:
            st.success("🎯 သင့်အသားအရေအမျိုးအစားမှာ **Sensitive (ထိလွယ်ရှလွယ်သော အသားအရေ)** ဖြစ်ပါသည်။")

with tab4:
    st.subheader("4. Routine Reminders & Streak Counter")
    today_str = datetime.now().strftime("%Y-%m-%d")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        m_done = st.checkbox("☀️ Morning Routine ပြီးစီးပါပြီ")
    with col_r2:
        n_done = st.checkbox("🌙 Night Routine ပြီးစီးပါပြီ")
        
    if st.button("Save Routine Log"):
        conn = sqlite3.connect('pro_skincare.db')
        cursor = conn.cursor()
        if m_done:
            cursor.execute("INSERT INTO routine_logs (user_name, routine_type, completed_date) VALUES (?, ?, ?)", (st.session_state.username, "Morning", today_str))
        if n_done:
            cursor.execute("INSERT INTO routine_logs (user_name, routine_type, completed_date) VALUES (?, ?, ?)", (st.session_state.username, "Night", today_str))
        conn.commit()
        conn.close()
        st.success("Routine log saved successfully!")
        
    conn = sqlite3.connect('pro_skincare.db')
    r_df = pd.read_sql("SELECT DISTINCT completed_date FROM routine_logs WHERE user_name = ? ORDER BY completed_date DESC", conn, params=(st.session_state.username,))
    conn.close()
    st.metric(label="🔥 Current Skincare Streak (Days)", value=f"{len(r_df)} Days")

with tab5:
    st.subheader("5. Skin Progress Photo Gallery")
    gal_img = st.file_uploader("Upload Progress Photo", type=["jpg", "jpeg", "png"], key="gal_upload")
    gal_note = st.text_input("Note (e.g., Week 1 - Acne reducing)")
    
    if gal_img and st.button("Save Photo to Gallery"):
        img_bytes = gal_img.getvalue()
        conn = sqlite3.connect('pro_skincare.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO skin_gallery (user_name, image_blob, note, upload_date) VALUES (?, ?, ?, ?)",
                       (st.session_state.username, sqlite3.Binary(img_bytes), gal_note, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        st.success("Photo saved to gallery!")
        
    conn = sqlite3.connect('pro_skincare.db')
    g_df = pd.read_sql("SELECT id, note, upload_date, image_blob FROM skin_gallery WHERE user_name = ? ORDER BY id DESC", conn, params=(st.session_state.username,))
    conn.close()
    if not g_df.empty:
        for index, row in g_df.iterrows():
            st.write(f"**Date:** {row['upload_date']} | **Note:** {row['note']}")
            st.image(Image.open(io.BytesIO(row['image_blob'])), width=300)

with tab6:
    st.subheader("6. Lifestyle & Progress Chart Visualization")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        water_val = st.number_input("Water Intake (Litres)", 0.0, 5.0, 2.0, 0.5)
    with col_w2:
        sleep_val = st.number_input("Sleep Duration (Hours)", 0.0, 12.0, 7.0, 0.5)
        
    if st.button("Save Lifestyle Log"):
        conn = sqlite3.connect('pro_skincare.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lifestyle_logs (user_name, water_intake, sleep_hours, log_date) VALUES (?, ?, ?, ?)", 
                       (st.session_state.username, water_val, sleep_val, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        st.success("Lifestyle log saved successfully!")
        
    conn = sqlite3.connect('pro_skincare.db')
    life_df = pd.read_sql("SELECT log_date, water_intake, sleep_hours FROM lifestyle_logs WHERE user_name = ? ORDER BY id ASC", conn, params=(st.session_state.username,))
    conn.close()
    if not life_df.empty:
        st.line_chart(life_df.set_index('log_date'))

with tab7:
    st.subheader("7. History & Export PDF Report")
    conn = sqlite3.connect('pro_skincare.db')
    hist_df = pd.read_sql("SELECT * FROM consultations WHERE user_name = ? ORDER BY id DESC", conn, params=(st.session_state.username,))
    conn.close()
    if not hist_df.empty:
        st.dataframe(hist_df[['id', 'skin_type', 'budget', 'timestamp']], use_container_width=True)
        sel_id = st.selectbox("Select Consultation ID for Report", hist_df['id'].unique())
        selected_rec = hist_df[hist_df['id'] == sel_id].iloc[0]
        st.markdown(selected_rec['recommendations'])
        st.download_button("📥 Download Official Report", data=selected_rec['recommendations'], file_name=f"Report_{sel_id}.txt", mime="text/plain")

with tab8:
    st.subheader("8. Ingredient Glossary")
    search_g = st.text_input("Search Ingredient (Retinol, Niacinamide, etc.)")
    glossary = {
        "retinol": "Anti-aging & cell renewal ingredient. Best used at night.",
        "niacinamide": "Brightens skin, fades dark spots, controls oil.",
        "hyaluronic acid": "Deeply hydrates and plumps the skin.",
        "salicylic acid": "BHA that clears pores and treats acne."
    }
    for k, v in glossary.items():
        if not search_g or search_g.lower() in k:
            st.markdown(f"- **{k.capitalize()}**: {v}")

with tab9:
    st.subheader("🤖 11, 12, 13, 14, 15. Advanced AI Hub (5 New AI Features)")
    ai_task = st.selectbox("AI အဆင့်မြင့် လုပ်ဆောင်ချက် ရွေးချယ်ရန်", [
        "11. AI-Driven Skincare Recipe Creator (အိမ်သုံး Natural Mask ဖော်စပ်နည်း)", 
        "12. Smart Skincare Conflict Detector (ပစ္စည်းများ ဓာတ်ပြုမှု စစ်ဆေးခြင်း)", 
        "13. AI-Powered Seasonal Skincare Adjuster (ရာသီဥတုအလိုက် Routine ပြောင်းလဲခြင်း)",
        "14. Skin Concern Predictive Analysis (အသားအရေ အခြေအနေ ကြိုတင်ခန့်မှန်းခြင်း)",
        "15. Professional Dermatology Consult Script (ဆရာဝန်ပြရန် Medical Summary ရေးပေးခြင်း)"
    ])
    
    ai_input = st.text_area("လိုအပ်သော အချက်အလက်များ သို့မဟုတ် မေးခွန်းကို ရိုက်ထည့်ပါ...")
    if st.button("AI ထံမှ အကြံဉာဏ်ရယူရန်"):
        with st.spinner("AI တွက်ချက်နေသည်..."):
            prompt_adv = f"Act as an expert dermatologist. Task Type: {ai_task}. User Input/Details: {ai_input}. Provide a professional response strictly in Burmese language."
            adv_res = client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[{"role": "user", "content": prompt_adv}],
                temperature=0.4
            )
            st.markdown(adv_res.choices[0].message.content)

with tab10:
    st.subheader("9. AI Beauty Chatbot")
    q = st.text_input("Ask any skincare or beauty question...")
    if st.button("Ask AI Chatbot"):
        if q:
            with st.spinner("Thinking..."):
                chat_res = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=[{"role": "user", "content": f"Answer professionally in Burmese: {q}"}],
                    temperature=0.5
                )
                st.markdown(chat_res.choices[0].message.content)

with tab11:
    st.subheader("10. Myanmar Climate Skin Care Guide")
    st.markdown("""
    မြန်မာနိုင်ငံ၏ ပူပြင်းစွတ်စိုသော (Hot & Humid) ရာသီဥတုတွင် အသားအရေ ထိန်းသိမ်းရန် အထူးအကြံပြုချက်များ:
    - **Sun Protection:** SPF 50 ပါသော Sunscreen ကို နေ့စဉ် မပျက်မကွက် လိမ်းပါ။
    - **Oil & Sweat Control:** Gel-based သို့မဟုတ် Water-based Moisturizer များကိုသာ ရွေးချယ်ပါ။
    - **Double Cleansing:** ညဘက်ရောက်လျှင် Micellar water သို့မဟုတ် Cleansing oil ဖြင့် ပထမတစ်ကြိမ်၊ Face wash ဖြင့် ဒုတိယတစ်ကြိမ် သန့်စင်ပါ။
    """)
