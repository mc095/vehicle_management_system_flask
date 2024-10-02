from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'abc'  # Needed for session management

# Connect to SQLite
def get_db_connection():
    conn = sqlite3.connect('vehicles.db')  # SQLite uses a file-based database
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userID = request.form['userID']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
        phone = request.form['phone']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new user into the database
        cursor.execute('''
            INSERT INTO users_list (userID, password, email, city, phone_number) 
            VALUES (?, ?, ?, ?, ?)
        ''', (userID, password, email, city, phone))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration successful! Please log in.")
        return redirect(url_for('registration_success')) 
    
    return render_template("registration_form.html")

@app.route('/registration_success')
def registration_success():
    return render_template("registration_success.html")

@app.route('/login', methods=['POST'])
def login_user():
    userID = request.form['userID']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check user credentials
    cursor.execute('''
        SELECT userID FROM users_list WHERE userID = ? AND password = ?
    ''', (userID, password))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        # Pass a success message to the template
        user_name = user['userID']
        message = "Login successful!"
        return render_template('login_success.html', user_name=user_name, message=message)
    else:
        # Pass an error message to the login page
        message = "Invalid credentials. Please try again."
        return render_template('login.html', message=message)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        try:
            
            vehicle_name = request.form['vehicleName']
            vehicle_type = request.form['vehicleType']
            license_number = request.form['licenseNumber']
            seating_capacity = request.form['seatingCapacity']
            purchase_date = request.form['purchaseDate']

            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert new vehicle into the vehicle_list table
            cursor.execute('''
                INSERT INTO vehicle_list (vehicleName, vehicleType, licenseNumber, seatingCapacity, purchaseDate)
                VALUES (?, ?, ?, ?, ?)
            ''', (vehicle_name, vehicle_type, license_number, seating_capacity, purchase_date))

            conn.commit()
            cursor.close()
            conn.close()

            # Set a success message in the session
            session['message'] = 'Vehicle added successfully!'
            return redirect(url_for('login_success'))  # Redirect to the success page
        except KeyError as e:
            return f"Missing field: {str(e)}", 400
    else:
        # Handle GET request - display the form to add a vehicle
        return render_template('add_vehicle.html')
    
    
@app.route('/view_vehicles')
def view_vehicles():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all vehicles from the vehicle_list table
    cursor.execute('SELECT * FROM vehicle_list')
    vehicles = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view_vehicles.html', vehicles=vehicles)


@app.route('/login_success')
def login_success():
    # Get the user name from the session if you are using session to store user info
    user_name = session.get('user_name', 'User')  # Default to 'User' if not set
    # Get the message from the session
    message = session.pop('message', None)  # Remove message after accessing it
    return render_template('login_success.html', user_name=user_name, message=message)

@app.route('/display_vehicle', methods=['GET', 'POST'])
def display_vehicle():
    vehicle = None  # Initialize vehicle variable
    if request.method == 'POST':
        license_number = request.form['licenseNumber']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch vehicle details based on the license number
        cursor.execute('SELECT * FROM vehicle_list WHERE licenseNumber = ?', (license_number,))
        vehicle = cursor.fetchone()

        cursor.close()
        conn.close()

        if not vehicle:
            flash("No vehicle found with that license number.")
    
    return render_template('display_vehicle.html', vehicle=vehicle)

@app.route('/search_route', methods=['GET', 'POST'])
def search_route():
    if request.method == 'GET':
        user_name = session.get('user_name')  # Assuming you store user_name in session
        city = session.get('city')  # Assuming you store city in session
        return render_template('search_route.html', user_name=user_name, city=city)
    # Handle POST request logic for searching routes here if needed


@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
