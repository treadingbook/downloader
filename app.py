import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Cyber Video Downloader", page_icon="📟", layout="wide")

# হ্যাকার টাইপ স্টাইল (CSS)
st.markdown("""
    <style>
    /* ডার্ক এবং হ্যাকার ব্যাকগ্রাউন্ড */
    .stApp {
        background-color: #000000;
        background-image: linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px), 
                          linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace;
    }

    /* মেইন কন্টেইনার বক্স */
    .main-box {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 35px;
        border-radius: 10px;
        border: 1px solid #00FF41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        backdrop-filter: blur(5px);
        margin-bottom: 80px; /* ফুটারের জন্য জায়গা */
    }

    /* টাইটেল এবং সব টেক্সট কালার গ্রিন */
    h1, h2, h3, p, label, .stMarkdown {
        color: #00FF41 !important;
        text-shadow: 0 0 5px #00FF41;
    }

    /* ইনপুট বক্স স্টাইল */
    .stTextInput>div>div>input {
        background-color: #050505 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        font-family: 'Courier New', monospace;
    }

    /* হ্যাকার টাইপ বাটন */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3.5em;
        background: transparent !important;
        color: #00FF41 !important;
        font-weight: bold;
        border: 1px solid #00FF41 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00FF41 !important;
        color: black !important;
        box-shadow: 0 0 20px #00FF41;
    }

    /* ফুটার সেকশন (ক্রেডিট) */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.95);
        color: #00FF41;
        text-align: center;
        padding: 15px;
        border-top: 2px solid #00FF41;
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
        z-index: 100;
    }
    .footer a {
        color: #fff;
        text-decoration: none;
        background: #004d1a;
        padding: 2px 8px;
        border-radius: 4px;
        transition: 0.3s;
    }
    .footer a:hover {
        background: #00FF41;
        color: #000;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>📟 CYBER VIDEO TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>[ ACCESSING SECURE DATA EXTRACTION PROTOCOL ]</p>", unsafe_allow_html=True)
st.markdown("---")

url = st.text_input("> ENTER VIDEO SOURCE URL:", placeholder="Paste link here...")

if url:
    try:
        with st.spinner('📡 EXTRACTING METADATA...'):
            # ৪0৩ এরর এড়াতে ইউজার এজেন্ট যুক্ত করা হয়েছে
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

            st.subheader(f"🎬 TARGET: {video_title}")
            st.video(url)
            
            with st.expander("📝 VIEW RAW METADATA"):
                st.write(f"**UPLOADER:** {uploader}")
                st.write(f"**VIEWS:** {view_count}")
                st.markdown("---")
                st.text(video_description) 

            st.success("SUCCESS: DATA PACKETS READY FOR EXTRACTION.")
    except Exception as e:
        st.error(f"ERROR: SYSTEM FAILURE - {e}")

st.markdown("---")
format_choice = st.radio("> SELECT EXPORT FORMAT:", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)

if st.button("EXECUTE DOWNLOAD"):
    if url:
        try:
            with st.spinner('⚡ DOWNLOADING DATA...'):
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
                        'outtmpl': 'cyber_audio.%(ext)s',
                    })
                else:
                    ydl_opts.update({
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': 'cyber_video.mp4',
                        'merge_output_format': 'mp4',
                    })

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_data = ydl.extract_info(url, download=True)
                    actual_filename = ydl.prepare_filename(info_data)
                    
                    if format_choice == "অডিও (MP3)":
                        actual_filename = actual_filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')

                with open(actual_filename, "rb") as file:
                    st.download_button(
                        label=f"💾 SAVE {format_choice} TO DISK",
                        data=file,
                        file_name=os.path.basename(actual_filename),
                        mime="video/mp4" if "video" in actual_filename else "audio/mp3"
                    )
                st.balloons()
        except Exception as e:
            st.error(f"FATAL ERROR: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# --- আপনার স্টাইলিশ ক্রেডিট সেকশন ---
st.markdown("""
    <div class="footer">
        <p>CORE_DEVELOPER: <a href="আপনার_লিঙ্ক_এখানে">আপনার নাম</a> | 
        PROTOCOL: <span style="color: #fff;">v1.0.4-SECURE</span> | 
        STATUS: <span style="color: #fff;">ENCRYPTED</span></p>
    </div>
    """, unsafe_allow_html=True)
