import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# 設定
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="リアルタイム翻訳", layout="centered")
st.title("🎤 リアルタイム翻訳")

# 言語設定
option = st.selectbox('翻訳言語を選んでください', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# 文字保存用
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

# --- 1. 音声認識ボタン ---
# JavaScriptの通信ミスを防ぐため、極限までシンプルにしました
val = components.html(
    """
    <div style="text-align: center;">
        <button id="btn" style="padding: 15px; font-size: 18px; border-radius: 10px; width: 100%; background-color: #FF4B4B; color: white; border: none; cursor: pointer; font-weight: bold;">
            🎤 音声認識スタート
        </button>
        <p id="msg" style="margin-top: 10px; color: #555; font-size: 14px;">ボタンを押して話してください</p>
    </div>
    <script>
        const btn = document.getElementById('btn');
        const msg = document.getElementById('msg');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.lang = 'ja-JP';
            
            btn.onclick = () => {
                recognition.start();
                msg.innerText = "👂 聞き取り中...";
                btn.style.backgroundColor = "#4CAF50";
            };
            
            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                // Python側に結果を送信
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

# ボタンから文字が届いた場合のみ更新
if val:
    st.session_state.voice_text = val

# --- 2. 認識結果の表示と翻訳 ---
# DeltaGeneratorエラーを防ぐため、valueに直接セッション値を指定
text_input = st.text_input("認識された日本語", value=st.session_state.voice_text)

if text_input:
    try:
        # GASへ翻訳依頼
        res = requests.post(GAS_URL, data=json.dumps({
            "ja": text_input, 
            "lang": lang_code, 
            "mode": "translate_only"
        }), timeout=10)
        
        st.markdown(f"### 【{option}】")
        st.info(res.text)
        
        # 3. 保存ボタン
        if st.button("✅ スプレッドシートに保存"):
            requests.post(GAS_URL, data=json.dumps({
                "ja": text_input, 
                "lang": lang_code, 
                "mode": "save"
            }))
            st.balloons()
            st.success("保存完了！")
    except:
        st.error("通信エラー: GASの設定を確認してください")

st.divider()
st.caption("※Chrome または Safari で使用してください")
