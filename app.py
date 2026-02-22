import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Ultimate Downloader", page_icon="📥", layout="wide")

# সিএসএস দিয়ে ইন্টারফেস রঙিন করা
st.markdown("""
    <style>
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
    .main-box {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    h1, h2, h3, p, label {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background: white !important;
        color: #e73c7e !important;
        font-weight: bold;
        border: none;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("📥 ভিডিও ডাউনলোডার ও ডিটেইলস")
st.markdown("---")

url = st.text_input("ভিডিও লিঙ্কটি এখানে দিন:", placeholder="https://...")

if url:
    try:
        with st.spinner('ভিডিওর তথ্য আনা হচ্ছে...'):
            # তথ্য সংগ্রহের সময় ৪0৩ এরর এড়াতে cookies বা user-agent ব্যবহার
            ydl_opts_info = {
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url') 
                video_title = info.get('title')
                video_description = info.get('description')
                uploader = info.get('uploader')
                view_count = info.get('view_count')

            st.subheader(f"🎥 {video_title}")
            st.video(url) # সরাসরি লিঙ্ক ব্যবহার করা নিরাপদ
            
            with st.expander("ভিডিওর বিস্তারিত ডেসক্রিপশন দেখুন"):
                st.write(f"**আপলোডার:** {uploader}")
                st.write(f"**মোট ভিউ:** {view_count}")
                st.markdown("---")
                st.text(video_description) 

            st.success("তথ্য লোড হয়েছে! নিচে ডাউনলোড অপশন বেছে নিন।")
    except Exception as e:
        st.error(f"তথ্য আনা সম্ভব হয়নি: {e}")

st.markdown("---")
format_choice = st.radio("কী ফরম্যাটে সেভ করতে চান?", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)

if st.button("ডাউনলোড শুরু করুন"):
    if url:
        try:
            with st.spinner('ডাউনলোড হচ্ছে...'):
                # ডাউনলোড করার সময় ৪0৩ এরর ফিক্স করার অপশন
                ydl_opts = {
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }

                if format_choice == "অডিও (MP3)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'downloaded_audio.%(ext)s',
                    })
                else:
                    ydl_opts.update({
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': 'downloaded_video.mp4',
                        'merge_output_format': 'mp4',
                    })

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

# আপনার ক্রেডিট সেকশন
st.markdown("""
    <div class="footer">
        Developed with ❤️ by <a href="#" style="color: #FFCC70; text-decoration: none;">আপনার নাম</a>
    </div>
    """, unsafe_allow_html=True)
