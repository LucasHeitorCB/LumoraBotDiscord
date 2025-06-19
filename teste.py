# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("🔑 DEEPSEEK_API_KEY:", os.getenv("DEEPSEEK_API_KEY"))
