import sqlite3

conn = sqlite3.connect('ativos.db')
cursor = conn.cursor()

# Verifique as colunas da tabela 'equipment_equipamento'
cursor.execute("PRAGMA table_info(equipment_equipamento)")
columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()
