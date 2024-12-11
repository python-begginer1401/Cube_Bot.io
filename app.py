import gradio as gr
import google.generativeai as genai
import time

# Define a placeholder variable for the API key
GOOGLE_API_KEY = None

# Transform Gradio history to Gemini format
def transform_history(history, system_prompt):
    new_history = []
    new_history.append({"parts": [{"text": system_prompt}], "role": "user"})
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history

# Function to handle API key input
def set_api_key(key):
    global GOOGLE_API_KEY
    GOOGLE_API_KEY = key
    genai.configure(api_key=GOOGLE_API_KEY)
    return "API Key Set Successfully ✅"

# Define the chat model
def initialize_chat_model():
    if not GOOGLE_API_KEY:
        return None
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    return model.start_chat(history=[])

chat = None  # Initialize chat variable globally

def response(message, history):
    global chat
    if chat is None:
        chat = initialize_chat_model()
        if chat is None:
            yield "Please enter a valid API Key in the sidebar before proceeding!"
            return

    # System prompt for Cube Bot
    system_prompt = """
    you are a cubing algorithm fetcher you will give the user the cubing algorithm to the case they give you...
    [Truncated system prompt for brevity; replace with full prompt in implementation]
    """
    chat.history = transform_history(history, system_prompt)
    response = chat.send_message(message)
    response.resolve()

    # Display the response character by character
    for i in range(len(response.text)):
        time.sleep(0.005)
        yield response.text[: i + 20]

# Gradio UI
with gr.Blocks() as app:
    with gr.Row():
        with gr.Column(scale=3):
            chat_interface = gr.ChatInterface(
                response,
                title="Cube_Bot.io",
                textbox=gr.Textbox(
                    placeholder="What case do you need help solving? (for example OLL 50)"
                ),
                retry_btn=None,
            )
        with gr.Column(scale=1):
            with gr.Row():
                api_key_sidebar = gr.Textbox(
                    label="Enter Google API Key in Sidebar",
                    placeholder="Your API Key here",
                    type="password",
                )
                api_status_sidebar = gr.Textbox(
                    label="Status", interactive=False, value="API Key Required"
                )
                set_key_button = gr.Button("Set API Key")
                set_key_button.click(
                    set_api_key, inputs=api_key_sidebar, outputs=api_status_sidebar
                )

app.launch(debug=True)
