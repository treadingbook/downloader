import streamlit as st
import yt_dlp
import os
import time

# পেজ কনফিগারেশন
st.set_page_config(page_title="Cyber Downloader Terminal", page_icon="📟", layout="wide")

# হ্যাকার থিম সিএসএস (Matrix Background and Neon Styling)
st.markdown("""
    <style>
    /* ম্যাট্রিক্স ব্যাকগ্রাউন্ড ইফেক্ট */
    .stApp {
        background: black;
        background-image: linear-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px), 
                          linear-gradient(90deg, rgba(0, 255, 0, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        color: #00FF41;
        font-family: 'Courier New', Courier, monospace;
    }

    /* ইনপুট বক্স স্টাইল */
    .stTextInput>div>div>input {
        background-color: #000 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }

    /* বাটন স্টাইল */
    .stButton>button {
        background-color: #003300 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        box-shadow: 0 0 10px #00FF41;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: black !important;
        box-shadow: 0 0 20px #00FF41;
    }

    /* টেক্সট এরিয়া */
    .stTextArea>div>div>textarea {
        background-color: #050505 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }

    h1, h2, h3, p {
        text-shadow: 0 0 5px #00FF41;
    }

    /* ডিভাইডার */
    hr {
        border: 1px solid #00FF41 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📟 CYBER DOWNLOADER TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>[ System Status: Ready | Protocol: Data Extraction ]</p>", unsafe_allow_html=True)

url = st.text_input("> ENTER SOURCE URL:", placeholder="https://...")

if st.button("EXECUTE EXTRACTION"):
    if url:
        try:
            with st.spinner('Accessing server...'):
                ydl_opts_info = {'format': 'best'}
                with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Target_File')
                    video_desc = info.get('description', 'No description found in metadata.')

                col1, col2 = st.columns([1.5, 1])

                with col1:
                    st.subheader("📺 VISUAL FEED")
                    st.video(url)
                    st.markdown(f"**FILE_NAME:** `{video_title}`")

                with col2:
                    st.subheader("📝 METADATA")
                    st.text_area("RAW DATA:", value=video_desc, height=350)

                st.divider()

                st.subheader("📥 EXPORT PROTOCOLS")
                dl_col1, dl_col2 = st.columns(2)

                # ভিডিও ডাউনলোড
                with dl_col1:
                    video_fn = f"cyber_video_{int(time.time())}.mp4"
                    with st.spinner('Compiling MP4...'):
                        ydl_v = {'format': 'best', 'outtmpl': video_fn}
                        with yt_dlp.YoutubeDL(ydl_v) as ydl:
                            ydl.download([url])
                        with open(video_fn, "rb") as f:
                            st.download_button(
                                label="DOWNLOAD VIDEO (MP4)",
                                data=f,
                                file_name=f"{video_title}.mp4",
                                mime="video/mp4",
                                key="v_dl"
                            )
                        os.remove(video_fn)

                # অডিও ডাউনলোড
                with dl_col2:
                    audio_fn = f"cyber_audio_{int(time.time())}.mp3"
                    with st.spinner('Compiling MP3...'):
                        ydl_a_simple = {'format': 'bestaudio', 'outtmpl': audio_fn}
                        with yt_dlp.YoutubeDL(ydl_a_simple) as ydl:
                            ydl.download([url])
                        with open(audio_fn, "rb") as f:
                            st.download_button(
                                label="DOWNLOAD AUDIO (MP3)",
                                data=f,
                                file_name=f"{video_title}.mp3",
                                mime="audio/mpeg",
                                key="a_dl"
                            )
                        os.remove(audio_fn)

        except Exception as e:
            st.error(f"SYSTEM_ERROR: {str(e)}")
    else:
        st.warning("ERROR: No URL detected!")

st.markdown("<br><hr><p style='text-align: center; font-size: 12px;'>AUTHORIZED ACCESS ONLY | PROJECT BY GEMINI AI</p>", unsafe_allow_html=True)
