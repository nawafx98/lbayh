import streamlit as st
import openai
import random  # Import the random module
import os  # Import the random module
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")


# Add a logo image
logo_image = "dd29fded-8d76-4f83-b3a9-ae38d43de7d3.png"  # Replace with your logo image path
st.image(logo_image, width= 60)

st.title("عاطف - مستشار العافية")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Add emojis to the initial responses
initial_responses = [
    "مرحبًا! أنا مستشارك عاطف 😊، تم تطويري بأيدي فريق لبيه وأنا جاهز لمساعدتك. ماذا تحتاج؟",
    "مرحبًا، أنا مستشارك المبني على الذكاء الاصطناعي عاطف 😄. كيف يمكنني أن أكون في خدمتك؟",
    "مرحبًا! أنا هنا لمساعدتك 😊، ماذا تحتاج؟",
]

# Add emojis to the button labels
if st.button("Clear Chat 🗑️"):
    st.session_state.messages = []

if not st.session_state.messages:
    # Select a random initial response
    initial_response = random.choice(initial_responses)
    st.session_state.messages.append({"role": "assistant", "content": initial_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("قل مرحبا 👋"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if st.button("Export Chat"):
    chat_text = "\n".join(
        [f"{message['role']}: {message['content']}" for message in st.session_state.messages]
    )
    st.download_button("Download Chat", data=chat_text, file_name="chat.txt")
