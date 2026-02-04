import streamlit as st
import google.generativeai as genai
import os

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- Custom CSS (Dark & Gold Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    .stButton>button {
        width: 100%; border-radius: 25px; height: 3em;
        background-color: #D4AF37; color: black; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #FFD700; color: black; }
    .result-card {
        background-color: #1A1C23; padding: 25px; border-radius: 15px;
        border: 1px solid #D4AF37; color: #E0E0E0; line-height: 1.8;
        margin-top: 20px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1);
        white-space: pre-wrap;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #1A1C23; border-radius: 10px 10px 0 0;
        color: white; padding: 0 15px; font-size: 14px;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- API Configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API Key မတွေ့ပါ။ Secrets မှာ GEMINI_API_KEY ထည့်ပေးပါ။")

st.markdown("<h1>🔮 မြန်မာ့ဗေဒင်နှင့် ဓာတ်ရိုက်ဓာတ်ဆင် AI</h1>", unsafe_allow_html=True)

# --- Tabs for Features ---
tab1, tab2, tab3 = st.tabs(["🌙 အိပ်မက်", "✨ ဟောစာတမ်း", "🛡️ ဓာတ်ရိုက်ဓာတ်ဆင်"])

# --- AI Personality Setup ---
# AI ကို ယောကျ်ားလေး လေသံ (ခင်ဗျာ/ကျွန်တော်) သုံးရန် ညွှန်ကြားထားသည်
system_instruction = "မင်းက မြန်မာ့ရိုးရာ ဗေဒင်ပညာရှင် ယောကျ်ားလေးတစ်ယောက်ပါ။ စကားပြောရင် 'ခင်ဗျာ' နဲ့ 'ကျွန်တော်' ကိုပဲ သုံးရပါမယ်။"

# --- Tab 1: Dream Interpreter ---
with tab1:
    st.markdown("### 🌙 အိပ်မက်နိမိတ်ဖတ်ခြင်း")
    user_dream = st.text_area("သင်မက်ခဲ့သည့် အိပ်မက်ကို ရေးပါ...", height=100)
    if st.button("နိမိတ်ဖတ်မယ်"):
        if user_dream:
            with st.spinner('ကျွန်တော် တွက်ချက်ပေးနေပါတယ် ခင်ဗျာ...'):
                prompt = f"{system_instruction} '{user_dream}' ဆိုတဲ့ အိပ်မက်ကို မြန်မာလို နိမိတ်ဖတ်ပေးပါ။ ကောင်းဆိုးနိမိတ်နဲ့ အကျိုးပေးဂဏန်းကို ယောကျ်ားလေးတစ်ယောက် လေသံနဲ့ သေချာရှင်းပြပေးပါ ခင်ဗျာ။"
                response = model.generate_content(prompt)
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)

# --- Tab 2: Daily Horoscope ---
with tab2:
    st.markdown("### ✨ နေ့စဉ်ဟောစာတမ်း")
    day = st.selectbox("သင့်မွေးနေ့ (နေ့နံ) ရွေးပါ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"])
    if st.button("ဟောစာတမ်းကြည့်မယ်"):
        with st.spinner('နက္ခတ်ကို ကြည့်ပေးနေပါတယ် ခင်ဗျာ...'):
            prompt = f"{system_instruction} {day} သားသမီးတွေအတွက် ဒီနေ့အတွက် ကံကြမ္မာကို အချစ်ရေး၊ စီးပွားရေး၊ ကျန်းမာရေး ခွဲပြီး ဟောပေးပါ။ ယောကျ်ားလေး လေသံနဲ့ 'ခင်ဗျာ' သုံးပြီး ဟောပေးပါ ခင်ဗျာ။"
            response = model.generate_content(prompt)
            st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)

# --- Tab 3: Yadaya (ဓာတ်ရိုက်ဓာတ်ဆင်) ---
with tab3:
    st.markdown("### 🛡️ အမည်နှင့် ဓာတ်ရိုက်ဓာတ်ဆင်")
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("သင့်အမည်")
    with col2:
        problem = st.selectbox("ရင်ဆိုင်နေရသော အခက်အခဲ", ["စီးပွားရေးညံ့ခြင်း", "အချစ်ရေးအဆင်မပြေခြင်း", "ကျန်းမာရေးမကောင်းခြင်း", "အတိုက်အခံများခြင်း", "အလုပ်အကိုင်ခက်ခဲခြင်း"])
    
    if st.button("ယတြာတောင်းမယ်"):
        if user_name:
            with st.spinner('သင့်အတွက် ယတြာတွက်ချက်ပေးနေပါတယ် ခင်ဗျာ...'):
                prompt = f"{system_instruction} အမည် {user_name} က {problem} အတွက် မြန်မာ့ရိုးရာ ဓာတ်ရိုက်ဓာတ်ဆင် (ယတြာ) ကို အကြံပေးရမှာပါ။ အမည်ရဲ့ ရှေ့ဆုံးစာလုံး (နံ) ကို ကြည့်ပြီး လိုအပ်တဲ့ ယတြာ ဒါမှမဟုတ် အဆောင်အယောင်ကို ယောကျ်ားလေး လေသံနဲ့ သေသေချာချာ အကြံပေးပါ ခင်ဗျာ။"
                response = model.generate_content(prompt)
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
        else:
            st.warning("အမည် အရင်ထည့်ပေးပါ ခင်ဗျာ။")

st.divider()
st.caption("Developed with ❤️ by Mg Kyal Ngar | Astrology AI (Male Version)")
