from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE_FILE = 'clinic.db'

# Database setup
def get_db_conn():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# === HALAMAN UTAMA ===
@app.route('/')
def home():
    return render_template('home.html')



# === LOGIN ===
# --- Halaman Login Admin ---
@app.route('/login-admin', methods=['GET', 'POST']) 
def loginAdmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded
        if request.form['password'] == 'admin123':
            return redirect(url_for('admin'))
        else:
            return render_template('login-admin.html', error="Password atau username salah!")
    return render_template('login-admin.html')

# --- Halaman Login Doctors ---
@app.route('/login-doctors', methods=['GET', 'POST'])
def loginDoctors():
    if request.method == 'POST':
        doctor_id = request.form['doctorID']
        
        conn = get_db_conn()
        doctor = conn.execute('SELECT * FROM doctor WHERE doctorID = ?', (doctor_id,)).fetchone()
        conn.close()
        
        if doctor:
            return redirect(url_for('doctors', id=doctor_id))
        else:
            return render_template('login-doctors.html', error="ID Dokter tidak ditemukan!")
            
    return render_template('login-doctors.html')

# --- Halaman Login Patients ---
@app.route('/login-patients', methods=['GET', 'POST'])
def loginPatients():
    if request.method == 'POST':
        patient_id = request.form['patientID']
        
        conn = get_db_conn()
        patient = conn.execute('SELECT * FROM patient WHERE patientID = ?', (patient_id,)).fetchone()
        conn.close()
        
        if patient:
            return redirect(url_for('patients', id=patient_id))
        else:
            return render_template('login-patients.html', error="ID Pasien tidak ditemukan!")
            
    return render_template('login-patients.html')



# === MAIN PAGES ===
# --- Admin ---
# READ
@app.route('/admin')
def admin():
    edit_type = request.args.get('type')
    edit_id = request.args.get('id')

    if edit_id:
        edit_id = int(edit_id)

    conn = get_db_conn()
    doctors = conn.execute('SELECT * FROM doctor ORDER BY doctorID ASC').fetchall()
    patients = conn.execute('SELECT * FROM patient ORDER BY patientID ASC').fetchall()
    clinics = conn.execute('SELECT * FROM clinic ORDER BY clinicID ASC').fetchall()

    rooms = conn.execute('''
        SELECT r.*, c.clinicName 
        FROM room r 
        JOIN clinic c ON r.clinicID = c.clinicID
    ''').fetchall()

    appointments = conn.execute('''
        SELECT a.*, p.firstName as pName, d.firstName as dName, r.roomName 
        FROM appointment a
        JOIN patient p ON a.patientID = p.patientID
        JOIN doctor d ON a.doctorID = d.doctorID
        JOIN room r ON a.roomID = r.roomID
    ''').fetchall()

    conn.close()
    return render_template('admin.html',
                           doctor=doctors,
                           patient=patients,
                           clinic=clinics,
                           room=rooms,
                           appointment=appointments,
                           edit_type=edit_type,
                           edit_id=edit_id)


# CREATE
@app.route('/doctor/add', methods=('POST',))
def add_doctor():
    conn = get_db_conn()
    conn.execute('INSERT INTO doctor (doctorID, firstName, lastName, specialization) VALUES (?, ?, ?, ?)',
                (request.form['doctorID'], request.form['firstName'], request.form['lastName'],
                request.form['specialization']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/patient/add', methods=('POST',))
def add_patient():
    conn = get_db_conn()
    conn.execute('INSERT INTO patient (patientID, firstName, lastName, emailAddress) VALUES (?, ?, ?, ?)',
                (request.form['patientID'], request.form['firstName'], request.form['lastName'],
                request.form['emailAddress']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/clinic/add', methods=('POST',))
def add_clinic():
    conn = get_db_conn()
    conn.execute('INSERT INTO clinic (clinicName, city, address) VALUES (?, ?, ?)',
                (request.form['clinicName'], request.form['city'], request.form['address']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/room/add', methods=['POST'])
def add_room():
    conn = get_db_conn()
    conn.execute('INSERT INTO room (roomID, roomName, capacity, clinicID) VALUES (?, ?, ?, ?)',
                 (request.form['roomID'], 
                  request.form['roomName'], 
                  request.form['capacity'], 
                  request.form['clinicID']))
    
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/appointment/add', methods=['POST'])
def add_appointment():
    conn = get_db_conn()
    conn.execute('''
        INSERT INTO appointment (date, time, status, patientID, doctorID, roomID) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        request.form['date'],
        request.form['time'],
        'Scheduled',
        request.form['patientID'],
        request.form['doctorID'],
        request.form['roomID']
    ))
    
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# UPDATE
@app.route('/doctor/update/<int:id>', methods=('POST',))
def update_doctor(id):
    conn = get_db_conn()
    conn.execute('UPDATE doctor SET firstName = ?, lastName = ?, specialization = ? WHERE doctorID = ?', 
                 (request.form['firstName'], request.form['lastName'], request.form['specialization'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/patient/update/<int:id>', methods=('POST',))
def update_patient(id):
    conn = get_db_conn()
    conn.execute('UPDATE patient SET firstName = ?, lastName = ?, emailAddress = ? WHERE patientID = ?', 
                 (request.form['firstName'], request.form['lastName'], request.form['emailAddress'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/clinic/update/<int:id>', methods=('POST',))
def update_clinic(id):
    conn = get_db_conn()
    conn.execute('UPDATE clinic SET clinicName = ?, city = ?, address = ? WHERE clinicID = ?', 
                 (request.form['clinicName'], request.form['city'], request.form['address'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/room/update/<int:id>', methods=['POST'])
def update_room(id):
    conn = get_db_conn()
    conn.execute('UPDATE room SET roomName = ?, capacity = ?, clinicID = ? WHERE roomID = ?', 
                 (request.form['roomName'], 
                  request.form['capacity'], 
                  request.form['clinicID'],
                  id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/appointment/update/<int:id>', methods=('POST',))
def update_appointment(id):
    conn = get_db_conn()
    conn.execute('UPDATE appointment SET date = ?, time = ?, status = ?,  patientID = ?, doctorID = ?, roomID = ? WHERE appointmentID = ?', 
                (request.form['date'],
                request.form['time'],
                'Scheduled',
                request.form['patientID'],
                request.form['doctorID'],
                request.form['roomID'],
                id
            ))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# DELETE
@app.route('/doctor/hapus/<int:id>', methods=('POST',))
def delete_doctor(id):
    conn = get_db_conn()
    conn.execute('DELETE FROM doctor WHERE doctorID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/patient/hapus/<int:id>', methods=('POST',))
def delete_patient(id):
    conn = get_db_conn()
    conn.execute('DELETE FROM patient WHERE patientID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/clinic/hapus/<int:id>', methods=('POST',))
def delete_clinic(id):
    conn = get_db_conn()
    conn.execute('DELETE FROM clinic WHERE clinicID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/room/delete/<int:id>', methods=['POST'])
def delete_room(id):
    conn = get_db_conn()
    # Kalau ruangan dihapus, appointment yang pakai ruangan ini error/hilang
    conn.execute('DELETE FROM room WHERE roomID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/appointment/hapus/<int:id>', methods=('POST',))
def delete_appointment(id):
    conn = get_db_conn()
    conn.execute('DELETE FROM appointment WHERE appointmentID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


# --- Doctors ---
@app.route('/doctors/<int:id>') 
def doctors(id):
    conn = get_db_conn()

    doctor = conn.execute('SELECT * FROM doctor WHERE doctorID = ?', (id,)).fetchone()
    
    query = '''
        SELECT a.appointmentID, a.date, a.time, a.status, 
               p.firstName || ' ' || p.lastName AS patientName, -- Gabung nama depan & belakang
               r.roomName
        FROM appointment a
        JOIN patient p ON a.patientID = p.patientID
        JOIN room r ON a.roomID = r.roomID
        WHERE a.doctorID = ? 
        ORDER BY a.date DESC, a.time ASC
    '''
    
    appointments = conn.execute(query, (id,)).fetchall()
    conn.close()
    
    return render_template('doctors.html', doctor=doctor, appointments=appointments)

# --- Patient ---
@app.route('/patients/<int:id>') 
def patients(id):
    conn = get_db_conn()

    patient_info = conn.execute('SELECT * FROM patient WHERE patientID = ?', (id,)).fetchone()
    
    doctors_list = conn.execute('SELECT * FROM doctor').fetchall()
    rooms_list = conn.execute('SELECT * FROM room').fetchall()
    patients_list = conn.execute('SELECT * FROM patient').fetchall()

    query = '''
        SELECT a.appointmentID, a.date, a.time, a.status, 
               d.firstName || ' ' || d.lastName AS doctorName, 
               d.specialization,
               r.roomName
        FROM appointment a
        JOIN doctor d ON a.doctorID = d.doctorID
        JOIN room r ON a.roomID = r.roomID
        WHERE a.patientID = ? 
        ORDER BY a.date DESC, a.time ASC
    '''
    appointments = conn.execute(query, (id,)).fetchall()
    conn.close()
    
    return render_template('patients.html', 
                           patient=patient_info, 
                           appointments=appointments,
                           doctor=doctors_list,
                           room=rooms_list,
                           patient_list=patients_list)

# Patient Nambah Appointment
@app.route('/patients/appointment/add', methods=['POST'])
def book_appointment():
    conn = get_db_conn()
    p_id = request.form['patientID'] 
    
    conn.execute('''
        INSERT INTO appointment (date, time, status, patientID, doctorID, roomID) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        request.form['date'],
        request.form['time'],
        'Scheduled',
        p_id,
        request.form['doctorID'],
        request.form['roomID']
    ))
    conn.commit()
    conn.close()
    
    return redirect(url_for('patients', id=p_id))

# Patient Update Appointment
@app.route('/patient/appointment/update/<int:id>', methods=('POST',))
def patient_update_appointment(id):
    conn = get_db_conn()
    
    p_id = request.form['patientID']
    
    conn.execute('UPDATE appointment SET date = ?, time = ?, status = ?,  patientID = ?, doctorID = ?, roomID = ? WHERE appointmentID = ?', 
                (request.form['date'],
                request.form['time'],
                'Scheduled',
                p_id,
                request.form['doctorID'],
                request.form['roomID'],
                id
            ))
    conn.commit()
    conn.close()
    
    return redirect(url_for('patients', id=p_id))

# Patient Hapus Appointment
@app.route('/patient/appointment/hapus/<int:id>', methods=('POST',))
def patient_delete_appointment(id):
    conn = get_db_conn()
    
    appt = conn.execute('SELECT patientID FROM appointment WHERE appointmentID = ?', (id,)).fetchone()
    patient_id = appt['patientID']
    
    conn.execute('DELETE FROM appointment WHERE appointmentID = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('patients', id=patient_id))

if __name__ == '__main__':
    app.run(debug=True)