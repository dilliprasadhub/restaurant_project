from supabase import create_client

import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('supabase_url')
key = os.getenv('supabase_key')

db=create_client(url,key)