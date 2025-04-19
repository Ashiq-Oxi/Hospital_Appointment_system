# test_booking.py
from agents.appointment_booking_agent import AppointmentBookingAgent

if __name__ == "__main__":
    agent = AppointmentBookingAgent()
    patient_input = "I want to meet a general practitioner"
    result = agent.suggest_doctors(patient_input)
    print("\n📋 Final Result:")
    print(result["message"])
