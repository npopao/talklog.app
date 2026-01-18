import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# GASのURL
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="TalkLog")

# --- Google翻訳の破壊を防ぐためのガード ---
st.markdown('<div translate="no">', unsafe_allow_html=True)

st.title("🎤 リアルタイム翻訳")

lang_opt = st.selectbox('翻訳先', ('インドネシア語', '英語'))
target_lang = 'id' if lang_opt == 'インドネシア語' else 'en'

if 'my_text' not in st.session_state:
    st.session_state.my_text = ""

# --- 音声認識ボタン (超シンプル版) ---
res_val = components.html(
    """
    <div translate="no">
        <button id="main-btn" style="padding: 20px; font-size: 20px; border-radius: 12px; width: 100%; background-color: #FF4B4B; color: white; border: none; cursor: pointer; font-weight: bold;">
            🎤 音声認識スタート
        </button>
        <p id="status-msg" style="margin-top: 10px; color: #555; text-align: center;">ボタンを押して話してください</p>
    </div>
    <script>
        const btn = document.getElementById('main-btn');
        const msg = document.getElementById('status-msg');
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRec) {
            const rec = new SpeechRec();
            rec.lang = 'ja-JP';
            btn.onclick = () => {
                rec.start();
                msg.innerText = "👂 聞き取り中...";
                btn.style.backgroundColor = "#4CAF50";
            };
            rec.onresult = (e) => {
                const resultText = e.results[0][0].transcript;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: resultText}, '*');
                msg.innerText = "✅ 完了: " + resultText;
            };
            rec.onend = () => { btn.style.backgroundColor = "#FF4B4B"; };
        } else {
            msg.innerText = "このブラウザは音声認識非対応です";
        }
    </script>
    """,
    height=150,
)

# 文字が入ってきたら更新
if res_val:
    st.session_state.my_text = res_val

# --- 表示と翻訳 ---
user_input = st.text_input("認識された言葉", value=st.session_state.my_text)

if user_input:
    try:
        # GASへ翻訳依頼
        api_res = requests.post(GAS_URL, data=json.dumps({
            "ja": user_input, "lang": target_lang, "mode": "translate_only"
        }), timeout=10)
        
        st.write(f"### 【{lang_opt}】")
        st.info(api_res.text)
        
        if st.button("✅ 保存する"):
            requests.post(GAS_URL, data=json.dumps({
                "ja": user_input, "lang": target_lang, "mode": "save"
            }))
            st.balloons()
            st.success("スプレッドシートに保存しました！")
    except:
        st.error("通信エラー: GASを確認してください")

st.markdown('</div>', unsafe_allow_html=True)
