import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Ultimate Downloader", page_icon="🚀", layout="wide")

# কাস্টম CSS ডিজাইন
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড গ্র্যাডিয়েন্ট অ্যানিমেশন */
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

    /* গ্লাস কার্ড ইফেক্ট */
    .main-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        color: white;
    }

    /* বাটন ডিজাইন */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background: white !important;
        color: #e73c7e !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* ইনপুট ফিল্ড স্টাইল */
    .stTextInput>div>div>input {
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.9);
    }
    
    h1, h2, h3, p, label {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# কন্টেন্ট শুরু
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.title("🚀 আল্টিমেট ভিডিও ও অডিও হাব")
st.write("আপনার পছন্দের ভিডিওর লিঙ্কটি দিন এবং ম্যাজিক দেখুন!")

url = st.text_input("🔗 ভিডিও লিঙ্কটি এখানে দিন:", placeholder="https://youtube.com/...")

if url:
    try:
        with st.spinner('✨ জাদুর মতো তথ্য সংগ্রহ করা হচ্ছে...'):
            # তথ্য সংগ্রহের সময় ব্রাউজারের মতো ছদ্মবেশ নেওয়ার অপশন
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

            st.markdown(f"### 🎥 {video_title}")
            st.video(url)
            
            with st.expander("ℹ️ ভিডিওর বিস্তারিত তথ্য"):
                st.write(f"👤 **আপলোডার:** {uploader}")
                st.write(f"👁️ **মোট ভিউ:** {view_count:,}")
                st.markdown("---")
                st.text_area("ডেসক্রিপশন:", video_description, height=200)

            st.success("✅ তথ্য লোড হয়েছে! নিচের অপশন বেছে নিন।")
    except Exception as e:
        st.error("⚠️ তথ্য আনা সম্ভব হয়নি। লিঙ্কটি সঠিক কিনা চেক করুন।")

st.markdown("---")
st.write("### 📁 ডাউনলোড ফরম্যাট")
format_choice = st.radio("", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)

if st.button("📥 ডাউনলোড প্রসেস শুরু করুন"):
    if url:
        try:
            with st.spinner('⚙️ প্রসেসিং হচ্ছে... কিছুক্ষণ অপেক্ষা করুন।'):
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
                    final_filename = "downloaded_audio.mp3"
                else:
                    ydl_opts.update({
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': 'downloaded_video.mp4',
                        'merge_output_format': 'mp4',
                    })
                    final_filename = "downloaded_video.mp4"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                with open(final_filename, "rb") as file:
                    st.download_button(
                        label=f"💾 {format_choice} সেভ করুন",
                        data=file,
                        file_name=f"Download_{final_filename}",
                        mime="video/mp4" if "video" in final_filename else "audio/mp3"
                    )
                st.balloons()
        except Exception as e:
            st.error(f"❌ ভুল হয়েছে: {e}")
    else:
        st.warning("⚠️ আগে একটি লিঙ্ক দিন।")

st.markdown('</div>', unsafe_allow_html=True)
