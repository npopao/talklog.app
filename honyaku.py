import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# --- 設定 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="TalkLog", layout="centered")

# --- ブラウザの自動翻訳による破壊を防ぐおまじない ---
st.markdown('<div id="main-content" translate="no">', unsafe_allow_html=True)

st.title("🎤 リアルタイム翻訳メモ")

option = st.selectbox('翻訳言語を選んでください', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

if 'v_text' not in st.session_state:
    st.session_state.v_text = ""

# --- 音声認識ボタン ---
# Pythonの変数(f-string)を使わず、直接記述してエラーを防ぎます
val = components.html(
    """
    <div style="text-align: center;">
        <button id="btn" style="padding: 20px; font-size: 20px; border-radius: 12px; width: 100%; background-color: #FF4B4B; color: white; border: none; cursor: pointer; font-weight: bold;">
            🎤 音声認識スタート
        </button>
        <p id="msg" style="margin-top: 10px; color: #555;">ボタンを押して話してください</p>
    </div>
    <script>
        const btn = document.getElementById('btn');
        const msg = document.getElementById('msg');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
            const rec = new SpeechRecognition();
            rec.lang = 'ja-JP';
            btn.onclick = () => {
                rec.start();
                msg.innerText = "👂 聞き取り中...";
                btn.style.backgroundColor = "#4CAF50";
            };
            rec.onresult = (e) => {
                const t = e.results[0][0].transcript;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: t}, '*');
                msg.innerText = "✅ 認識完了: " + t;
            };
            rec.onend = () => { btn.style.backgroundColor = "#FF4B4B"; };
        } else {
            msg.innerText = "エラー: ブラウザが音声認識に対応していません";
        }
    </script>
    """,
    height=150,
)

if val:
    st.session_state.v_text = val

# --- 結果表示と翻訳 ---
text_in = st.text_input("認識された日本語", value=st.session_state.v_text)

if text_in:
    try:
        res = requests.post(GAS_URL, data=json.dumps({"ja": text_in, "lang": lang_code, "mode": "translate_only"}), timeout=10)
        st.write(f"### 【{option}】")
        st.info(res.text)
        
        if st.button("✅ スプレッドシートに保存"):
            requests.post(GAS_URL, data=json.dumps({"ja": text_in, "lang": lang_code, "mode": "save"}))
            st.balloons()
            st.success("保存しました！")
    except:
        st.error("通信エラー: GASを確認してください")

st.markdown('</div>', unsafe_allow_html=True)
