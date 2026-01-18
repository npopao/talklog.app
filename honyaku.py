import streamlit as st
import streamlit.components.v1 as components
import requests
import json

GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="リアルタイム翻訳", layout="centered")
st.title("🚀 爆速・リアルタイム翻訳")

# 言語設定
option = st.selectbox('翻訳言語', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# --- JavaScriptでブラウザの音声認識を強制起動 ---
st.write("### 1. 下のボタンを押して話してください")
# ここでブラウザのマイク機能を直接叩きます
st_canvas = components.html(
    """
    <div style="text-align: center;">
        <button id="start-btn" style="padding: 15px 30px; font-size: 20px; border-radius: 10px; cursor: pointer; background-color: #FF4B4B; color: white; border: none;">
            🎤 音声認識スタート
        </button>
        <p id="status" style="margin-top: 10px; color: #555;">ボタンを押して話してください</p>
    </div>

    <script>
        const btn = document.getElementById('start-btn');
        const status = document.getElementById('status');
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        
        recognition.lang = 'ja-JP';
        recognition.interimResults = true; // 喋っている最中の結果も取得する
        recognition.continuous = false;

        btn.onclick = () => {
            recognition.start();
            status.innerText = "聞き取り中...";
            btn.style.backgroundColor = "#4CAF50";
        };

        recognition.onresult = (event) => {
            const result = event.results[0][0].transcript;
            // Streamlitの親ウィンドウに文字を即座に送る
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: result}, '*');
            status.innerText = "認識中: " + result;
        };

        recognition.onend = () => {
            status.innerText = "完了！下の枠に文字が入りました。";
            btn.style.backgroundColor = "#FF4B4B";
        };
    </script>
    """,
    height=150,
)

# JavaScriptから受け取った文字を入れる隠し枠
# ※実際にはユーザーが入力する代わりに、上のマイクがここに文字を流し込みます
text_input = st.text_input("認識された文字（修正も可能）", key="voice_input")

if text_input:
    # 即座にGASへ翻訳を依頼
    try:
        res = requests.post(GAS_URL, data=json.dumps({"ja": text_input, "lang": lang_code, "mode": "translate_only"}))
        st.markdown(f"### 【{option}】")
        st.success(res.text)
        
        if st.button("✅ シートに保存"):
            requests.post(GAS_URL, data=json.dumps({"ja": text_input, "lang": lang_code, "mode": "save"}))
            st.balloons()
    except:
        st.error("通信エラー")
