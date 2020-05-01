import sqlite3

conn = sqlite3.connect('aids.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS aids(active_substance text, aids_name text,         
                                                release_form text,farm_group text,
                                                target text,animal text,
                                                dosage text,ways_to_use text,                                
                                                how_often text,source text)""")