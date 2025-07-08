import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# Connection function
def get_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in environment")
    return psycopg2.connect(db_url)


# Fetch certificate by UID
def get_certificate_by_uid(uid):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM certificates WHERE uid = %s", (uid,))
    cert = cur.fetchone()
    cur.close()
    conn.close()
    return cert
