import streamlit as st
import psutil
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googlesearch import search
from PIL import Image, ImageDraw
import os
import datetime
import sys
import random
import time
from twilio.rest import Client
import tweepy
import cv2
import numpy as np
from PIL import Image


# Try to import pywhatkit, handle connection errors gracefully
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except Exception as e:
    PYWHATKIT_AVAILABLE = False
    st.warning(f"WhatsApp functionality unavailable: {str(e)}")

st.title("🧪 Python Mini Projects")
st.markdown("Here you can explore various small Python projects:")


# Tabs for all tools
tabs = st.tabs([
    "🔍 Read RAM", "📱 WhatsApp", "📧 Email", 
    "📩 SMS & Call", "🌐 Google Search", "📸 Post to Social Media",
    "⬇️ Website Scraper", "📘 Tuple vs List", "💼 LinkedIn Message",
    "🖼️ Digital Image"
])

# 1. RAM Monitor
with tabs[0]:
    st.header("🔍 RAM Monitor")
    ram = psutil.virtual_memory()
    st.write(f"Total: {ram.total / (1024**3):.2f} GB")
    st.write(f"Available: {ram.available / (1024**3):.2f} GB")
    st.write(f"Used: {ram.used / (1024**3):.2f} GB")
    st.write(f"Usage: {ram.percent}%")

# 2. WhatsApp
with tabs[1]:
    st.header("📱 Send WhatsApp Message")
    if not PYWHATKIT_AVAILABLE:
        st.error("WhatsApp functionality is not available due to connection issues.")
        st.info("Please check your internet connection and restart the app.")
    else:
        number = st.text_input("Enter Phone Number (with +91 etc.)")
        msg = st.text_area("Message")
        delay = st.slider("Send in how many minutes from now?", 1, 10, 2)
        if st.button("Schedule WhatsApp Message"):
            now = datetime.datetime.now()
            send_hour = now.hour
            send_minute = now.minute + delay
            try:
                # send instantly (may still open a browser tab)
                pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=2, tab_close=True)
                # pywhatkit.sendwhatmsg(number, msg, send_hour, send_minute)
                st.success(f"Message scheduled for {send_hour}:{send_minute:02d} via WhatsApp Web")
            except Exception as e:
                st.error(str(e))

  
# 3. Email with SMTP_SSL
with tabs[2]:
    st.header("📧 Send Email (Secure SSL)")
    sender = "naveenchundawat55@gmail.com"
    pwd = "icet ovqf tgxh dabp"  # App Password
    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    content = st.text_area("Body")

    if st.button("Send Email via Gmail SSL"):
        msg = MIMEMultipart()
        msg['From'], msg['To'], msg['Subject'] = sender, recipient, subject
        msg.attach(MIMEText(content, 'plain'))
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender, pwd)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()
            st.success("Email sent successfully via SSL (Port 465)")
        except Exception as e:
            st.error(str(e))



# 4. SMS & Call
with tabs[3]:
    st.header("📩 SMS and 📞 Call with Python")

    # Twilio Credentials (replace with secure env vars in real use)
    account_sid = st.text_input("Twilio SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Twilio Phone Number", value="+1415XXXXXXX")
    target_number = st.text_input("Target Phone Number", value="+91XXXXXXXXXX")
    sms_message = st.text_area("SMS Content")

    if st.button("Send SMS"):
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=sms_message,
                from_=twilio_number,
                to=target_number
            )
            st.success(f"SMS sent! SID: {message.sid}")
        except Exception as e:
            st.error(str(e))

    st.subheader("📞 Make a Call")
    
    if st.button("Make Call"):
        try:
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                twiml='<Response><Say>This is a test call from your Python application.</Say></Response>',
                from_=twilio_number,
                to=target_number
            )
            st.success(f"Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(str(e))



# 5. Google Search
with tabs[4]:
    st.header("🌐 Google Search with Python")
    query = st.text_input("Enter search query")
    if st.button("Search"):
        results = list(search(query, num_results=5))
        for i, link in enumerate(results):
            st.write(f"{i+1}. {link}")

# 6. Post to Instagram/X/Facebook
with tabs[5]:

    st.header("📸 Post to Twitter (X) with Python")    
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_secret = "YOUR_ACCESS_SECRET"

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth)

    tweet = st.text_area("Write your Tweet", max_chars=280)

    if st.button("Post Tweet"):
      if tweet.strip() == "":
        st.warning("⚠️ Tweet cannot be empty.")
      else:
        try:
            api.update_status(tweet)
            st.success("✅ Tweet posted successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# 7. Website Scraper
with tabs[6]:
    st.header("⬇️ Website Data Downloader")
    url = st.text_input("Enter website URL")
    if st.button("Download Data"):
        try:
            data = requests.get(url).text
            with open("site_data.html", "w", encoding="utf-8") as f:
                f.write(data)
            st.success("Website data saved to site_data.html")
        except Exception as e:
            st.error(str(e))

# 8. Tuple vs List
with tabs[7]:
    st.header("📘 Tuple vs List")
    st.write("**Tuple**: Immutable, faster, memory-efficient")
    st.write("**List**: Mutable, flexible, supports more operations")
    st.write("**List size:**", sys.getsizeof([1, 2, 3]))
    st.write("**Tuple size:**", sys.getsizeof((1, 2, 3)))

# 9. LinkedIn Message
with tabs[8]:
    # Your LinkedIn Access Token (OAuth 2.0)
    ACCESS_TOKEN = "YOUR_LINKEDIN_ACCESS_TOKEN"
    URN = "urn:li:person:YOUR_PROFILE_ID"  # Replace with your LinkedIn Profile URN

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    post_text = st.text_area("✍️ Write your LinkedIn post here", max_chars=3000)

    if st.button("Post to LinkedIn"):
        if post_text.strip() == "":
            st.warning("⚠️ Post cannot be empty.")
        else:
            payload = {
                "author": URN,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }

            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers,
                json=payload
            )

            if response.status_code == 201:
                st.success("✅ Post published to LinkedIn!")
            else:
                st.error(f"❌ Failed: {response.text}")

# 10. Digital Image
with tabs[9]:
    st.header("🖼️ Create Digital Image")
    img = Image.new("RGB", (200, 100), color=(0, 100, 200))
    draw = ImageDraw.Draw(img)
    draw.text((20, 40), "Streamlit Image", fill=(255, 255, 255))
    img.save("custom_image.png")
    st.image("custom_image.png")

    # Add random art image
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    for _ in range(200):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(20, 100)
        y2 = y1 + random.randint(20, 100)
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        draw.rectangle([x1, y1, x2, y2], fill=color, outline=None)

    image.save("abstract_art.png")
    st.image("abstract_art.png")

