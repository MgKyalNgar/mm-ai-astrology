from flask import Flask
import subprocess
import os

app = Flask(__name__)

# Streamlit App ကို run ရန် gunicorn command
def run_streamlit():
    # Vercel တွင် Port ကို Environment Variable မှ ရယူရပါမည်
    port = os.environ.get("PORT", "8501")
    command = f"gunicorn --worker-class=geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:{port} streamlit_app:run"
    subprocess.Popen(command, shell=True)

# Vercel က ဒီ route ကို လှမ်းခေါ်ပါမည်
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Streamlit app ကို run ပြီးသားလား စစ်ဆေးခြင်း
    # မ run ရသေးရင် run ပေးခြင်း
    # ဒီနေရာမှာ Streamlit ရဲ့ URL ကို redirect လုပ်ပေးရုံပါ
    streamlit_port = "8501" # Streamlit default port
    streamlit_url = f"http://localhost:{streamlit_port}"
    return f'<meta http-equiv="refresh" content="0; url={streamlit_url}" />'

if __name__ == "__main__":
    run_streamlit()
    # Flask app ကို development အတွက် run ရန်
    app.run(port=5000)

