import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Streamlit
st.set_page_config(
    page_title="Health Q&A ChatBot",
    page_icon="🩺",
    layout="centered"
)

# ✅ Load Gemini model using flash (faster)
@st.cache_resource
def load_model():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name="models/gemini-1.5-flash")

model = load_model()

# ✅ Single-shot response generator
def get_gemini_response(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ Error from Gemini: {str(e)}"

# ✅ Sample suggestions
health_suggestions = [
    "How to cure fever?",
    "What are the symptoms of dengue?",
    "Home remedies for cold",
    "How to reduce body pain?",
    "What to do for a sore throat?",
    "Tips for healthy skin",
    "How to boost immunity?",
    "Is headache a sign of stress?",
    "Foods to eat during fever",
    "Natural remedies for cough",
    "How to cure asthma?"
]

# ✅ Session state setup
if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ✅ App UI
st.header("🩺 QueueCare Health Assistant")

user_query = st.text_input(
    "Ask your health question:",
    value=st.session_state.user_query,
    placeholder="Start typing...",
    on_change=lambda: st.session_state.update(submitted=True)
)

# ✅ Suggestions
if user_query and not st.session_state.submitted:
    matches = [q for q in health_suggestions if user_query.lower() in q.lower()]
    if matches:
        st.markdown("**Suggestions:**")
        for match in matches:
            if st.button(match):
                st.session_state.user_query = match
                st.rerun()

submit = st.button("Ask")

# ✅ Submission logic
if (submit or st.session_state.submitted) and user_query:
    if len(user_query.split()) > 100:
        st.warning("Please keep your question under 100 words.")
    else:
        with st.spinner("Analyzing your health question..."):
            response = get_gemini_response(user_query)
            st.markdown(response)

    st.session_state.user_query = ""
    st.session_state.submitted = False

elif (submit or st.session_state.submitted) and not user_query:
    st.warning("Please type your health question first.")
    st.session_state.submitted = False
