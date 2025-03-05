from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your_secret_key'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1908',
    'database': 'college2' 
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE email=%s AND password=%s", (email, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid email or password'
    return render_template('admin_login.html', error=error)

@app.route('/admindashboard')
def admin_dashboard():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM college")
    colleges = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admindashboard.html', colleges=colleges)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        aadhaar = request.form['aadhaar']
        address = request.form['address']
        city = request.form['city']
        district = request.form['district']
        pincode = request.form['pincode']
        school_12th = request.form['school_12th']
        board_12th = request.form['board_12th']
        marks_math = request.form['marks_math']
        marks_physics = request.form['marks_physics']
        marks_chemistry = request.form['marks_chemistry']
        cutoff = request.form['cutoff']
        community = request.form['community']
        tamil_medium = request.form.get('tamil_medium', 'No')
        first_graduate = request.form.get('first_graduate', 'No')
        preferred_college = request.form['preferred_college']
        preferred_course = request.form['preferred_course']
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql_query = '''
            INSERT INTO student (name, dob, gender, email, phone, aadhaar, address, city, district, pincode,
                                 school_12th, board_12th, marks_math, marks_physics, marks_chemistry, cutoff, community,
                                 tamil_medium, first_graduate, preferred_college, preferred_course)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (name, dob, gender, email, phone, aadhaar, address, city, district, pincode,
                  school_12th, board_12th, marks_math, marks_physics, marks_chemistry, cutoff, community,
                  tamil_medium, first_graduate, preferred_college, preferred_course)
        cursor.execute(sql_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('register_success'))
    return render_template('register.html')

@app.route('/registersuccess')
def register_success():
    return render_template('registersuccess.html')

@app.route('/add_college', methods=['POST'])
def add_college():
    college_name = request.form['collegeName']
    affiliation = request.form['affiliation']
    location = request.form['location']
    branch = request.form['branch']
    seats = int(request.form['seats'])
    tnea_code = int(request.form['tnea_code'])
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO college (collegename, affiliation, location, branch, seats, tnea_code) VALUES (%s, %s, %s, %s, %s, %s)",
                   (college_name, affiliation, location, branch, seats, tnea_code))
    conn.commit()
    cursor.close()
    conn.close()
    flash("College added successfully!", "success")
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
