import streamlit as st
import yt_dlp
import os
import time

# পেজ সেটআপ
st.set_page_config(page_title="Ultimate Video Bot", page_icon="🎬", layout="wide")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 অল-ইন-ওয়ান ভিডিও বট</h1>", unsafe_allow_html=True)
st.write("---")

# লিঙ্ক ইনপুট বক্স
url = st.text_input("ভিডিওর লিঙ্কটি এখানে পেস্ট করুন (YouTube, FB, Insta, TikTok):", placeholder="https://...")

if st.button("ভিডিও লোড করুন"):
    if url:
        try:
            with st.spinner('ভিডিও এবং তথ্য লোড হচ্ছে...'):
                # ভিডিওর তথ্য সংগ্রহ (ডাউনলোড ছাড়া)
                ydl_opts_info = {'format': 'best'}
                
                with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'ভিডিওর শিরোনাম')
                    video_description = info.get('description', 'ডেসক্রিপশন পাওয়া যায়নি।')
                    video_url = info.get('url') # সরাসরি স্ট্রিমিং লিঙ্ক

                # স্ক্রিনকে দুই ভাগে ভাগ করা (বাম দিকে প্লেয়ার, ডান দিকে ডেসক্রিপশন)
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.subheader("📺 ভিডিও প্রিভিউ")
                    if video_url:
                        st.video(url) # সরাসরি অরিজিনাল ইউআরএল থেকে প্লে হবে
                    else:
                        st.error("দুঃখিত, এই ভিডিওটি এখানে প্লে করা সম্ভব হচ্ছে না।")

                with col2:
                    st.subheader("📝 ডেসক্রিপশন")
                    st.text_area("কপি করতে নিচের বক্সটি ব্যবহার করুন:", value=video_description, height=350)

                st.write("---")
                
                # ডাউনলোড সেকশন
                st.subheader("⬇️ ডাউনলোড জোন")
                save_filename = f"video_{int(time.time())}.mp4"
                
                # ভিডিওটি ডাউনলোড করা যাতে ইউজার সেভ করতে পারে
                with st.spinner('ডাউনলোড বাটন তৈরি হচ্ছে...'):
                    ydl_opts_dl = {'format': 'best', 'outtmpl': save_filename}
                    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                        ydl.download([url])

                    with open(save_filename, "rb") as file:
                        st.download_button(
                            label="📥 পিসিতে সেভ করুন (Download File)",
                            data=file,
                            file_name=f"{video_title}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                    
                    # টেম্পোরারি ফাইল ডিলিট করা
                    os.remove(save_filename)

        except Exception as e:
            st.error(f"দুঃখিত, ভিডিওটি লোড করা যায়নি। এরর: {str(e)}")
    else:
        st.warning("আগে একটি ভিডিওর লিঙ্ক দিন!")

st.markdown("---")
st.caption("দ্রষ্টব্য: বড় ভিডিওর ক্ষেত্রে ডাউনলোড বাটন আসতে কিছুটা সময় লাগতে পারে।")
