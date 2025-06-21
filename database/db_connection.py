# PostgreSQL connection logic

import psycopg2
from config import DB_SETTINGS

def get_connection():
    return psycopg2.connect(**DB_SETTINGS)