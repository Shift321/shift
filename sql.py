import sqlite3

conn = sqlite3.connect('medicines.db')
cursor = conn.cursor()


def create_data_base():
    cursor.execute("""CREATE TABLE IF NOT EXISTS medicines(active_substance text, medicines_name text,info_of_medicines text)""")