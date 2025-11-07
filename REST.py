from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "auto_database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к столбцам по имени
    return conn

# ==============================
# Контроллер для дилеров (manufacturers)
# ==============================

@app.route('/api/dealers', methods=['GET'])
def get_all_dealers():
    conn = get_db_connection()
    dealers = conn.execute('SELECT * FROM manufacturers').fetchall()
    conn.close()
    return jsonify([dict(row) for row in dealers])

@app.route('/api/dealers/<int:dealer_id>', methods=['GET'])
def get_dealer_by_id(dealer_id):
    conn = get_db_connection()
    dealer = conn.execute('SELECT * FROM manufacturers WHERE id = ?', (dealer_id,)).fetchone()
    conn.close()
    if dealer is None:
        return jsonify({'error': 'Dealer not found'}), 404
    return jsonify(dict(dealer))

# ==============================
# Контроллер для автомобилей (cars)
# ==============================

@app.route('/api/cars', methods=['GET'])
def get_all_cars():
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()
    return jsonify([dict(row) for row in cars])

@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    conn = get_db_connection()
    car = conn.execute('SELECT * FROM cars WHERE id = ?', (car_id,)).fetchone()
    conn.close()
    if car is None:
        return jsonify({'error': 'Car not found'}), 404
    return jsonify(dict(car))

# ==============================
# Запуск сервера
# ==============================
if __name__ == '__main__':
    app.run(debug=True)

#http://127.0.0.1:5000/api/dealers → все дилеры

#http://127.0.0.1:5000/api/dealers/1 → дилер с id = 1

#http://127.0.0.1:5000/api/cars → все автомобили

#http://127.0.0.1:5000/api/cars/1 → автомобиль с id = 1