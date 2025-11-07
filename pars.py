import json
import sqlite3

# === 1. Загружаем JSON ===
with open("dilers .json", "r", encoding="utf-8") as f:
    manufacturers = json.load(f)

with open("cars .json", "r", encoding="utf-8") as f:
    cars = json.load(f)
    cars = cars["cars"]

# === 2. Создаём базу данных ===
conn = sqlite3.connect("auto_database.db")
cursor = conn.cursor()

# === 3. Таблицы ===

# Таблица с производителями / автосалонами
cursor.execute("""
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    city TEXT,
    address TEXT,
    area TEXT,
    rating REAL
)
""")

# Таблица с машинами
cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firm TEXT,
    model TEXT,
    year INTEGER,
    power INTEGER,
    color TEXT,
    price REAL,
    manufacturer_id INTEGER,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
)
""")

# === 4. Заполняем таблицы ===

# Производители
cursor.executemany("""
INSERT OR IGNORE INTO manufacturers (name, city, address, area, rating)
VALUES (:Name, :City, :Address, :Area, :Rating)
""", manufacturers)

# Теперь добавляем машины
for car in cars:
    # ищем id производителя по названию фирмы
    cursor.execute("SELECT id FROM manufacturers WHERE name = ?", (car["firm"],))
    result = cursor.fetchone()
    manufacturer_id = result[0] if result else None

    cursor.execute("""
    INSERT INTO cars (firm, model, year, power, color, price, manufacturer_id)
    VALUES (:firm, :model, :year, :power, :color, :price, :manufacturer_id)
    """, {**car, "manufacturer_id": manufacturer_id})

conn.commit()

# === 5. Проверим ===

print("=== Производители ===")
for row in cursor.execute("SELECT * FROM manufacturers"):
    print(row)

print("\n=== Машины (с привязкой к производителю) ===")
for row in cursor.execute("""
SELECT cars.model, cars.firm, cars.year, cars.price, manufacturers.city
FROM cars
LEFT JOIN manufacturers ON cars.manufacturer_id = manufacturers.id
"""):
    print(row)

conn.close()
print("\n База сохранена в файле 'auto_database.db'")
