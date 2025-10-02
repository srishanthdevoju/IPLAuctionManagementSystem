from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

class Database:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def get_client(self):
        return self.client