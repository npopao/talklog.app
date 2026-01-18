import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# 送信先のGAS URL
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="リアルタイム翻訳メモ", page_icon="🎤")
st.title("🎤 リアルタイム翻訳メモ")

# 言語選択
option = st.selectbox('翻訳言語を選んでください', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# セッション状態の初期化（文字を保持するため）
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

# --- 1. ブラウザ音声認識コンポーネント ---
# JavaScriptでブラウザのマイクを直接動かし、結果をPythonに投げます
st.write("### 1. マイクを押して話してください")
val = components.html(
    """
    <div style="text-align: center;">
        <button id="btn" style="padding: 15px; font-size: 18px; border-radius: 10px; width: 100%; background-color: #FF4B4B; color: white; border: none; cursor: pointer; font-weight: bold;">
            🎤 音声認識スタート
        </button>
        <p id="msg" style="margin-top: 10px; color: #555; font-size: 14px;">ボタンを押すと聞き取りを開始します</p>
    </div>
    <script>
        const btn = document.getElementById('btn');
        const msg = document.getElementById('msg');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            msg.innerText = "エラー: お使いのブラウザは音声認識に対応していません";
        } else {
            const recognition = new SpeechRecognition();
            recognition.lang = 'ja-JP';
            recognition.interimResults = false;

            btn.onclick = () => {
                recognition.start();
                msg.innerText = "👂 聞き取り中... 喋ってください";
                btn.style.backgroundColor = "#4CAF50";
            };

            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                // Streamlit側に値を送信
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: text}, '*');
                msg.innerText = "✅ 認識完了: " + text;
            };

            recognition.onend = () => {
                btn.style.backgroundColor = "#FF4B4B";
            };
        }
    </script>
    """,
    height=130,
)

# JavaScriptから新しい値が届いたら、セッションに保存
if val is not None and val != "":
    st.session_state.voice_text = val

# --- 2. 認識結果の表示と翻訳 ---
st.write("---")
# 枠の中に自動で文字が入ります
text_input = st.text_input("認識
