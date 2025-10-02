import os
import streamlit as st
from supabase import create_client

# Default: None
SUPABASE_URL = None
SUPABASE_KEY = None

# Try Streamlit secrets (for deployed app)
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    # Fallback: local .env via config.py
    from config import SUPABASE_URL, SUPABASE_KEY

class Database:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_client(self):
        return self.client
