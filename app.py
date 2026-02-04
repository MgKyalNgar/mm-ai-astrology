import streamlit as st
import google.generativeai as genai
import os

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- Custom CSS (Particles & UI Fixes) ---
st.markdown("""
    <style>
    /* 1. Main App Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        overflow: hidden;
    }
    
    /* 2. Floating Stars Layer */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        background-size: 500px 500px;
        z-index: 0; /* Background layer */
        animation: move-stars 300s linear infinite; /* Star Speed */
        opacity: 0.6;
        pointer-events: none;
    }

    @keyframes move-stars {
        from { background-position: 0 0; }
        to { background-position: 10000px 5000px; }
    }

    /* 3. Content Visibility */
    .main .block-container {
        position: relative;
        z-index: 1; /* Content အားလုံးကို Stars ရဲ့ အပေါ်မှာထားခြင်း */
    }

    /* Light Mode မှာပါ စာသားတွေ အမြဲပေါ်နေအောင် Fixed လုပ်ခြင်း */
	/* Label စာသားများ (ဥပမာ - သင့်အမည်၊ အိပ်မက်ရေးပါ) */
	.stWidgetLabel {
		color: #D4AF37 !important; /* အမြဲတမ်း ရွှေရောင် ဖြစ်နေစေရမည် */
		font-weight: bold !important;
		font-size: 1.1rem !important;
	}

    /* Result Card Styling */
    .result-card {
        background-color: rgba(26, 28, 35, 0.95); 
        padding: 25px; 
        border-radius: 15px;
        border: 1px solid #D4AF37; 
        color: #F0F0F0; 
        line-height: 1.6;
        margin-top: 15px;
        white-space: pre-wrap;
    }

    h1 { color: #D4AF37 !important; text-align: center; font-size: 2em !important; text-shadow: 2px 2px 4px #000; }

    /* Tabs Styling - ပိုကျယ်သွားအောင် ပြင်ထားသည် */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 55px; 
        background-color: rgba(26, 28, 35, 0.8); 
        border-radius: 10px 10px 0 0;
        color: white; 
        font-size: 16px;
        padding: 0 25px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold;
    }

    .stButton>button {
        width: 100%; border-radius: 25px; height: 3.5em;
        background-color: #D4AF37; color: black; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FFD700; transform: scale(1.01); }
    </style>
    """, unsafe_allow_html=True)

# --- API Configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API Key မတွေ့ပါ။ Settings ထဲမှာ GEMINI_API_KEY ထည့်ပေးပါ။")

st.markdown("<h1>🔮 မြန်မာ့ဗေဒင်နှင့် ဓာတ်ရိုက်ဓာတ်ဆင် AI</h1>", unsafe_allow_html=True)

# --- AI Instructions ---
system_instruction = """
မင်းက မြန်မာ့ရိုးရာ ဗေဒင်ပညာရှင် ယောကျ်ားလေးတစ်ယောက်ပါ။ 
စကားပြောရင် 'ကျွန်တော်' နဲ့ 'ခင်ဗျာ' ကို သုံးရပါမယ်။ 
နှုတ်ဆက်တဲ့အခါ 'မင်္ဂလာပါ [နာမည်] ခင်ဗျာ' လို့ပဲ သုံးပါ။ 
အဖြေတွေကို ရေးတဲ့အခါ သက်ဆိုင်ရာ Emoji (🔮, ✨, 🌙, 🍀, 🧿, 🛡️) လေးတွေကို ဆွဲဆောင်မှုရှိရှိ ထည့်ပေးပါ။
စာကြောင်းတွေကို ကျစ်ကျစ်လျစ်လျစ်နဲ့ ဖတ်ရလွယ်အောင် ရေးပေးပါ။
"""

tab1, tab2, tab3 = st.tabs(["🌙 အိပ်မက်အဘိဓာန်", "✨ နေ့စဉ်ဟောစာတမ်း", "🛡️ ယတြာတောင်းရန်"])

# --- Tab 1: Dream ---
with tab1:
    user_dream = st.text_area("သင်မက်ခဲ့သည့် အိပ်မက်ကို ရေးပါ...", height=100)
    if st.button("နိမိတ်ဖတ်မယ် 🌙"):
        if user_dream:
            with st.spinner('ကျွန်တော် တွက်ချက်ပေးနေပါတယ် ခင်ဗျာ...'):
                prompt = f"{system_instruction} အိပ်မက်: '{user_dream}' ကို နိမိတ်ဖတ်ပေးပါ။"
                response = model.generate_content(prompt)
                res_text = response.text
                st.markdown(f"<div class='result-card'>{res_text}</div>", unsafe_allow_html=True)
                st.download_button("📂 ရလဒ်ကိုသိမ်းမယ်", res_text, file_name="dream_analysis.txt")

# --- Tab 2: Daily Horoscope ---
with tab2:
    day = st.selectbox("သင့်မွေးနေ့ (နေ့နံ) ရွေးပါ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"])
    if st.button("ဟောစာတမ်းကြည့်မယ် ✨"):
        with st.spinner('နက္ခတ်ကို ကြည့်ပေးနေပါတယ် ခင်ဗျာ...'):
            prompt = f"{system_instruction} {day} သားသမီးတွေအတွက် ဒီနေ့အတွက် ဟောစာတမ်းကို အချစ်၊ စီးပွား၊ ကျန်းမာရေး ခွဲပြီး ဟောပေးပါ။"
            response = model.generate_content(prompt)
            res_text = response.text
            st.markdown(f"<div class='result-card'>{res_text}</div>", unsafe_allow_html=True)
            st.download_button("📂 ဟောစာတမ်းသိမ်းမယ်", res_text, file_name="horoscope.txt")

# --- Tab 3: Yadaya (ဓာတ်ရိုက်ဓာတ်ဆင်) ---
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("သင့်အမည် (သို့မဟုတ်) နာမည်")
    with col2:
        # ထပ်တိုးပေးထားသော အခက်အခဲများ
        problem = st.selectbox("ရင်ဆိုင်နေရသော အခက်အခဲ", [
            "စီးပွားရေးညံ့ခြင်း/ငွေကြေးခက်ခဲခြင်း", 
            "အချစ်ရေးအဆင်မပြေခြင်း", 
            "အိမ်ထောင်ရေးအဆင်မပြေခြင်း",
            "ကျန်းမာရေးမကောင်းခြင်း", 
            "အတိုက်အခံ/ရန်များခြင်း", 
            "အလုပ်အကိုင်ခက်ခဲခြင်း",
            "ပညာရေးအဆင်မပြေခြင်း",
            "အကြွေးကိစ္စအခက်အခဲဖြစ်ခြင်း",
            "တရားရင်ဆိုင်နေရခြင်း",
            "ခရီးသွားလာရန်အခက်အခဲရှိခြင်း"
        ])
    
    if st.button("ယတြာတောင်းမယ် 🛡️"):
        if user_name:
            with st.spinner('ယတြာတွက်ချက်ပေးနေပါတယ် ခင်ဗျာ...'):
                prompt = f"{system_instruction} အမည် {user_name} က {problem} ဖြစ်နေတာအတွက် အထိရောက်ဆုံး ယတြာပေးပါ။ အစမှာ 'မင်္ဂလာပါ {user_name} ခင်ဗျာ' လို့ နှုတ်ဆက်ပါ။"
                response = model.generate_content(prompt)
                res_text = response.text
                st.markdown(f"<div class='result-card'>{res_text}</div>", unsafe_allow_html=True)
                st.download_button("📂 ယတြာကိုသိမ်းမယ်", res_text, file_name="yadaya.txt")
        else:
            st.warning("အမည် ထည့်ပေးပါ ခင်ဗျာ။")

st.divider()
st.caption("Developed with ❤️ by Mg Kyal Ngar | Astrology AI v2.5")
