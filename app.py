import streamlit as st
import google.generativeai as genai
import os
import datetime
import prompts
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- PWA Mainframe Logic ---
# ဤ Code သည် Browser ကို Install လုပ်ရန် (Add to Home Screen) လှုံ့ဆော်ပေးပါလိမ့်မည်
st.markdown(f"""
    <link rel="manifest" href="manifest.json">
    <script>
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', function() {{
        navigator.serviceWorker.register('/sw.js').then(function(registration) {{
          console.log('ServiceWorker registration successful');
        }}, function(err) {{
          console.log('ServiceWorker registration failed: ', err);
        }});
      }});
    }}
    </script>
""", unsafe_allow_html=True)

# --- Offline Support Service Worker Logic ---
st.markdown("""
    <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('./sw.js').then(function(reg) {
          console.log('Service Worker Registered!', reg);
        }).catch(function(err) {
          console.log('Service Worker Failed!', err);
        });
      });
    }
    </script>
""", unsafe_allow_html=True)

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
	[data-testid="stWidgetLabel"] p, 
	label {
    	color: #D4AF37 !important; /* ရွှေရောင် */
    	font-weight: bold !important;
    	font-size: 1.1rem !important;
    	text-shadow: 1px 1px 2px black; /* စာလုံးပိုကြွလာအောင် */
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
		border: 1px solid #D4AF37;
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
    st.error("API Key Not Found Error")

# --- Lucky Color Logic ---
now = datetime.datetime.now()
day_name = now.strftime("%A") # ဥပမာ - Wednesday

lucky_data = {
    "Monday": {"color": "ဖြူစင်သော အဖြူရောင်", "hex": "#FFFFFF", "text": "တနင်္လာ"},
    "Tuesday": {"color": "တောက်ပသော အနီရောင်", "hex": "#FF0000", "text": "အင်္ဂါ"},
    "Wednesday": {"color": "စိမ်းလန်းသော အစိမ်းရောင်", "hex": "#00FF00", "text": "ဗုဒ္ဓဟူး/ရာဟု"},
    "Thursday": {"color": "ဝင်းပသော အဝါရောင်", "hex": "#FFFF00", "text": "ကြာသပတေး"},
    "Friday": {"color": "ကြည်လင်သော အပြာရောင်", "hex": "#0000FF", "text": "သောကြာ"},
    "Saturday": {"color": "နက်မှောင်သော ခရမ်းရောင်", "hex": "#800080", "text": "စနေ"},
    "Sunday": {"color": "ရွှေအိုရောင်/လိမ္မော်ရောင်", "hex": "#FFA500", "text": "တနင်္ဂနွေ"}
}

today_lucky = lucky_data.get(day_name, lucky_data["Monday"])

# --- Display Banner ---
st.markdown(f"""
    <div style="background-color: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <span style="color: #D4AF37; font-size: 1.1rem;">✨ ယနေ့ <b>{today_lucky['text']}</b> နေ့အတွက် ကံကောင်းစေသောအရောင်မှာ <b style="color: {today_lucky['hex']}; text-shadow: 1px 1px 2px black;">{today_lucky['color']}</b> ဖြစ်ပါတယ် ✨</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1>🔮 မြန်မာ့ဗေဒင်နှင့် ဓာတ်ရိုက်ဓာတ်ဆင် AI</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌙 အိပ်မက်အဘိဓာန်", "✨ နေ့စဉ်ဟောစာတမ်း", "🛡️ ယတြာတောင်းရန်"])

# --- Helper Function for AI ---
def get_ai_response(prompt):
	loading_placeholder = st.empty()
    try:
        with st.spinner("နက္ခတ်ဗေဒင်များ တွက်ချက်နေပါသည်..."):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        loading_placeholder.empty()
        if "429" in str(e):
            st.error("AI Tokan Free Limit ပြည့်သွားပါပြီ။ ခဏနားပြီးမှ ပြန်စမ်းပေးပါ")
        else:
            st.error(f"Error တက်သွားပါတယ်: {str(e)}")
        return None

#  def get_ai_response(prompt, spinner_text):
#    loading_placeholder = st.empty()
#    try:
#        with st.spinner(spinner_text):
#            response = model.generate_content(prompt)
#            res_text = response.text
#            return res_text
#    except Exception as e:
#        loading_placeholder.empty()
#        if "429" in str(e):
#            st.error("AI Tokan Free Limit ပြည့်သွားပါပြီ။ ခဏနားပြီးမှ ပြန်စမ်းပေးပါ")
#        else:
#            st.error(f"Error တက်သွားပါတယ်: {str(e)}")
#        return None


# --- Tab 1: Dream ---
with tab1:
    user_dream = st.text_area("သင်မက်ခဲ့သည့် အိပ်မက်ကို ရေးပါ...", key="dream_input")
    if st.button("နိမိတ်ဖတ်မယ် 🌙"):
        if user_dream:
            full_prompt = prompts.DREAM_TEMPLATE.format(
                system_instruction=prompts.SYSTEM_INSTRUCTION,
                user_dream=user_dream
            )
            # Result ကို session state ထဲ သိမ်းသည်
            st.session_state['dream_res'] = get_ai_response(full_prompt)
        else:
            st.warning("အိပ်မက်ကို အရင်ရေးပေးပါ ခင်ဗျာ။")

    if 'dream_res' in st.session_state and st.session_state['dream_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['dream_res']}</div>", unsafe_allow_html=True)
        st.download_button("📁 ရလဒ်ကိုသိမ်းမယ်", st.session_state['dream_res'], file_name="dream.txt")

# --- Tab 2: Daily Horoscope ---
with tab2:
    day = st.selectbox("သင့်မွေးနေ့ ရွေးပါ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"])
    if st.button("ဟောစာတမ်းကြည့်မယ် ✨"):
        full_prompt = prompts.HOROSCOPE_TEMPLATE.format(
            system_instruction=prompts.SYSTEM_INSTRUCTION,
            day=day
        )
        st.session_state['horo_res'] = get_ai_response(full_prompt)
            
    if 'horo_res' in st.session_state and st.session_state['horo_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['horo_res']}</div>", unsafe_allow_html=True)
        st.download_button("📂 ဟောစာတမ်းသိမ်းမယ်", st.session_state['horo_res'], file_name="horoscope.txt")

# --- Tab 3: Yadaya ---
with tab3:
    u_name = st.text_input("သင့်အမည်")
     # ထပ်တိုးပေးထားသော အခက်အခဲများ
        prob = st.selectbox("ရင်ဆိုင်နေရသော အခက်အခဲ", [
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
        if u_name:
            full_prompt = prompts.YADAYA_TEMPLATE.format(
                system_instruction=prompts.SYSTEM_INSTRUCTION,
                user_name=u_name,
                problem=prob
            )
            st.session_state['yadaya_res'] = get_ai_response(full_prompt)
        else:
            st.warning("အမည် ထည့်ပေးပါ ခင်ဗျာ။")

    if 'yadaya_res' in st.session_state and st.session_state['yadaya_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['yadaya_res']}</div>", unsafe_allow_html=True)
        st.download_button("📁 ယတြာကိုသိမ်းမယ်", st.session_state['yadaya_res'], file_name="yadaya.txt")
        
# --- Viewer Counter & Facebook Share Section ---
# --- Footer Section (Revised Version) ---
st.divider()

# Link အမှန်ကို သတ်မှတ်ခြင်း
app_url_official = "https://myanmar-ai-astrology-by-kyalngar.streamlit.app"

# အခြား Counter တစ်ခု (VisitorBadge.io) ကို ပြောင်းသုံးကြည့်ပါမည်
# ဒါက hits ထက်စာရင် broken link ဖြစ်နိုင်ခြေ ပိုနည်းပါသည်
counter_html_new = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
    <div style="color: #D4AF37; font-size: 0.9rem; font-weight: bold;">
        Developed with ❤️ by Mg Kyal Ngar | Astrology AI v3.5
    </div>
    <div>
        <a href="https://visitorbadge.io/status?path={app_url_official}">
            <img src="https://api.visitorbadge.io/api/combined?path={app_url_official}&label=VISITORS&countColor=%23d4af37&style=flat" alt="Visitor Counter"/>
        </a>
    </div>
</div>
"""
st.markdown(counter_html_new, unsafe_allow_html=True)

# Facebook Share Button
st.markdown(f"""
    <div style="text-align: center; margin-top: 25px;">
        <a href="https://www.facebook.com/sharer/sharer.php?u={app_url_official}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #1877F2; color: white; padding: 10px 25px; border-radius: 25px; font-weight: bold; display: inline-block;">
                🔵 Facebook မှာ Share မယ်
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

