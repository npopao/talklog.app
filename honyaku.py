import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# 設定
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="TalkLog", layout="centered")

# 自動翻訳対策（これ重要！）
st.markdown('<div translate="no">', unsafe_allow_html=True)
st.title("🎤 リアルタイム翻訳メモ")

opt = st.selectbox('翻訳先', ('インドネシア語', '英語'))
l_code = 'id' if opt == 'インドネシア語' else 'en'

# 文字を一時保存する場所
if 'txt' not in st.session_state:
    st.session_state.txt = ""

# --- 音声認識ボタン ---
# ここで喋った文字が "res" に入ります
res = components.html(
    """
    <div translate="no">
        <button id="b" style="padding:18px; font-size:18px; border-radius:10px; width:100%; background:#FF4B4B; color:white; border:none; cursor:pointer; font-weight:bold;">
            🎤 音声認識スタート
        </button>
        <p id="m" style="margin-top:10px; color:#555; text-align:center;">ボタンを押して話してください</p>
    </div>
    <script>
        const b = document.getElementById('b');
        const m = document.getElementById('m');
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SR) {
            const r = new SR();
            r.lang = 'ja-JP';
            b.onclick = () => { r.start(); m.innerText = "👂 聞き取り中..."; b.style.background = "#4CAF50"; };
            r.onresult = (e) => {
                const t = e.results[0][0].transcript;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: t}, '*');
                m.innerText = "✅ 完了: " + t;
            };
            r.onend = () => { b.style.background = "#FF4B4B"; };
        }
    </script>
    """,
    height=130,
)

# 【ここが修正ポイント！】ボタンの情報ではなく、文字だけを抽出します
if isinstance(res, str) and res != "":
    st.session_state.txt = res

# --- 翻訳処理 ---
t_in = st.text_input("認識された日本語", value=st.session_state.txt)

if t_in:
    try:
        # 翻訳だけ実行
        ans = requests.post(GAS_URL, data=json.dumps({"ja": t_in, "lang": l_code, "mode": "translate_only"}), timeout=10)
        st.write(f"### 【{opt}】")
        st.info(ans.text)
        
        if st.button("✅ 保存する"):
            requests.post(GAS_URL, data=json.dumps({"ja": t_in, "lang": l_code, "mode": "save"}))
            st.balloons()
            st.success("スプレッドシートに保存しました！")
    except:
        st.error("通信エラー")

st.markdown('</div>', unsafe_allow_html=True)
