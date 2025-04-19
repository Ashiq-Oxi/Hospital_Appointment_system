import ollama
from agents.doctor_database_manager import DoctorDatabaseManager

class AppointmentBookingAgent:
    def __init__(self):
        self.db_manager = DoctorDatabaseManager()

    def infer_specialization(self, patient_input):
        prompt = f"""
        Based on the patient's statement, suggest the most relevant medical specialization.
        Only return one specialization word like 'Cardiology', 'Dermatology', 'Pediatrics', etc.

        Patient statement: "{patient_input}"
        Specialization:
        """
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        print("📨 Raw Ollama Response:", response)  # DEBUG
        inferred = response["message"]["content"].strip().split("\n")[0].split('.')[0]
        print("🧠 Inferred Specialization:", inferred)  # DEBUG
        return inferred

    def suggest_doctors(self, user_input):
        specialization = self.infer_specialization(user_input)

        print("🔍 Searching for doctors with specialization:", specialization)  # DEBUG
        print("📋 All doctors in database:")
        for doc in self.db_manager.get_all_doctors():
            print(f"  - {doc['name']} | {doc['specialization']}")

        doctors = self.db_manager.get_doctors_by_specialization(specialization)

        if not doctors:
            return {
                "success": False,
                "specialization": specialization,
                "message": f"❌ Sorry, no available doctors found for {specialization} right now.",
                "doctors": []
            }

        message_lines = [f"👨‍⚕️ Here are available doctors for **{specialization}**:"]
        for doc in doctors:
            line = f"- **{doc['name']}** ({doc['specialization']}) — Available on {doc['available_day']} at {doc['available_time']}"

            message_lines.append(line)

        message_lines.append("\n🗓️ Please tell me which doctor you'd like to book an appointment with.")

        return {
            "success": True,
            "specialization": specialization,
            "message": "\n".join(message_lines),
            "doctors": doctors
        }
