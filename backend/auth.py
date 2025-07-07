import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

admin_user = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")
if not admin_password:
    raise ValueError("ADMIN_PASSWORD environment variable not set")
admin_pass_hash = generate_password_hash(admin_password)

def check_login(username, password):
    return username == admin_user and check_password_hash(admin_pass_hash, password)
