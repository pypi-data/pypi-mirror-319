from huggingface_hub import HfApi, create_repo, upload_file, add_space_variable
import os

class FAQAssistant:
    def __init__(self, hf_token: str, openai_api_key: str):
        self.hf_token = hf_token
        self.openai_api_key = openai_api_key
        self.config = None
        self.api = HfApi(token=hf_token)

    def configure(self, 
                 # Required OpenAI Settings
                 assistant_id: str,
                 
                 # Branding & Identity
                 agent_name: str,
                 agent_subtitle: str,
                 logo_url: str = None,
                 primary_color: str = "#6B46C1",
                 secondary_color: str = "#FF7F50",
                 
                 # Chat Interface
                 welcome_message: str = None,
                 chat_input_placeholder: str = "Ask me anything...",
                 thinking_message: str = "Thinking...",
                 typing_speed: float = 0.01,
                 
                 # UI Elements
                 page_icon: str = "🤖",
                 user_avatar: str = None,
                 assistant_avatar: str = None,
                 
                 # Conversation Flow
                 conversation_starters: list = None,
                 
                 # Demo Website
                 demo_website: bool = False,
                 demo_website_config: dict = None):
        """Configure the FAQ Assistant with specific settings."""
        
        self.config = {
            "ASSISTANT_ID": assistant_id,
            "AVATAR_CONFIG": {
                "user": user_avatar or "https://tezzyboy.s3.amazonaws.com/avatars/user_20241221_183530_c2d3a83c.svg",
                "assistant": assistant_avatar or "https://tezzyboy.s3.amazonaws.com/avatars/avatar_20241221_180909_5c30ae3f.svg"
            },
            "LOGO_URL": logo_url,
            "AGENT_NAME": agent_name,
            "AGENT_SUBTITLE": agent_subtitle,
            "WELCOME_MESSAGE": welcome_message or f"Hello! I'm {agent_name}. How can I assist you today?",
            "CHAT_INPUT_PLACEHOLDER": chat_input_placeholder,
            "CONVERSATION_STARTERS": conversation_starters or [
                {"text": "Who are you?", "id": "id1"},
                {"text": "What can you help me with?", "id": "id2"}
            ],
            "PAGE_ICON": page_icon,
            "PRIMARY_COLOR": primary_color,
            "SECONDARY_COLOR": secondary_color,
            "THINKING_MESSAGE": thinking_message,
            "TYPING_SPEED": typing_speed,
        }
        
        self.demo_website = demo_website
        self.demo_website_config = demo_website_config or {}
        
        return self

    def _write_file(self, filename: str, content: str):
        """Write content to a temporary file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_config_file(self) -> str:
        """Generate config.py content."""
        config_content = "# OpenAI Assistant Configuration\n"
        for key, value in self.config.items():
            config_content += f"{key} = {repr(value)}\n\n"
        return config_content

    def _get_app_content(self) -> str:
        """Get the content for app.py"""
        return '''import streamlit as st
import time
from openai import OpenAI
import os
from config import *  # Import all configurations
from customcss1 import CUSTOM_CSS

my_secret = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=my_secret)

# Thinking Animation
THINKING_DOTS = ["", ".", "..", "..."]
THINKING_INTERVAL = 0.5  # seconds

def ensure_single_thread_id():
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    return st.session_state.thread_id

def get_avatar(role):
    return AVATAR_CONFIG.get(role)

def get_assistant_response(prompt, thread_id, assistant_id):
    message_placeholder = st.empty()
    i = 0

    # Create message
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    # Start streaming
    stream = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        stream=True
    )

    full_response = ""

    # Stream the response
    for event in stream:
        if not full_response:
            message_placeholder.markdown(f"*Thinking{THINKING_DOTS[i % len(THINKING_DOTS)]}*", unsafe_allow_html=True)
            i += 1
            time.sleep(THINKING_INTERVAL)

        if event.data.object == "thread.message.delta":
            for content in event.data.delta.content:
                if content.type == 'text':
                    full_response += content.text.value
                    formatted_response = f'<div class="fade-in assistant-message">{full_response}▌</div>'
                    message_placeholder.markdown(formatted_response, unsafe_allow_html=True)
                    time.sleep(0.01)

    # Final display without cursor
    formatted_response = f'<div class="fade-in assistant-message">{full_response}</div>'
    message_placeholder.markdown(formatted_response, unsafe_allow_html=True)
    return full_response

st.set_page_config(page_icon=PAGE_ICON)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(f"""
    <div class="logo-container">
        <img src="{LOGO_URL}" alt="Logo" class="round-logo">
        <div class="concierge-header">{AGENT_NAME}</div>
        <div class="concierge-subtitle">{AGENT_SUBTITLE}</div>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_starter_selected" not in st.session_state:
    st.session_state.conversation_starter_selected = False
if "conversation_starter" not in st.session_state:
    st.session_state.conversation_starter = ""

# Add initial welcome message only once
if 'welcome_message_displayed' not in st.session_state:
    st.session_state.messages.append({"role": "assistant", "content": WELCOME_MESSAGE})
    st.session_state.welcome_message_displayed = True

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"], avatar=get_avatar(message["role"])):
        if idx == 0 and message["role"] == "assistant":
            st.markdown(f'<div class="fade-in">{message["content"]}</div>', unsafe_allow_html=True)
            # Conversation starter buttons
            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                for starter in CONVERSATION_STARTERS:
                    if st.button(starter["text"]):
                        st.session_state.conversation_starter = starter["text"]
                        st.session_state.conversation_starter_selected = True
        else:
            st.markdown(message["content"], unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input(CHAT_INPUT_PLACEHOLDER)
if st.session_state.conversation_starter_selected and not prompt:
    prompt = st.session_state.conversation_starter
    st.session_state.conversation_starter_selected = False

if prompt:
    with st.chat_message("user", avatar=get_avatar("user")):
        st.markdown(prompt, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    thread_id = ensure_single_thread_id()

    with st.chat_message("assistant", avatar=get_avatar("assistant")):
        assistant_response = get_assistant_response(prompt, thread_id, ASSISTANT_ID)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})'''

    def _get_css_content(self) -> str:
        """Get the content for customcss1.py"""
        return '''CUSTOM_CSS = """
    /* Hide default elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Basic resets and container setup */
    .reportview-container .main .block-container {
        padding-top: 0;
        max-width: 700px;
        padding-right: 1rem;
        padding-left: 1rem;
    }

    /* Animations */
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }

    /* Logo and header styling */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 0;
        padding-top: 0.5rem;
    }

    .round-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-top: 0.5rem;
        padding: 2px;
        opacity: 0;
        animation: fadeIn 1.5s ease-out forwards;
        object-fit: cover;
        aspect-ratio: 1 / 1;
        overflow: hidden;
    }

    .concierge-header {
        font-size: 1.25rem;
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-weight: 500;
    }

    .concierge-subtitle {
        text-align: center;
        font-size: 0.9rem;
        margin-top: 0.25rem;
        margin-bottom: 0.5rem;
        padding: 4px 12px;
        border-radius: 4px;
        animation: highlightText 7s ease-in-out infinite;
        display: inline-block;
    }

    /* Chat styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding-bottom: 70px;
    }

    .stChatMessage {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 1.5rem !important;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    .assistant-message {
        width: 100% !important;
        max-width: 100% !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: #ffffff !important;
        color: #1E88E5 !important;
        border: 1px solid #E3E3E3 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
        font-weight: normal !important;
        width: 90% !important;
        margin: 0 auto !important;
        box-shadow: none !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #FF7F50 !important;
        color: white !important;
        border-color: #FF7F50 !important;
        transform: translateY(-1px);
    }

    /* Chat input styling */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        border-top: none !important;
        box-shadow: none !important;
    }
"""'''

    def _generate_requirements(self) -> str:
        """Generate requirements.txt content."""
        return '''streamlit==1.31.0
openai==1.55.0
python-dotenv==1.0.0
httpx>=0.26.0,<0.29.0
supabase==2.11.0'''

    def _generate_gitignore(self) -> str:
        """Generate .gitignore content."""
        return '''.env
__pycache__/
*.pyc
.DS_Store'''

    def deploy(self, hf_username: str, space_name: str, deploy_demo: bool = True, demo_space_name: str = None):
        if not self.config:
            raise ValueError("Assistant must be configured before deployment")

        space_id = f"{hf_username}/{space_name}"
        result = DeploymentResult(
            assistant_url=f"https://huggingface.co/spaces/{space_id}",
            space_status="deploying"
        )

        try:
            # Deploy main assistant
            self._deploy_assistant(space_id)
            result.space_status = "deployed"
            
            # Deploy demo website if requested
            if self.demo_website and deploy_demo:
                demo_space_id = f"{hf_username}/{demo_space_name or f'demo-{space_name}'}"
                demo_url = self._deploy_demo_website(demo_space_id)
                result.demo_url = demo_url
                
                # Create integration guide
                guide_url = self._create_integration_guide(space_id)
                result.integration_guide_url = guide_url

            return result

        except Exception as e:
            print(f"Error in deployment: {str(e)}")
            result.space_status = "error"
            raise
