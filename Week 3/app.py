import sqlite3
import time


DATABASE_FILE = 'clinic.db'

def get_db_conn():
    """Membuka koneksi baru ke database SQLite."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row 
    return conn

# --- FUNGSI PRINT ---

def print_all_doctors():
    print("--- Isi Tabel Doctor ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    if not doctors:
        print("  [Kosong]")
    for doc in doctors:
        print(f"  ID: {doc['doctorID']}, Nama: {doc['firstName']} {doc['lastName']}, Spesialis: {doc['specialization']}")
    conn.close()
    print("---------------------------------")

def print_all_patients():
    print("--- Isi Tabel Patient ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    if not patients:
        print("  [Kosong]")
    for p in patients:
        print(f"  ID: {p['patientID']}, Nama: {p['firstName']} {p['lastName']}, Email: {p['emailAddress']}")
    conn.close()
    print("----------------------------------")

def print_all_appointments():
    print("--- Isi Tabel Appointment ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM appointment")
    apps = cursor.fetchall()
    if not apps:
        print("  [Kosong]")
    for app in apps:
        print(f"  ID: {app['appointmentID']}, PasienID: {app['patientID']}, DokterID: {app['doctorID']}, Status: {app['status']}")
    conn.close()
    print("--------------------------------------")

def print_all_clinics():
    print("--- Isi Tabel Clinic ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM clinic")
    items = cursor.fetchall()
    if not items:
        print("  [Kosong]")
    for item in items:
        print(f"  ID: {item['clinicID']}, Nama: {item['clinicName']}, Kota: {item['city']}, Alamat: {item['address']}")
    conn.close()
    print("----------------------------------")

def print_all_rooms():
    print("--- Isi Tabel Room ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM room")
    items = cursor.fetchall()
    if not items:
        print("  [Kosong]")
    for item in items:
        print(f"  ID: {item['roomID']}, Nama: {item['roomName']}, Kapasitas: {item['capacity']}, ClinicID: {item['clinicID']}")
    conn.close()
    print("----------------------------------")

def print_all_doctor_clinics():
    print("--- Isi Tabel doctor_clinic (Relasi) ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM doctor_clinic")
    items = cursor.fetchall()
    if not items:
        print("  [Kosong]")
    for item in items:
        print(f"  DokterID: {item['doctorID']}, ClinicID: {item['clinicID']}")
    conn.close()
    print("----------------------------------")

def print_all_doctor_phones():
    print("--- Isi Tabel doctor_phoneNumber ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM doctor_phoneNumber")
    items = cursor.fetchall()
    if not items:
        print("  [Kosong]")
    for item in items:
        print(f"  DokterID: {item['doctorID']}, No.Telp: {item['phoneNumber']}")
    conn.close()
    print("----------------------------------")

def print_all_patient_phones():
    print("--- Isi Tabel patient_phoneNumber ---")
    conn = get_db_conn()
    cursor = conn.execute("SELECT * FROM patient_phoneNumber")
    items = cursor.fetchall()
    if not items:
        print("  [Kosong]")
    for item in items:
        print(f"  PasienID: {item['patientID']}, No.Telp: {item['phoneNumber']}")
    conn.close()
    print("----------------------------------")

# --- FUNGSI CRUD: DOCTOR ENTITY ---

def add_doctor(doctor_id, first_name, last_name, specialization):
    print(f"[C] Menambahkan dokter: {first_name} {last_name}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO doctor (doctorID, firstName, lastName, specialization) VALUES (?, ?, ?, ?)",
        (doctor_id, first_name, last_name, specialization)
    )
    conn.commit()
    conn.close()

def get_doctor_by_id(doctor_id):
    print(f"[R] Mencari dokter ID: {doctor_id}")
    conn = get_db_conn()
    doc = conn.execute("SELECT * FROM doctor WHERE doctorID = ?", (doctor_id,)).fetchone()
    conn.close()
    return doc

def update_doctor_specialization(doctor_id, new_specialization):
    print(f"[U] Mengupdate spesialisasi dokter ID {doctor_id} menjadi '{new_specialization}'")
    conn = get_db_conn()
    conn.execute(
        "UPDATE doctor SET specialization = ? WHERE doctorID = ?",
        (new_specialization, doctor_id)
    )
    conn.commit()
    conn.close()

def delete_doctor(doctor_id):
    # print(f"[D] Menghapus dokter ID: {doctor_id}")
    conn = get_db_conn()
    conn.execute("DELETE FROM doctor WHERE doctorID = ?", (doctor_id,))
    conn.commit()
    conn.close()

# --- FUNGSI CRUD: PATIENT ENTITY ---

def add_patient(patient_id, first_name, last_name, email):
    print(f"[C] Menambahkan pasien: {first_name} {last_name}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO patient (patientID, firstName, lastName, emailAddress) VALUES (?, ?, ?, ?)",
        (patient_id, first_name, last_name, email)
    )
    conn.commit()
    conn.close()

def get_patient_by_id(patient_id):
    print(f"[R] Mencari pasien ID: {patient_id}")
    conn = get_db_conn()
    patient = conn.execute("SELECT * FROM patient WHERE patientID = ?", (patient_id,)).fetchone()
    conn.close()
    return patient

def update_patient_email(patient_id, new_email):
    print(f"[U] Mengupdate email pasien ID {patient_id} menjadi '{new_email}'")
    conn = get_db_conn()
    conn.execute(
        "UPDATE patient SET emailAddress = ? WHERE patientID = ?",
        (new_email, patient_id)
    )
    conn.commit()
    conn.close()

def delete_patient(patient_id):
    # print(f"[D] Menghapus pasien ID: {patient_id}")
    conn = get_db_conn()
    conn.execute("DELETE FROM patient WHERE patientID = ?", (patient_id,))
    conn.commit()
    conn.close()

# --- FUNGSI CRUD: APPOINTMENT ENTITY ---

def add_appointment(app_id, date, time, status, patient_id, doctor_id, room_id):
    print(f"[C] Menjadwalkan appointment ID: {app_id}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO appointment (appointmentID, date, time, status, patientID, doctorID, roomID) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (app_id, date, time, status, patient_id, doctor_id, room_id)
    )
    conn.commit()
    conn.close()

def update_appointment_status(app_id, new_status):
    print(f"[U] Mengupdate status appointment ID {app_id} menjadi '{new_status}'")
    conn = get_db_conn()
    conn.execute(
        "UPDATE appointment SET status = ? WHERE appointmentID = ?",
        (new_status, app_id)
    )
    conn.commit()
    conn.close()

def delete_appointment(app_id):
    # print(f"[D] Membatalkan (menghapus) appointment ID: {app_id}")
    conn = get_db_conn()
    conn.execute("DELETE FROM appointment WHERE appointmentID = ?", (app_id,))
    conn.commit()
    conn.close()

# --- FUNGSI CRUD: CLINIC & ROOM ENTITIES ---

def add_clinic(clinic_id, name, city, address):
    print(f"[C] Menambahkan klinik: {name}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO clinic (clinicID, clinicName, city, address) VALUES (?, ?, ?, ?)",
        (clinic_id, name, city, address)
    )
    conn.commit()
    conn.close()

def add_room(room_id, name, capacity, clinic_id):
    print(f"[C] Menambahkan ruang: {name} ke klinik ID {clinic_id}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO room (roomID, roomName, capacity, clinicID) VALUES (?, ?, ?, ?)",
        (room_id, name, capacity, clinic_id)
    )
    conn.commit()
    conn.close()

def update_room_capacity(room_id, new_capacity):
    print(f"[U] Mengupdate kapasitas ruang ID {room_id} menjadi {new_capacity}")
    conn = get_db_conn()
    conn.execute(
        "UPDATE room SET capacity = ? WHERE roomID = ?",
        (new_capacity, room_id)
    )
    conn.commit()
    conn.close()

def delete_room(room_id):
    # print(f"[D] Menghapus ruang ID: {room_id}")
    conn = get_db_conn()
    conn.execute("DELETE FROM room WHERE roomID = ?", (room_id,))
    conn.commit()
    conn.close()

# --- FUNGSI CRUD: RELATIONSHIP & MULTIVALUED ---

def add_doctor_to_clinic(doctor_id, clinic_id):
    print(f"[C] Menghubungkan dokter ID {doctor_id} ke klinik ID {clinic_id}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO doctor_clinic (doctorID, clinicID) VALUES (?, ?)",
        (doctor_id, clinic_id)
    )
    conn.commit()
    conn.close()

def add_phone_to_patient(patient_id, phone_number):
    print(f"[C] Menambahkan nomor telepon ke pasien ID {patient_id}")
    conn = get_db_conn()
    conn.execute(
        "INSERT INTO patient_phoneNumber (patientID, phoneNumber) VALUES (?, ?)",
        (patient_id, phone_number)
    )
    conn.commit()
    conn.close()

def remove_doctor_from_clinic(doctor_id, clinic_id):
    # print(f"[D] Menghapus hubungan dokter ID {doctor_id} dari klinik ID {clinic_id}")
    conn = get_db_conn()
    conn.execute(
        "DELETE FROM doctor_clinic WHERE doctorID = ? AND clinicID = ?",
        (doctor_id, clinic_id)
    )
    conn.commit()
    conn.close()

def remove_phone_from_patient(patient_id, phone_number):
    # print(f"[D] Menghapus nomor telepon pasien ID {patient_id}")
    conn = get_db_conn()
    conn.execute(
        "DELETE FROM patient_phoneNumber WHERE patientID = ? AND phoneNumber = ?",
        (patient_id, phone_number)
    )
    conn.commit()
    conn.close()


# --- BAGIAN UTAMA ---

if __name__ == "__main__":
    
    print("===== DEMO =====")
    time.sleep(2)

    # --- DEMO DOCTOR ---
    print("\n\n===== DEMO ENTITAS: DOCTOR =====")
    print_all_doctors() # Tampilkan awal (kosong)
    add_doctor(1, 'Chelsea', 'Natasja', 'Surgeon')
    print_all_doctors() # Tampilkan setelah C
    doc = get_doctor_by_id(1)
    print(f"  Hasil GetByID: {doc['firstName']} {doc['lastName']} adalah seorang {doc['specialization']}")
    update_doctor_specialization(1, 'Pediatrics')
    print_all_doctors() # Tampilkan setelah U

    # --- DEMO PATIENT ---
    print("\n\n===== DEMO ENTITAS: PATIENT =====")
    print_all_patients() # Tampilkan awal
    add_patient(101, 'Siti', 'Aminah', 'siti.a@example.com')
    print_all_patients() # Tampilkan setelah C
    update_patient_email(101, 'siti.aminah@newdomain.com')
    pat = get_patient_by_id(101)
    print(f"  Hasil GetByID: Email baru pasien adalah {pat['emailAddress']}")
    print_all_patients() # Tampilkan setelah U

    # --- DEMO CLINIC & ROOM ---
    print("\n\n===== DEMO ENTITAS: CLINIC & ROOM =====")
    print_all_clinics() # Tampilkan awal
    print_all_rooms() # Tampilkan awal
    add_clinic(1, 'Klinik Sehat Utama', 'Yogyakarta', 'Jl. Malioboro 1')
    add_room(12, 'Ruang Periksa 1', 1, 1)
    print_all_clinics() # Tampilkan setelah C
    print_all_rooms() # Tampilkan setelah C
    update_room_capacity(12, 2)
    print_all_rooms() # Tampilkan setelah U

    # --- DEMO APPOINTMENT ---
    print("\n\n===== DEMO ENTITAS: APPOINTMENT =====")
    print_all_appointments() # Tampilkan awal
    add_appointment(1001, '2025-11-20', '10:00:00', 'Scheduled', 101, 1, 12)
    print_all_appointments() # Tampilkan setelah C
    update_appointment_status(1001, 'Completed')
    print_all_appointments() # Tampilkan setelah U

    # --- DEMO RELATIONSHIP & MULTIVALUED ---
    print("\n\n===== DEMO ENTITAS: RELATIONSHIP & MULTIVALUED =====")
    print_all_doctor_clinics() # Tampilkan awal
    print_all_patient_phones() # Tampilkan awal
    add_doctor_to_clinic(1, 1)
    add_phone_to_patient(101, '08123456789')
    print("  [C] Data relasi & multivalued berhasil ditambahkan.")
    print_all_doctor_clinics() # Tampilkan setelah C
    print_all_patient_phones() # Tampilkan setelah C


    # --- CLEANUP ---
    print("\n\n===== CLEANUP DATA DEMO =====")
    
    # Hapus data dalam urutan terbalik (anak dulu baru induk)
    remove_phone_from_patient(101, '08123456789')
    remove_doctor_from_clinic(1, 1)
    delete_appointment(1001)
    delete_patient(101)
    delete_doctor(1)
    delete_room(12)
    
    # Hapus clinic (baru bisa setelah room dihapus)
    conn = get_db_conn()
    conn.execute("DELETE FROM clinic WHERE clinicID = 1")
    conn.commit()
    conn.close()
    
    print("===== DEMO SELESAI =====")