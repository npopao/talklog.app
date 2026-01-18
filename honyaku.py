import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# 設定
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="リアルタイム翻訳", layout="centered")
st.title("🎤 リアルタイム翻訳")

# 言語設定
option = st.selectbox('翻訳言語', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# --- 1. JavaScriptによる音声認識ボタン ---
# ここで喋った内容が、下の枠（voice_input）に直接流し込まれます
val = components.html(
    """
    <div style="text-align: center;">
        <button id="btn" style="padding: 20px; font-size: 20px; border-radius: 10px; width: 100%; background-color: #FF4B4B; color: white; border: none; cursor: pointer;">
            🎤 音声認識スタート
        </button>
        <p id="msg" style="margin-top: 10px; font-weight: bold; color: #555;">ボタンを押して話してください</p>
    </div>
    <script>
        const btn = document.getElementById('btn');
        const msg = document.getElementById('msg');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            msg.innerText = "お使いのブラウザは音声認識に対応していません";
        } else {
            const recognition = new SpeechRecognition();
            recognition.lang = 'ja-JP';
            
            btn.onclick = () => {
                recognition.start();
                msg.innerText = "👂 聞き取り中...";
                btn.style.backgroundColor = "#4CAF50";
            };
            
            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                // Streamlitに直接値を送る
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: text}, '*');
                msg.innerText = "✅ 認識完了: " + text;
            };
            
            recognition.onend = () => {
                btn.style.backgroundColor = "#FF4B4B";
            };
        }
    </script>
    """,
    height=150,
)

# --- 2. 認識された文字の表示と翻訳 ---
# マイクボタンから届いた文字をキャッチします
text_input = st.text_input("認識された日本語", value=val if val else "")

if text_input:
    try:
        # GASに翻訳を依頼
        res = requests.post(GAS_URL, data=json.dumps({
            "ja": text_input,
            "lang": lang_code,
            "mode": "translate_only"
        }), timeout=10)
        
        # 翻訳結果を大きく表示
        st.markdown(f"### 【{option}】")
        st.success(res.text)
        
        # 3. 保存ボタン
        if st.button("✅ スプレッドシートに保存"):
            requests.post(GAS_URL, data=json.dumps({
                "ja": text_input, 
                "lang": lang_code, 
                "mode": "save"
            }))
            st.balloons()
            st.write("保存完了！")
    except:
        st.error("通信エラーが発生しました。ネット接続を確認してください。")

st.divider()
st.caption("※マイクが反応しない場合はブラウザの許可設定を確認してください。")
