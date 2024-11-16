from flask import Flask, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'manyamf'
app.config['MYSQL_DB'] = 'minorprojectauth'

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        return '', 200
    else:
        return '', 401

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return '', 409

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    mysql.connection.commit()

    session['user_id'] = cursor.lastrowid
    return '', 200

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Fetch user data and render the dashboard
        return render_template('dashboard.html')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
