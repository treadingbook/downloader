import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Ultimate Downloader", page_icon="📥")

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

            # ভিডিও প্রিভিউ
            st.subheader(f"🎥 {video_title}")
            st.video(video_url)
            
            # ডেসক্রিপশন ও অন্যান্য তথ্য দেখানোর অংশ
            with st.expander("ভিডিওর বিস্তারিত ডেসক্রিপশন দেখুন"):
                st.write(f"**আপলোডার:** {uploader}")
                st.write(f"**মোট ভিউ:** {view_count}")
                st.markdown("---")
                st.text(video_description) # এখানে পুরো ডেসক্রিপশন দেখা যাবে

            st.success("তথ্য লোড হয়েছে! নিচে ডাউনলোড অপশন বেছে নিন।")
    except Exception as e:
        st.error("তথ্য আনা সম্ভব হয়নি। লিঙ্কটি আবার চেক করুন।")

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
                    
                    # অডিওর ক্ষেত্রে সঠিক নাম নিশ্চিত করা
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
            st.error(f"ভুল হয়েছে: {e}")