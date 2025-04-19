# agents/emergency_assessment_agent.py

from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class EmergencyAssessmentAgent:
    def __init__(self, model_name="mistral"):
        self.llm = Ollama(model=model_name)

        self.prompt = PromptTemplate(
            input_variables=["symptom_data"],
            template="""
You are an AI medical triage assistant.

You will receive structured symptom data from a patient. Based on your understanding of medical urgency, 
classify the situation as either:

- emergency (requires immediate medical attention)
- not_emergency (can proceed with routine consultation or appointment)

Consider:
- Severity and duration of pain or discomfort
- Life-threatening signs (e.g., unconsciousness, difficulty breathing, chest/jaw pain, seizures)
- Overall symptom context

Respond with only one word: emergency OR not_emergency.

Patient Symptom Data:
{symptom_data}
"""
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def assess_emergency(self, symptom_data: dict):
        try:
            formatted_data = "\n".join([f"{k}: {v}" for k, v in symptom_data.items()])
            response = self.chain.run(symptom_data=formatted_data)
            response_clean = response.strip().lower().replace('"', '').replace("'", '').replace("-", '').strip()

            if response_clean == "emergency":
                return {
                    "is_emergency": True,
                    "explanation": "🚨 Emergency detected. Please call 📞 +91-9876543210 or visit the nearest hospital immediately.",
                    "next_step": None
                }

            elif response_clean == "not_emergency":
                return {
                    "is_emergency": False,
                    "explanation": "✅ It does not appear to be an emergency. Would you like to book an appointment with a doctor?",
                    "next_step": "ask_appointment_booking"
                }

            else:
                return {
                    "is_emergency": False,
                    "explanation": f"⚠️ Unclear response from AI triage: '{response_clean}'. Defaulting to non-emergency. Please confirm with a human professional.",
                    "next_step": None
                }

        except Exception as e:
            return {
                "is_emergency": False,
                "explanation": f"❌ Error while analyzing emergency: {e}",
                "next_step": None
            }
