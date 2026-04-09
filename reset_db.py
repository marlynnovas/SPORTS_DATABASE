from database.connection import init_db
from seed_db import seed_data
import os

if __name__ == "__main__":
    db_path = "sports_club.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed old database: {db_path}")
    
    init_db("database/schema.sql")
    seed_data()
    print("Database recreated and seeded.")
