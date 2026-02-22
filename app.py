import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Ultimate Downloader", page_icon="📥", layout="wide")

# শুধুমাত্র স্টাইল (CSS) যোগ করা
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #4158D0, #C850C0, #FFCC70, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    h1, h2, h3, p, label {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background: #ffffff !important;
        color: #C850C0 !important;
        font-weight: bold;
        border: none;
    }
    /* ক্রেডিট সেকশনের স্টাইল */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("📥 ভিডিও ডাউনলোডার ও ডিটেইলস")
st.markdown("---")

url = st.text_input("ভিডিও লিঙ্কটি এখানে দিন:", placeholder="https://...")

if url:
    try:
        with st.spinner('ভিডিওর তথ্য ও ডেসক্রিপশন আনা হচ্ছে...'):
            ydl_opts_info = {'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url') 
                video_title = info.get('title')
                video_description = info.get('description')
                uploader = info.get('uploader')
                view_count = info.get('view_count')

            st.subheader(f"🎥 {video_title}")
            st.video(video_url)
            
            with st.expander("ভিডিওর বিস্তারিত ডেসক্রিপশন দেখুন"):
                st.write(f"**আপলোডার:** {uploader}")
                st.write(f"**মোট ভিউ:** {view_count}")
                st.markdown("---")
                st.text(video_description) 

            st.success("তথ্য লোড হয়েছে! নিচে ডাউনলোড অপশন বেছে নিন।")
    except Exception as e:
        st.error("তথ্য আনা সম্ভব হয়নি। লিঙ্কটি আবার চেক করুন।")

st.markdown("---")
format_choice = st.radio("কী ফরম্যাটে সেভ করতে চান?", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)

if st.button("ডাউনলোড শুরু করুন"):
    if url:
        try:
            with st.spinner('ডাউনলোড হচ্ছে...'):
                if format_choice == "অডিও (MP3)":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'downloaded_audio.%(ext)s',
                    }
                else:
                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': 'downloaded_video.mp4',
                        'merge_output_format': 'mp4',
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_data = ydl.extract_info(url, download=True)
                    actual_filename = ydl.prepare_filename(info_data)
                    
                    if format_choice == "অডিও (MP3)":
                        actual_filename = actual_filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')

                with open(actual_filename, "rb") as file:
                    st.download_button(
                        label=f"💾 {format_choice} সেভ করুন",
                        data=file,
                        file_name=os.path.basename(actual_filename),
                        mime="video/mp4" if "video" in actual_filename else "audio/mp3"
                    )
                st.balloons()
        except Exception as e:
            st.error(f"ভুল হয়েছে: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# --- ক্রেডিট সেকশন (পরিবর্তন করুন এখানে) ---
st.markdown("""
    <div class="footer">
        <p>Developed with ❤️ by <a href="আপনার_লিঙ্ক" style="color: #FFCC70; text-decoration: none;">MD RASHED MIAH</a></p>
    </div>
    """, unsafe_allow_html=True)
