import os
import subprocess
from flask import Flask, request, Response
import requests
import threading

# Flask app ကို တည်ဆောက်
app = Flask(__name__)

# Streamlit App ကို နောက်ကွယ်မှာ run မည့် function
def run_streamlit():
    # Streamlit ကို port 8501 မှာ run မယ်
    command = "streamlit run app.py --server.port=8501 --server.headless=true --server.enableCORS=false"
    subprocess.run(command, shell=True)

# Streamlit ကို thread သီးသန့်တစ်ခုဖြင့် run ခြင်း
# ဒါမှ Flask app က request တွေကို ဆက်လက်ကိုင်တွယ်နိုင်မှာဖြစ်တယ်
thread = threading.Thread(target=run_streamlit)
thread.daemon = True
thread.start()

# Vercel ကနေ ဝင်လာတဲ့ request တွေကို Streamlit ဆီ လမ်းကြောင်းလွှဲပေးမယ့် Proxy
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def proxy(path):
    streamlit_port = "8501"
    url = f'http://127.0.0.1:{streamlit_port}/{path}'
    
    # User ရဲ့ request header တွေကို ကူးယူ
    req_headers = {key: value for (key, value) in request.headers if key.lower() != 'host'}
    
    # Streamlit server ဆီကို request ပို့ခြင်း
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=req_headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            stream=True
        )

        # Vercel မှာ မလိုအပ်တဲ့ header တွေကို ဖယ်ထုတ်
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]

        # Streamlit က ပြန်ပို့လိုက်တဲ့ response ကို user ဆီ ပြန်ပေး
        return Response(resp.iter_content(chunk_size=1024), resp.status_code, resp_headers)

    except requests.exceptions.ConnectionError:
        # Streamlit app စ run နေတုန်းမှာ ခဏစောင့်ဖို့ response
        return "Service is starting, please wait a moment and refresh.", 503

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)))
