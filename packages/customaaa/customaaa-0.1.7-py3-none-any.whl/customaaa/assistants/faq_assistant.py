from huggingface_hub import HfApi, create_repo, upload_file, add_space_variable
from dataclasses import dataclass, field
from typing import Optional
import os

@dataclass
class DeploymentResult:
    assistant_url: str
    demo_url: str = None
    integration_guide_url: str = None
    space_status: str = None
    build_logs_url: str = None


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
'''


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

    def _create_demo_website_content(self, assistant_url: str) -> str:
        """Create demo website HTML content."""
        embed_url = f"{assistant_url}/?embed=true"
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['AGENT_NAME']} - Demo</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        header {{
            background: linear-gradient(45deg, {self.config.get('PRIMARY_COLOR', '#6B46C1')}, {self.config.get('SECONDARY_COLOR', '#805AD5')});
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        main {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        .feature {{
            background: #f5f5f5;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        .faq-section {{
            margin: 2rem 0;
        }}
        .faq-item {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        {self.demo_website_config.get('custom_css', '')}
    </style>
</head>
<body>
    <header>
        <h1>{self.config['AGENT_NAME']}</h1>
        <p>{self.config['AGENT_SUBTITLE']}</p>
    </header>
    <main>
        <h2>Welcome to Our Knowledge Base</h2>
        <p>{self.demo_website_config.get('description', 'Get instant answers to your questions!')}</p>

        <div class="feature">
            <h3>✨ Key Features</h3>
            <ul>
                {self._generate_features_list()}
            </ul>
        </div>

        <div class="faq-section">
            <h3>Popular Questions</h3>
            {self._generate_faq_items()}
        </div>
    </main>

    <!-- Chat Widget Integration -->
    <script src='https://tezzyboy.s3.amazonaws.com/static/chatwidget_20241231_090506_c82d1b79.js'></script>
    <script>
    initChatWidget({{
        agentName: '{self.config['AGENT_NAME']}',
        agentImage: '{self.config['LOGO_URL']}',
        headerColor: '{self.demo_website_config.get('header_color', '#6B46C1')}',
        buttonColor: '{self.demo_website_config.get('button_color', '#805AD5')}',
        chatbotUrl: '{embed_url}'
    }});
    </script>
</body>
</html>"""

    def _generate_features_list(self) -> str:
        """Generate HTML list of features."""
        features = self.demo_website_config.get('features', [
            "24/7 AI Support",
            "Instant Answers",
            "Smart Assistance"
        ])
        return '\n'.join([f'<li>{feature}</li>' for feature in features])

    def _generate_faq_items(self) -> str:
        """Generate FAQ items HTML."""
        return '\n'.join([
            f'<div class="faq-item"><h4>{starter["text"]}</h4></div>'
            for starter in self.config['CONVERSATION_STARTERS']
        ])

    def _deploy_demo_website(self, space_id: str) -> str:
        """Deploy demo website to a separate Space."""
        try:
            # Try to delete existing demo space
            try:
                self.api.delete_repo(
                    repo_id=space_id,
                    repo_type="space",
                    token=self.hf_token
                )
                print(f"Deleted existing demo space: {space_id}")
            except Exception as e:
                print(f"No existing demo space to delete or error: {e}")

            # Create new space for demo
            create_repo(
                space_id,
                repo_type="space",
                space_sdk="static",
                token=self.hf_token
            )
            print(f"Created demo space: {space_id}")

            # Create and upload index.html
            demo_content = self._create_demo_website_content(
                f"https://huggingface.co/spaces/{space_id}"
            )
            self._write_file('index.html', demo_content)

            # Upload to Hugging Face
            self.api.upload_file(
                path_or_fileobj='index.html',
                path_in_repo='index.html',
                repo_id=space_id,
                repo_type="space"
            )
            print("Uploaded demo website files")

            # Clean up
            os.remove('index.html')

            return f"https://huggingface.co/spaces/{space_id}"

        except Exception as e:
            print(f"Error deploying demo website: {e}")
            return None


def deploy(self, hf_username: str, space_name: str, deploy_demo: bool = True, demo_space_name: str = None):
        """Deploy the assistant and optionally a demo website."""
        if not self.config:
            raise ValueError("Assistant must be configured before deployment")

        space_id = f"{hf_username}/{space_name}"
        result = DeploymentResult(
            assistant_url=f"https://huggingface.co/spaces/{space_id}",
            space_status="deploying"
        )

        try:
            # Try to delete existing space
            try:
                # In the deploy method, add after deploying the main assistant:
                if self.demo_website and deploy_demo:
                    demo_space_id = f"{hf_username}/{demo_space_name or f'demo-{space_name}'}"
                    result.demo_url = self._deploy_demo_website(demo_space_id)
                    if result.demo_url:
                        print(f"Demo website deployed at: {result.demo_url}")
                self.api.delete_repo(
                    repo_id=space_id,
                    repo_type="space",
                    token=self.hf_token
                )
                print(f"Deleted existing space: {space_id}")
            except Exception as e:
                print(f"No existing space to delete or error: {e}")

            # Create new space
            create_repo(
                space_id,
                repo_type="space",
                space_sdk="streamlit",
                token=self.hf_token
            )
            print(f"Created new Space: {space_id}")

            # Add secrets
            add_space_variable(
                repo_id=space_id,
                key="OPENAI_API_KEY",
                value=self.openai_api_key,
                token=self.hf_token
            )
            print("Added OPENAI_API_KEY to Space secrets")

            # Generate and upload files
            files = {
                'app.py': self._get_app_content(),
                'config.py': self._generate_config_file(),
                'customcss1.py': self._get_css_content(),
                'requirements.txt': self._generate_requirements(),
                '.gitignore': self._generate_gitignore()
            }

            for filename, content in files.items():
                # Write file locally
                self._write_file(filename, content)
                
                # Upload to Hugging Face
                self.api.upload_file(
                    path_or_fileobj=filename,
                    path_in_repo=filename,
                    repo_id=space_id,
                    repo_type="space"
                )
                print(f"Uploaded {filename}")

                # Clean up local file
                os.remove(filename)

            result.space_status = "deployed"

            return result

        except Exception as e:
            print(f"Error in deployment: {str(e)}")
            result.space_status = "error"
            raise


