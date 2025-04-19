# agents/patient_listener_agent.py

class PatientListenerAgent:
    def __init__(self):
        self.last_message = None

    def listen(self, user_input: str):
        """Receives and stores the user's latest message."""
        self.last_message = user_input
        return {
            "status": "received",
            "message": user_input
        }
