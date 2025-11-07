from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = "auto_database.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

#   Контроллер: Дилеры (manufacturers)

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


# POST
@app.route('/api/dealers', methods=['POST'])
def add_dealer():
    data = request.get_json()
    required_fields = ["name", "city", "address", "area", "rating"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO manufacturers (name, city, address, area, rating)
        VALUES (?, ?, ?, ?, ?)
    """, (data["name"], data["city"], data["address"], data["area"], data["rating"]))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Dealer added', 'id': new_id}), 201


# PUT
@app.route('/api/dealers/<int:dealer_id>', methods=['PUT'])
def update_dealer(dealer_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE manufacturers
        SET name = ?, city = ?, address = ?, area = ?, rating = ?
        WHERE id = ?
    """, (data.get("name"), data.get("city"), data.get("address"),
          data.get("area"), data.get("rating"), dealer_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Dealer updated'})


# DELETE
@app.route('/api/dealers/<int:dealer_id>', methods=['DELETE'])
def delete_dealer(dealer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM manufacturers WHERE id = ?', (dealer_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Dealer {dealer_id} deleted'})


#   Контроллер: Автомобили (cars)

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


# POST
@app.route('/api/cars', methods=['POST'])
def add_car():
    data = request.get_json()
    required_fields = ["firm", "model", "year", "power", "color", "price"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cars (firm, model, year, power, color, price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data["firm"], data["model"], data["year"],
          data["power"], data["color"], data["price"]))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Car added', 'id': new_id}), 201


# PUT
@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cars
        SET firm = ?, model = ?, year = ?, power = ?, color = ?, price = ?
        WHERE id = ?
    """, (data.get("firm"), data.get("model"), data.get("year"),
          data.get("power"), data.get("color"), data.get("price"), car_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Car updated'})


# DELETE
@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Car {car_id} deleted'})

if __name__ == '__main__':
    app.run(debug=True)
