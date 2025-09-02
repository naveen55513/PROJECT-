import streamlit as st

st.set_page_config(page_title="👋 Welcome", layout="wide")
st.title("👋 Welcome to the Streamlit App")
st.markdown("Use the sidebar to explore different sections like Python Projects, ML/GenAI apps, JEE AND NEET.")

# First row of buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Python Projects"):
        st.info("Click 'Python Projects' from the sidebar.")

with col2:
    if st.button("🤖 GenAI & ML"):
        st.info("Click 'GenAI & ML' from the sidebar.")

with col3:
    if st.button("JEE AND NEET"):
        st.info("Click 'JEE AND NEET' from the sidebar.")



# App description
st.markdown("---")
st.header("About This App")
st.write("""
This multi-purpose Streamlit application provides various tools and utilities:

- **Python Projects**: Explore Python code examples and projects
- **GenAI & ML**: Interact with generative AI and machine learning models
- **JEE AND NEET** : Find best institute for your exam preparation 

Select any section from the sidebar to get started!
""")

# Footer
st.markdown("---")
st.caption("© 2023 Streamlit Multi-Tool App")