import sqlite3

class DoctorDatabaseManager:
    def __init__(self, db_path="doctor.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_doctor_table()
        self.seed_dummy_doctors()

    def create_doctor_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS doctors (
            id TEXT PRIMARY KEY,
            name TEXT,
            specialization TEXT,
            availability TEXT,
            timing TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_doctor(self, id, name, specialization, availability, timing):
        self.conn.execute(
            "INSERT OR IGNORE INTO doctors (id, name, specialization, availability, timing) VALUES (?, ?, ?, ?, ?)",
            (id, name, specialization, availability, timing),
        )
        self.conn.commit()

    def get_doctors_by_specialization(self, specialization):
        specialization = specialization.strip().lower()

        # Try direct LIKE match first
        cursor = self.conn.execute(
            "SELECT * FROM doctors WHERE LOWER(specialization) LIKE ?",
            ('%' + specialization + '%',)
        )
        rows = cursor.fetchall()

        # If no match found, apply custom fuzzy matching logic
        if not rows:
            all_doctors = self.get_all_doctors()
            rows = [
                (
                    doc["id"], doc["name"], doc["specialization"],
                    doc["available_day"], doc["available_time"]
                )
                for doc in all_doctors
                if specialization in doc["specialization"].lower()
                   or doc["specialization"].lower() in specialization
            ]

        doctors = []
        for row in rows:
            doctors.append({
                "id": row[0],
                "name": row[1],
                "specialization": row[2],
                "available_day": row[3],
                "available_time": row[4]
            })
        return doctors

    def get_all_doctors(self):
        cursor = self.conn.execute("SELECT * FROM doctors")
        rows = cursor.fetchall()
        doctors = []
        for row in rows:
            doctors.append({
                "id": row[0],
                "name": row[1],
                "specialization": row[2],
                "available_day": row[3],
                "available_time": row[4]
            })
        return doctors

    def seed_dummy_doctors(self):
        doctors = [
            ("dr_001", "Dr. Ravi Kumar", "General Medicine", "Mon,Tue,Thu", "10:00-13:00"),
            ("dr_002", "Dr. Meena Iyer", "Dermatology", "Wed,Fri", "11:00-14:00"),
            ("dr_003", "Dr. Arvind Raj", "Pediatrics", "Mon,Wed,Fri", "09:00-12:00"),
            ("dr_004", "Dr. Lakshmi B", "Cardiology", "Tue,Thu", "14:00-17:00"),
            ("dr_005", "Dr. Suresh P", "Orthopedics", "Mon,Fri", "10:00-12:30"),
            ("dr_006", "Dr. Anitha Das", "Gynecology", "Tue,Wed,Thu", "13:00-16:00"),
            ("dr_007", "Dr. Mohammed Z", "General Practice", "Mon,Thu", "15:00-17:00"),
            ("dr_008", "Dr. Rekha S", "Neurology", "Wed,Fri", "10:30-13:30"),
        ]
        for doc in doctors:
            self.add_doctor(*doc)
        print("✅ Dummy doctors seeded successfully.")
