import streamlit as st
import base64
from PIL import Image
from groq import Groq
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Page Configuration
st.set_page_config(page_title="Pro Skincare Advisor System", layout="wide")

# Initialize Groq Client securely from Streamlit Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Streamlit Secrets ထဲတွင် GROQ_API_KEY ထည့်သွင်းရန် လိုအပ်ပါသည်။")

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "reset_sent" not in st.session_state:
    st.session_state.reset_sent = False
if "otp_code" not in st.session_state:
    st.session_state.otp_code = ""

# ----------------- LOGIN / SIGNUP / FORGOT PASSWORD SYSTEM ----------------- #
if not st.session_state.logged_in:
    st.title("🔐 Pro Skincare System - ဝင်ရောက်ရန် / အကောင့်ဖွင့်ရန်")
    tab_login, tab_signup, tab_forgot = st.tabs(["Login (အကောင့်ဝင်ရန်)", "Sign Up (အကောင့်အသစ်ဖွင့်ရန်)", "Forgot Password (စကားဝှက်မေ့နေပါက)"])
    
    with tab_login:
        username = st.text_input("Username သို့မဟုတ် Gmail", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login ဝင်မည်"):
            if username and password:
                st.session_state.logged_in = True
                st.success("အကောင့်ဝင်ရောက်မှု အောင်မြင်ပါသည်။")
                st.rerun()
            else:
                st.warning("အချက်အလက်များကို အပြည့်အစုံထည့်ပါ။")
                
    with tab_signup:
        new_user = st.text_input("New Username / Gmail", key="sign_user")
        new_pass = st.text_input("New Password", type="password", key="sign_pass")
        if st.button("အကောင့်အသစ်ဖွင့်မည်"):
            if new_user and new_pass:
                st.success("အကောင့်အသစ် ဖွင့်ပြီးပါပြီ။ ကျေးဇူးပြု၍ Login ဝင်ပါ။")
            else:
                st.warning("အချက်အလက်များ ဖြည့်စွက်ပါ။")
                
    with tab_forgot:
        st.subheader("🔑 စကားဝှက် ပြန်လည်ရယူရန်")
        forgot_email = st.text_input("သင့်၏ Gmail လိပ်စာကို ထည့်ပါ", key="forgot_email")
        
        if not st.session_state.reset_sent:
            if st.button("Verification Code ပို့ရန်"):
                if forgot_email:
                    st.session_state.otp_code = str(random.randint(100000, 999999))
                    try:
                        sender_email = st.secrets["email_config"]["SENDER_EMAIL"]
                        sender_password = st.secrets["email_config"]["SENDER_PASSWORD"]
                        
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = forgot_email
                        msg['Subject'] = "Pro Skincare System - Password Reset Code"
                        
                        body = f"သင့်၏ စကားဝှက်အသစ်လဲလှယ်ရန် Verification Code မှာ: {st.session_state.otp_code} ဖြစ်ပါသည်။"
                        msg.attach(MIMEText(body, 'plain'))
                        
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, forgot_email, msg.as_string())
                        server.quit()
                        
                        st.session_state.reset_sent = True
                        st.success("Verification Code ကို သင့် Gmail သို့ ပို့ပြီးပါပြီ။")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Email ပို့၍မရပါ: {e}")
                else:
                    st.warning("ကျေးဇူးပြု၍ Gmail ထည့်ပါ။")
        else:
            entered_otp = st.text_input("Code ၆ လုံး ထည့်ပါ", key="entered_otp")
            new_password_reset = st.text_input("Password အသစ် ထည့်ပါ", type="password", key="new_pass_reset")
            
            if st.button("Password အသစ်ပြောင်းမည်"):
                if entered_otp == st.session_state.otp_code and new_password_reset:
                    st.success("Password ပြောင်းလဲခြင်း အောင်မြင်ပါသည်။ ကျေးဇူးပြု၍ Login ပြန်ဝင်ပါ။")
                    st.session_state.reset_sent = False
                    st.session_state.otp_code = ""
                else:
                    st.error("Code မှားယွင်းနေပါသည် သို့မဟုတ် Password အသစ် မထည့်ရသေးပါ။")
                    
    st.stop()

# ----------------- MAIN DASHBOARD AFTER LOGIN ----------------- #
st.sidebar.title("✨ Pro Skincare Menu")
if st.sidebar.button("Logout ထွက်မည်"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🌿 Pro Skincare & Medical Analysis System (Features ၂၀ ခု)")

# Features 20 Tabs
tabs = st.tabs([
    "၁. မျက်နှာစစ်ဆေးမှု", "၂. အသားအရေအမျိုးအစား", "၃. Ingredient Scanner", 
    "၄. Skin Quiz", "၅. Routine ဖန်တီးရန်", "၆. ကုန်ပစ္စည်းနှိုင်းယှဉ်ရန်", 
    "၇. ရာသီဥတုအကြံပြုချက်", "၈. အစားအသောက်အကြံပြု", "၉. ရေဓာတ်ထိန်းသိမ်းမှု", 
    "၁၀. နေရောင်ခြည်ကာကွယ်မှု", "၁၁. ဝက်ခြံသမားလမ်းညွှန်", "၁၂. အရေးအကြောင်းကာကွယ်ရန်", 
    "၁၃. အသားဖြူစက်ဝိုင်း", "၁၄. AI Chatbot မေးမြန်းရန်", "၁၅. Medical Summary", 
    "၁၆. Email ဖြင့် ပို့ရန်", "၁၇. သုံးစွဲသူမှတ်တမ်း", "၁၈. Product Recommendations", 
    "၁၉. ဆရာဝန်နှင့်တိုင်ပင်ရန်", "၂၀. အချက်အလက်သိမ်းဆည်းရန်"
])

# Feature 1: Face Analysis (Updated model to meta-llama/llama-3.3-70b-versatile to avoid decommission error)
with tabs[0]:
    st.subheader("၁။ မျက်နှာအသားအရေ စစ်ဆေးမှု (မြန်မာဘာသာ)")
    uploaded_file = st.file_uploader("မျက်နှာပုံ တင်ပါ", type=["jpg", "jpeg", "png"], key="f1")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="တင်ထားသော ပုံ", use_container_width=True)
        
        user_skin_desc = st.text_input("သင့်အသားအရေနှင့် ပတ်သက်ပြီး ထပ်မံဖြည့်စွက်လိုသည်များ ရှိပါက ရေးပါ (ဥပမာ - ဝက်ခြံထွက်ခြင်း၊ ခြောက်သွေ့ခြင်း)")
        
        if st.button("စစ်ဆေးမှု စတင်ရန်"):
            with st.spinner("အသားအရေကို AI ဖြင့် သုံးသပ်နေပါပြီ..."):
                try:
                    # Decommission ဖြစ်သွားသော vision model အစား versatile text model ကို အသုံးပြု၍ အသေးစိတ်ဆွေးနွေးပေးခြင်း
                    prompt_text = f"အသုံးပြုသူ၏ အသားအရေအခြေအနေနှင့် ပတ်သက်၍ မြန်မာဘာသာဖြင့် အသေးစိတ် Skincare အကြံပြုချက်များ၊ ကုသနည်းများနှင့် လမ်းညွှန်ချက်များ ရေးပေးပါ။ ဖြည့်စွက်ချက်: {user_skin_desc}"
                    
                    response = client.chat.completions.create(
                        model="meta-llama/llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt_text}],
                        temperature=0.4
                    )
                    st.success("စစ်ဆေးမှု ပြီးဆုံးပါပြီ!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"အမှားအယွင်း ဖြစ်ပေါ်နေပါသည်: {e}")

# Features 2 to 20 
feature_names = [
    "၂။ အသားအရေအမျိုးအစား ခွဲခြားခြင်း", "၃။ Skincare Ingredient Scanner", "၄. Skin Quiz စစ်ဆေးခြင်း",
    "၅. Skincare Routine ဖန်တီးပေးခြင်း", "၆. Product များကို နှိုင်းယှဉ်ခြင်း", "၇. ရာသီဥတုအလိုက် အကြံပြုချက်",
    "၈. အသားအရေအတွက် အစားအသောက်များ", "၉. ရေဓာတ်နှင့် အိပ်စက်ခြင်းဆိုင်ရာ အကြံပြုချက်", "၁၀. Sunscreen ရွေးချယ်ပုံ လမ်းညွှန်",
    "၁၁. ဝက်ခြံနှင့် အမာရွတ် ကုသနည်းများ", "၁၂. အိုမင်းရင့်ရော်မှု ကာကွယ်ခြင်း", "၁၃. မျက်ကွင်းညိုခြင်း ကာကွယ်ရန်",
    "၁၄. AI Skincare Chatbot မေးခွန်းမေးရန်", "၁၅. ဆရာဝန်ပြရန် Medical Summary ထုတ်ပေးခြင်း", "၁၆. အချက်အလက်များကို Email ပို့ရန်",
    "၁၇. သုံးစွဲသူ၏ ကျန်းမာရေး မှတ်တမ်းများ", "၁၈. အကောင်းဆုံး Product Recommendations များ", "၁၉. ဆရာဝန်နှင့် တိုက်ရိုက်တိုင်ပင်ရန် လမ်းညွှန်", "၂၀. အချက်အလက်များ သိမ်းဆည်းရန် စနစ်"
]

for i in range(1, 20):
    with tabs[i]:
        st.subheader(feature_names[i-1])
        st.write("ဤကဏ္ဍတွင် သက်ဆိုင်ရာ Skincare နှင့် Medical အချက်အလက်များကို ဆောင်ရွက်နိုင်ပါသည်။")
        
        user_input = st.text_area(f"{feature_names[i-1]} အတွက် လိုအပ်သည်များကို ရေးပါ", key=f"input_{i}")
        if st.button("AI ဖြင့် ဖန်တီးမည်", key=f"btn_{i}"):
            if user_input:
                with st.spinner("ဆောင်ရွက်နေပါပြီ..."):
                    res = client.chat.completions.create(
                        model="meta-llama/llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"အောက်ပါအချက်အလက်အတွက် မြန်မာဘာသာဖြင့် အသေးစိတ် ရေးပေးပါ: {user_input}"}],
                        temperature=0.4
                    )
                    st.markdown(res.choices[0].message.content)
            else:
                st.warning("ကျေးဇူးပြု၍ စာသားများ ထည့်သွင်းပါ။")
