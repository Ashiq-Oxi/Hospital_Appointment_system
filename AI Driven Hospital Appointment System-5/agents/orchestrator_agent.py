from agents.intent_analyzer_agent import IntentAnalyzerAgent
from agents.symptom_clarifier_agent import SymptomClarifierAgent
from agents.data_structurer_agent import DataStructurerAgent
from agents.emergency_assessment_agent import EmergencyAssessmentAgent
from agents.appointment_booking_agent import AppointmentBookingAgent

class OrchestratorAgent:
    def __init__(self, intent_agent, clarifier_agent, structurer_agent, emergency_agent, appointment_agent):
        self.intent_agent = intent_agent
        self.symptom_agent = clarifier_agent
        self.data_agent = structurer_agent
        self.emergency_agent = emergency_agent
        self.appointment_agent = appointment_agent

        self.symptom = None
        self.questions = []
        self.answers = []
        self.question_index = 0
        self.awaiting_appointment_confirmation = False

    def handle_input(self, user_input):
        response_payload = {
            "intent": None,
            "message": None,
            "follow_up_questions": [],
            "emergency_result": None,
            "structured_data": None,
            "appointment_result": None
        }

        # ✅ If waiting for appointment confirmation
        if self.awaiting_appointment_confirmation:
            if user_input.strip().lower() in ["yes", "y", "sure", "ok", "okay"]:
                result = self.appointment_agent.suggest_doctors("I want to book an appointment")
                response_payload["intent"] = "book_appointment"
                response_payload["appointment_result"] = result
                response_payload["message"] = result.get("message", "✅ Appointment options prepared.")
            else:
                response_payload["message"] = "👍 No problem. Let me know if you need help later."
            self.awaiting_appointment_confirmation = False
            return response_payload

        # 🔁 If answering follow-up symptom questions
        if self.symptom and self.question_index < len(self.questions):
            question_key = self.questions[self.question_index]
            self.data_agent.add_symptom_detail(self.symptom, question_key, user_input)
            self.answers.append(user_input)
            self.question_index += 1

            if self.question_index < len(self.questions):
                next_q = self.questions[self.question_index]
                response_payload["intent"] = "report_symptoms"
                response_payload["message"] = f"🔍 {next_q}"
            else:
                structured_data = self.data_agent.get_structured_data()
                emergency_result = self.emergency_agent.assess_emergency(structured_data)

                response_payload["intent"] = "report_symptoms"
                response_payload["structured_data"] = structured_data
                response_payload["emergency_result"] = emergency_result

                if emergency_result["is_emergency"]:
                    response_payload["message"] = f"🚨 Emergency Alert: {emergency_result['explanation']}"
                else:
                    response_payload["message"] = emergency_result["explanation"]
                    if emergency_result.get("next_step") == "ask_appointment_booking":
                        self.awaiting_appointment_confirmation = True

                # Reset symptom session
                self.symptom = None
                self.questions = []
                self.answers = []
                self.question_index = 0

            return response_payload

        # 🧠 First-time input - detect intent
        intent = self.intent_agent.analyze_intent(user_input)
        response_payload["intent"] = intent

        if intent == "report_symptoms":
            self.symptom = self.extract_symptom_keyword(user_input)
            if not self.symptom:
                response_payload["message"] = "⚠️ I couldn't detect a symptom from your input. Please try again."
                return response_payload

            self.questions = self.symptom_agent.generate_followup_questions(user_input)
            self.answers = []
            self.question_index = 0
            self.data_agent.add_symptom(self.symptom)

            if self.questions:
                response_payload["message"] = f"🔍 {self.questions[0]}"
                response_payload["follow_up_questions"] = self.questions
            else:
                response_payload["message"] = "⚠️ I couldn't generate follow-up questions for that symptom."

        elif intent == "book_appointment":
            result = self.appointment_agent.suggest_doctors(user_input)
            if not result or "message" not in result:
                response_payload["message"] = "❌ Sorry, no available doctors found."
            else:
                response_payload["appointment_result"] = result
                response_payload["message"] = result.get("message", "✅ Doctor suggestions provided.")

        elif intent == "specific_doctor":
            response_payload["message"] = "👨‍⚕️ Specific doctor matcher not implemented yet. Stay tuned!"

        else:
            response_payload["message"] = "🤖 Sorry, I couldn't understand your request."

        return response_payload

    def extract_symptom_keyword(self, input_text):
        # Modify to capture the entire symptom or a more intelligent keyword
        symptom = input_text.strip().split()[0]  # Example, extracting only the first word
        return symptom if symptom else None
