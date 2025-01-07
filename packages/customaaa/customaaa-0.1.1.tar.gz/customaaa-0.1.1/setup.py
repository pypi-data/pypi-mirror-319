from setuptools import setup, find_packages

setup(
    name="customaaa",
    version="0.1.1",  # Increment version number
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.31.0',
        'openai>=1.55.0',
        'python-dotenv>=1.0.0',
        'httpx>=0.26.0,<0.29.0',
        'huggingface_hub>=0.19.0',
        'supabase>=2.11.0'
    ],
)
