import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Magic Downloader", page_icon="🪄", layout="wide")

# প্রফেশনাল CSS ডিজাইন
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড অ্যানিমেশন */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* গ্লাস ইফেক্ট কার্ড */
    .glass-card {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 20px;
        margin: 10px 0;
    }

    /* বাটন স্টাইল */
    .stButton>button {
        background: #ffffff;
        color: #e73c7e !important;
        border-radius: 50px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    h1, h2, h3, p {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# কন্টেন্ট এরিয়া
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("🪄 ম্যাজিক ভিডিও ডাউনলোডার")
st.write("সবচেয়ে দ্রুত এবং সুন্দর উপায়ে ভিডিও সেভ করুন।")

# ইনপুট
url = st.text_input("🔗 আপনার লিঙ্কটি এখানে দিন:", placeholder="ইউটিউব বা অন্য লিঙ্ক...")

if url:
    try:
        with st.spinner('✨ জাদুর মতো তথ্য আনা হচ্ছে...'):
            ydl_opts_info = {
                'quiet': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
                title = info.get('title')

            st.markdown(f"### 🎬 {title}")
            st.video(url)
            
            st.write("---")
            format_choice = st.radio("📂 কী ফরম্যাটে নেবেন?", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)
            
            if st.button("🚀 এখনই ডাউনলোড করুন"):
                with st.spinner('⚙️ কাজ চলছে...'):
                    ydl_opts = {
                        'nocheckcertificate': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    if format_choice == "অডিও (MP3)":
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}], 'outtmpl': 'm.%(ext)s'})
                        fname = "m.mp3"
                    else:
                        ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 'outtmpl': 'v.mp4'})
                        fname = "v.mp4"

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

                    with open(fname, "rb") as f:
                        st.download_button(label="💾 আপনার ডিভাইসে সেভ করুন", data=f, file_name=f"Magic_{fname}")
                    st.balloons()
    except:
        st.error("লিঙ্কটি সঠিক নয় বা কাজ করছে না।")

st.markdown('</div>', unsafe_allow_html=True)
