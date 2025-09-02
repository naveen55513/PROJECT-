import streamlit as st

st.title("🤖 GenAI & ML Projects")

api_key = "enter your api key "

st.markdown("Explore GenAI (Gemini) and Machine Learning models.")

st.subheader("AI Chatbot")
st.write("A simple chatbot using the Gemini API.")

import streamlit as st
import requests


# Tabs for all tools
tabs = st.tabs([ "🤖 GenAI","📈 Linear Regression","💬 Sentiment Analysis"
    
])

# 1. "🤖 GenAI"
with tabs[0]:
    API_KEY = "enter your api key" # <--- REPLACE THIS WITH YOUR ACTUAL API KEY

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# App UI
    st.title("✨ General Purpose AI Chatbot (Gemini 2.5 Flash)")
    st.markdown("""
Ask me anything! I'm powered by Google's Gemini 2.5 Flash AI and can answer a wide range of questions.
""")

# Input
    user_input = st.text_area("What's on your mind?", placeholder="e.g. Explain quantum computing in simple terms.", height=100)

# Button
    if st.button("Ask Gemini"):
        if not user_input.strip():
            st.warning("Please enter a question to ask the AI.")
        elif API_KEY == "YOUR_GEMINI_API_KEY" or not API_KEY.strip():
            st.error("api key ")
            st.info("You can get an API key from [Google AI Studio](https://makersuite.google.com/)."
                    "\n\n**Note:** For deployment, consider using Streamlit Secrets for API keys.")
        else:
            with st.spinner("Gemini is thinking... 🧠"):
                system_prompt_content = f"""
                You are a helpful and knowledgeable AI assistant. Your goal is to provide concise, accurate, and easy-to-understand answers.
                
                Based on the user's question, provide a direct answer. If you don't know the answer, state that you don't know rather than hallucinating.
    
                User's Question: {user_input}
                """
    
                headers = {
                    "Content-Type": "application/json"
                }
    
                params = {
                    "key": API_KEY
                }
    
                payload = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": system_prompt_content}]
                        }
                    ]
                }
    
               
                try:
                    response = requests.post(
                        BASE_URL,
                        headers=headers,
                        params=params,
                        json=payload
                    )
    
                    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    
                    output = response.json()
                    reply = output["candidates"][0]["content"]["parts"][0]["text"]
                    
                    st.success("Answer:")
                    st.markdown(reply)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error making request to Gemini API: {str(e)}")
                except KeyError as e:
                    st.error(f"Error parsing API response: {str(e)}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
    # Footer
    st.markdown("""
    ---
    👨‍💻 Built by Naveen Singh Chundawat · Powered by Gemini 2.5 Flash
    """)


# 2. "📈 Linear Regression"
with tabs[1]:
    
    col1, col2 = st.columns(2)

    with col1:
        import streamlit as st
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression
               
        df = pd.DataFrame({
              'HOUSE SIZE': [1330, 1200, 1250, 800, 0, 10, 100],  # Fixed typo: SIVE -> SIZE
              'PRICE': [10000000, 9000000, 9500000, 7500000, 0, 250000, 2500000]
            })
               
               
        df = df[df['HOUSE SIZE'] > 0] 
        df = df[df['PRICE'] > 0]
        df.columns = df.columns.str.strip()
        X = df[["HOUSE SIZE"]]  
        y = df[["PRICE"]]
        model = LinearRegression()
        model.fit(X, y)
        st.title("🏠 House Price Prediction")
               
        if st.checkbox("Show Training Data"):
                   st.dataframe(df)
               
               # User input
        house_size = st.number_input("Enter House Size (sq ft):", min_value=0.0, step=1.0)
               
        if st.button("Predict Price"):
                if house_size > 0:
                       prediction = model.predict([[house_size]])[0][0]
                       st.success(f"Estimated Price: ₹{prediction:,.2f}")
                else:
                       st.error("Please enter a house size greater than 0")
           
  
  
    with col2:
        import streamlit as st
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression
            
        da = pd.DataFrame({
                'EXPRINCE': [13, 5, 1.2, 8, 0, 1, 10],  # Fixed typo: SIVE -> SIZE
                'SALARE': [100000, 60000, 9500, 75000, 0, 2500, 95000]
            })
            
        da = da[da['EXPRINCE'] > 0] 
        da = da[da['SALARE'] > 0]
            
        da.columns = da.columns.str.strip()
        X = da[["EXPRINCE"]]  
        y = da[["SALARE"]]
            
        model = LinearRegression()
        model.fit(X, y)
            
        st.title("🏠 SALARE PREDICTION")
            
        if st.checkbox("Show Training Data" ,key = '1'):
                st.dataframe(da)
            
            # User input
        exprince = st.number_input("Enter Exprince :", min_value=0.0, step=1.0)
            
        if st.button("Predict Salare"):
                if exprince > 0:
                    prediction = model.predict([[exprince]])[0][0]
                    st.success(f"Estimated Price: ₹{prediction:,.2f}")
                else:
                    st.error("Please enter a exprince greater than 0")




# 3. 💬 Sentiment Analysis

with tabs[2]:
    st.subheader("💬 Sentiment Analysis")
    import streamlit as st
    from textblob import TextBlob
    
    
    # Input text
    sentence = st.text_area("Enter a sentence to analyze:")
    
    if st.button("Analyze"):
        if sentence.strip() != "":
            snet_inp = TextBlob(sentence)
            sub = snet_inp.sentiment.subjectivity
            pol = snet_inp.sentiment.polarity
            
            st.success(f"✅ Polarity: {pol:.2f}")
            st.info(f"📝 Subjectivity: {sub:.2f}")
            
            # Extra: give sentiment meaning
            if pol > 0:
                st.write("🙂 Positive sentiment")
            elif pol < 0:
                st.write("☹️ Negative sentiment")
            else:
                st.write("😐 Neutral sentiment")
        else:
            st.warning("⚠️ Please enter a sentence first.")
    
