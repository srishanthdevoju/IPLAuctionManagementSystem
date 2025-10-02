import os
from dotenv import load_dotenv

load_dotenv()

# Try to import streamlit for cloud deployment
try:
    import streamlit as st
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv('SUPABASE_URL'))
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv('SUPABASE_KEY'))
except:
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')