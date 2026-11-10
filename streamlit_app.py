import streamlit as st
import google.generativeai as genai
from pytrends.request import TrendReq

st.set_page_config(page_title="Shorts Viral Planner", page_icon="🚀", layout="wide")
st.title("🚀 YouTube Shorts Viral Planner & Creator")

with st.sidebar:
    st.header("⚙️ API Settings")
    gemini_api_key = st.text_input("Gemini API Key डालें:", type="password")
    
    st.header("📺 चैनल सेटिंग्स")
    channel_niche = st.selectbox(
        "चैनल का प्रकार:", 
        ["Tech & AI Tutorials", "Education & GK", "Storytelling", "General"]
    )
    video_style = st.selectbox(
        "वीडियो स्टाइल:", 
        ["AI Animated Visuals", "Whiteboard Animation", "Screen Recording + Voiceover"]
    )

try:
    pytrends = TrendReq(hl='en-US', tz=330)
except Exception:
    pass

st.subheader("🔥 1. लाइव ट्रेंड और कीवर्ड रिसर्च")
col1, col2 = st.columns([3, 1])
with col1:
    keyword_idea = st.text_input("किस टॉपिक पर वीडियो बनाना है? (उदा. AI Video, Tech News):")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    check_trends = st.button("ट्रेंड स्कैन करें", use_container_width=True)

if check_trends and keyword_idea:
    with st.spinner("YouTube और Google ट्रेंड्स स्कैन हो रहे हैं..."):
        try:
            pytrends.build_payload(kw_list=[keyword_idea], timeframe='now 7-d', geo='IN')
            related_queries = pytrends.related_queries()
            if related_queries[keyword_idea]['top'] is not None:
                st.success("✅ टारगेट ऑडियंस अभी ये सर्च कर रही है:")
                top_trends = related_queries[keyword_idea]['top'].head(5)
                st.dataframe(top_trends, use_container_width=True)
                st.session_state['best_keyword'] = top_trends['query'].iloc[0]
            else:
                st.session_state['best_keyword'] = keyword_idea
        except Exception:
            st.session_state['best_keyword'] = keyword_idea

st.subheader("⏱️ 2. बेस्ट अपलोड टाइम")
st.info("💡 **एल्गोरिदम टिप:** भारत में टेक और एजुकेशनल शॉर्ट्स के लिए शाम **6:30 PM से 8:15 PM** के बीच सबसे ज्यादा व्यूअर्स ऑनलाइन रहते हैं।")

st.subheader("🎬 3. वायरल स्क्रिप्ट और एडिटिंग गाइड")
if st.button("ऑटोमैटिक स्क्रिप्ट तैयार करें", type="primary"):
    if not gemini_api_key:
        st.error("⚠️ कृपया साइडबार में Gemini API Key डालें।")
    elif 'best_keyword' not in st.session_state and not keyword_idea:
        st.error("⚠️ कृपया पहले कोई टॉपिक डालें या ट्रेंड स्कैन करें।")
    else:
        target_topic = st.session_state.get('best_keyword', keyword_idea)
        with st.spinner(f"'{target_topic}' के लिए स्क्रिप्ट तैयार की जा रही है..."):
            try:
                model = genai.GenerativeModel('gemini-pro')
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                तुम एक एक्सपर्ट YouTube Shorts प्रोड्यूसर हो। मेरा चैनल '{channel_niche}' है और स्टाइल '{video_style}' है।
                मुझे '{target_topic}' पर 60 सेकंड के 9:16 वर्टिकल Short की पूरी स्क्रिप्ट चाहिए।
                1. 🪝 Killer Hook (0-3 sec): दर्शक को रोकने वाली पहली लाइन।
                2. 📝 Main Script (Hinglish): तेज और एंगेजिंग कंटेंट।
                3. ✂️ Visual/Editing Guide: स्क्रीन पर क्या वीडियो/इमेज लूप और टेक्स्ट पॉप-अप्स आने चाहिए।
                4. 🏷️ SEO: क्लिकेबल टाइटल और 5 वायरल हैशटैग।
                """
                res = model.generate_content(prompt)
                st.markdown("### 📜 आपकी तैयार स्क्रिप्ट:")
                st.write(res.text)
            except Exception as e:
                st.error(f"एरर: {e}")
