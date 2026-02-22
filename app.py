import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ: টাইটেল এবং আইকন
st.set_page_config(page_title="Ultra Downloader Pro", page_icon="🎬", layout="centered")

# কাস্টম সিএসএস (CSS) দিয়ে স্টাইলিশ লুক তৈরি
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp {
        background: linear-gradient(to right, #1e1e2f, #23233b);
        color: white;
    }
    /* টাইটেল স্টাইল */
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        background: -webkit-linear-gradient(#ff4b4b, #ff8a8a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    /* ইনপুট বক্স */
    .stTextInput>div>div>input {
        background-color: #2d2d44;
        color: white;
        border: 2px solid #ff4b4b;
        border-radius: 10px;
    }
    /* বাটন ডিজাইন */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #ff4b4b, #ff8a8a);
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 15px rgba(255, 75, 75, 0.4);
    }
    /* ইনফো বক্স */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# হেডার সেকশন
st.markdown('<h1 class="main-title">🚀 Ultra Downloader</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>মুহূর্তেই ডাউনলোড করুন আপনার পছন্দের সব মিডিয়া</p>", unsafe_allow_html=True)
st.write("---")

# ইউজার লিঙ্ক ইনপুট
url = st.text_input("🔗 ভিডিওর লিঙ্কটি এখানে পেস্ট করুন:", placeholder="https://youtube.com/...")

if url:
    try:
        with st.spinner('🔍 ভিডিওর তথ্য খোঁজা হচ্ছে...'):
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

            # সুন্দর ভাবে ভিডিও ডিটেইলস দেখানো
            st.info(f"📌 **নাম:** {video_title}")
            st.video(url)
            
            with st.expander("📖 ডেসক্রিপশন পড়তে এখানে ক্লিক করুন"):
                st.write(f"👤 **আপলোডার:** {uploader}")
                st.markdown("---")
                st.write(video_description)

            st.success("✨ ডাউনলোড করার জন্য সব রেডি!")
            
            # ফরম্যাট সিলেকশন
            st.write("### 📁 নিচের অপশন থেকে একটি বেছে নিন:")
            c1, c2 = st.columns(2)
            with c1:
                format_choice = st.radio("", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)
            
            # ডাউনলোড বাটন
            if st.button("📥 প্রসেস ও ডাউনলোড শুরু করুন"):
                try:
                    with st.spinner('⚙️ কনভার্ট হচ্ছে... একটু সময় দিন।'):
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
                                'outtmpl': 'music.%(ext)s',
                            })
                            final_filename = "music.mp3"
                        else:
                            ydl_opts.update({
                                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                                'outtmpl': 'video.mp4',
                                'merge_output_format': 'mp4',
                            })
                            final_filename = "video.mp4"

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])

                        with open(final_filename, "rb") as file:
                            st.download_button(
                                label=f"💾 {format_choice} আপনার ফোনে সেভ করুন",
                                data=file,
                                file_name=f"Ultra_DL_{final_filename}",
                                mime="video/mp4" if "video" in final_filename else "audio/mp3"
                            )
                        st.balloons()
                except Exception as e:
                    st.error(f"❌ এরর: {e}")

    except Exception as e:
        st.error("⚠️ ভিডিওটি পাওয়া যায়নি। লিঙ্কটি পুনরায় চেক করুন।")
else:
    st.write("---")
    st.markdown("<p style='text-align: center; color: #888;'>শুরু করতে উপরে একটি লিঙ্ক দিন।</p>", unsafe_allow_html=True)
