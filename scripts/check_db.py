import sqlite3

conn = sqlite3.connect('data/seo_affiliate.db')
cursor = conn.cursor()

# Check keywords table schema
cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="keywords"')
result = cursor.fetchone()
if result:
    print('Keywords table schema:')
    print(result[0])
else:
    print('Keywords table does not exist')

# Check all tables
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('\nAll tables:')
for table in tables:
    print(f'- {table[0]}')

conn.close()
