import sqlite3

c = sqlite3.connect("database.db")
cu = c.cursor()

f = "SELECT count(*) FROM lego ORDER BY id"
fat = cu.execute(f)
print(fat.fetchall())