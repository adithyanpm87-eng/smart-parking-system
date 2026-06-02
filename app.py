from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "smartparking_secret_key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root@adithyan'
app.config['MYSQL_DB'] = 'smartparking'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM parking_slots")
    slots = cur.fetchall()
    cur.close()

    return render_template('index.html', slots=slots)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(username, password, role) VALUES(%s,%s,%s)",
            (username, hashed_password, 'user')
        )
        mysql.connection.commit()
        cur.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]

            if user[3] == 'admin':
                return redirect('/admin')
            return redirect('/')

        return "Invalid username or password"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        return redirect('/login')

    slot_id = request.form['slot_id']
    vehicle_number = request.form['vehicle_number']

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO bookings(slot_id, vehicle_number) VALUES(%s,%s)",
        (slot_id, vehicle_number)
    )

    cur.execute(
        "UPDATE parking_slots SET status='Booked' WHERE id=%s",
        (slot_id,)
    )

    mysql.connection.commit()
    cur.close()

    return render_template('success.html')


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            bookings.id,
            parking_slots.slot_number,
            bookings.vehicle_number,
            bookings.booking_time
        FROM bookings
        JOIN parking_slots
        ON bookings.slot_id = parking_slots.id
        ORDER BY bookings.booking_time DESC
    """)

    history = cur.fetchall()
    cur.close()

    return render_template('history.html', history=history)


@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied. Admin only."

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM parking_slots")
    slots = cur.fetchall()

    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.close()

    return render_template('admin.html', slots=slots, bookings=bookings, users=users)


@app.route('/add_slot', methods=['POST'])
def add_slot():
    slot = request.form['slot']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO parking_slots(slot_number,status) VALUES(%s,%s)",
        (slot, 'Available')
    )
    mysql.connection.commit()
    cur.close()

    return redirect('/admin')


@app.route('/delete_slot/<int:id>', methods=['POST'])
def delete_slot(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM parking_slots WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect('/admin')


@app.route('/update_slot/<int:id>', methods=['POST'])
def update_slot(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT status FROM parking_slots WHERE id=%s", (id,))
    slot = cur.fetchone()

    if slot[0] == "Available":
        new_status = "Booked"
    else:
        new_status = "Available"

    cur.execute(
        "UPDATE parking_slots SET status=%s WHERE id=%s",
        (new_status, id)
    )

    mysql.connection.commit()
    cur.close()

    return redirect('/admin')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
