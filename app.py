import streamlit as st
import google.generativeai as genai
import time

try:
    import google.generativeai as genai
except ImportError:
    st.error("Please install `google-generativeai` library using `pip install google-generativeai`.")

# Sidebar for API Key input and navigation
with st.sidebar:
    st.title("Navigation")
    tabs = st.radio("Select an option", ["🏠 Home", "📝 Cube Solver"])

    api_key = st.text_input("Google API Key", type="password")

# Initialize session states for handling actions
if "history" not in st.session_state:
    st.session_state["history"] = []
if "chat" not in st.session_state:
    st.session_state["chat"] = None

def transform_history(history, system_prompt):
    new_history = []
    new_history.append({"parts": [{"text": system_prompt}], "role": "user"})
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history

# Main Home Tab
if tabs == "🏠 Home":
    st.title("🐍 Cube Solver")
    st.write("""
        Welcome to Cube Solver! 
        Provide your cube case and get the algorithm to solve it.
    """)

# Cube Solver Tab
elif tabs == "📝 Cube Solver":
    st.title("📝 Cube Solver")
    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar.")
    else:
        # Configure Google Gemini AI
        genai.configure(api_key=api_key)
        if st.session_state["chat"] is None:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            st.session_state["chat"] = model.start_chat(history=[])

        message = st.text_input("Enter your cube case (for example OLL 50)", key="message_input")
        system_prompt = """
        you are a cubing algorithm fetcher you will give the user the cubing algorithm to the case they give you and respond in no more than 150 words make sure that the algorithm you give them is written with cubing notations for example OLL 50
        r' U r2 U' r2 U' r2 U r' also make sure the algorithms are correct also this is only for 3 by 3 cubes Here Are all of the oll cases so you don't get confused : 
        [Include your list of algorithms here]
        """

        if st.button("Get Algorithm"):
            try:
                chat = st.session_state["chat"]
                chat.history = transform_history(st.session_state["history"], system_prompt)
                response = chat.send_message(message)
                response.resolve()

                algorithm = response.text
                st.session_state["history"].append((message, algorithm))

                st.write("### Response")
                st.write(algorithm)

                st.write("### History")
                for i, (user_msg, bot_msg) in enumerate(st.session_state["history"]):
                    st.write(f"**User:** {user_msg}")
                    st.write(f"**Bot:** {bot_msg}")

            except Exception as e:
                st.error(f"Error during translation: {e}")

        if st.button("Clear History"):
            st.session_state["history"] = []

# Optionally, you can have a placeholder for the list of algorithms and replace [Include your list of algorithms here] with the actual algorithms
