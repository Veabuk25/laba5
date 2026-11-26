# Таблица computers: компьютеры в ремонте
# name     - модель компьютера
# category - вид неисправности
# value    - стоимость ремонта в условных единицах
import sqlite3
from pathlib import Path

folder = Path(__file__).resolve().parent
con = sqlite3.connect(folder / "app.db")

con.execute("""
CREATE TABLE IF NOT EXISTS computers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    value INTEGER
)
""")

data = [
    ("Lenovo ThinkCentre M70q", "Питание", 120),
    ("HP ProDesk 400 G6", "Питание", 85),
    ("Dell OptiPlex 3070", "Питание", 150),
    ("Acer Veriton X2660G", "Питание", 60),
    ("ASUS ExpertCentre D640", "Материнская плата", 210),
    ("Сборка на Gigabyte B450", "Материнская плата", 95),
    ("MSI Cubi 5", "Накопитель", 130),
    ("Apple Mac mini 2018", "Накопитель", 180),
    ("Irbis Nettop 3120", "Материнская плата", 45),
    ("HP EliteDesk 800 G4", "Питание", 110),
]

count = con.execute(
    "SELECT COUNT(*) FROM computers"
).fetchone()[0]

if count == 0: #чтобы при каждом запуске исходные данные не добавлялись заново
    con.executemany(
        "INSERT INTO computers (name, category, value)"
        "VALUES (?, ?, ?)", #места для значений из списка
        data
    )
    con.commit()

print("\nВсе записи:")
rows = con.execute( 
    "SELECT * FROM computers ORDER BY id"
).fetchall()
for row in rows:
    print(row)

chosen_category = "Накопитель" #отбор по категории
print("\nПроблема с накопителем:")
rows = con.execute(
    "SELECT * FROM computers WHERE category = ?",
    (chosen_category,)
).fetchall()
for row in rows:
    print(row)

limit = 120 #отбор по числу
print("\nСтоимость более 120:")
rows = con.execute(
    "SELECT * FROM computers WHERE value > ?",
    (limit,)
).fetchall()
for row in rows:
    print(row)

print("\nСортировка:")
rows = con.execute(
    "SELECT * FROM computers ORDER BY value ASC, id ASC" #ASC задаёт порядок по возрастанию, DESC — по убыванию
).fetchall()
for row in rows:
    print(row)

#изменение 
record_id = 6
new_value = 120

con.execute(
    "UPDATE computers SET value = ? WHERE id = ?",
    (new_value, record_id)
)
con.commit()

print("\nПосле изменения (id = 6, цена 95 -> 120 ):")
print(con.execute(
    "SELECT * FROM computers WHERE id = ?",
    (record_id,)
).fetchone())

record_id = 5 #удаление
con.execute(
    "DELETE FROM computers WHERE id = ?",
    (record_id,)
)
con.commit()

print("\nПосле удаления:")
for row in con.execute("SELECT * FROM computers ORDER BY id"):
    print(row)
con.close()
