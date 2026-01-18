import streamlit as st
import streamlit.components.v1 as components
import requests
import json

GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="リアルタイム翻訳", layout="centered")
st.title("🚀 爆速・リアルタイム翻訳")

option = st.selectbox('翻訳言語', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# --- JavaScript部分（ここを修正しました） ---
st_canvas = components.html(
    f"""
    <div style="text-align: center;">
        <button id="start-btn" style="padding: 15px 30px; font-size: 20px; border-radius: 10px; cursor: pointer; background-color: #FF4B4B; color: white; border: none; width: 100%;">
            🎤 音声認識スタート
        </button>
        <p id="status" style="margin-top: 10px; color: #555; font-weight: bold;">ボタンを押して話してください</p>
    </div>

    <script>
        const btn = document.getElementById('start-btn');
        const status = document.getElementById('status');
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        
        recognition.lang = 'ja-JP';
        recognition.interimResults = false; 

        btn.onclick = () => {{
            recognition.start();
            status.innerText = "👂 聞き取り中...";
            btn.style.backgroundColor = "#4CAF50";
        }};

        recognition.onresult = (event) => {{
            const result = event.results[0][0].transcript;
            // ★ここを修正：Streamlitに値をセットする命令を確実に送る
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: result
            }}, '*');
            status.innerText = "✅ 認識完了: " + result;
        }};

        recognition.onend = () => {{
            btn.style.backgroundColor = "#FF4B4B";
        }};
    </script>
    """,
    height=150,
)

# JavaScriptからの値を受け取る（ここで値が空にならないようにします）
voice_input = st_canvas if st_canvas else ""

# 2. 入力エリア（ここに自動で文字が入ります）
# st.text_inputの代わりに st.text_areaを使うとより安定します
text_input = st.text_area("認識された文字（修正も可能）", value=voice_input, height=100)

if text_input:
    try:
        res = requests.post(GAS_URL, data=json.dumps({{"ja": text_input, "lang": lang_code, "mode": "translate_only"}}))
        st.markdown(f"### 【{option}】")
        st.success(res.text)
        
        if st.button("✅ シートに保存"):
            requests.post(GAS_URL, data=json.dumps({{"ja": text_input, "lang": lang_code, "mode": "save"}}))
            st.balloons()
    except:
        st.error("翻訳エラーが発生しました")
