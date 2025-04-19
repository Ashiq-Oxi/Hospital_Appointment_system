import streamlit as st

# Import agents
from agents.patient_listener_agent import PatientListenerAgent
from agents.intent_analyzer_agent import IntentAnalyzerAgent
from agents.symptom_clarifier_agent import SymptomClarifierAgent
from agents.data_structurer_agent import DataStructurerAgent
from agents.emergency_assessment_agent import EmergencyAssessmentAgent
from agents.appointment_booking_agent import AppointmentBookingAgent
from agents.orchestrator_agent import OrchestratorAgent

# Page Setup
st.set_page_config(page_title="🤖 AI Healthcare Assistant", layout="centered")
st.title("🤖 AI Healthcare Assistant")
st.caption("Your personal health companion: Talk to me about symptoms, bookings, or health concerns.")

# Initialize session state
if "orchestrator_agent" not in st.session_state:
    st.session_state.listener_agent = PatientListenerAgent()
    st.session_state.intent_agent = IntentAnalyzerAgent()
    st.session_state.clarifier_agent = SymptomClarifierAgent()
    st.session_state.structurer_agent = DataStructurerAgent()
    st.session_state.emergency_agent = EmergencyAssessmentAgent()
    st.session_state.appointment_agent = AppointmentBookingAgent()

    st.session_state.orchestrator_agent = OrchestratorAgent(
        intent_agent=st.session_state.intent_agent,
        clarifier_agent=st.session_state.clarifier_agent,
        structurer_agent=st.session_state.structurer_agent,
        emergency_agent=st.session_state.emergency_agent,
        appointment_agent=st.session_state.appointment_agent
    )
    st.session_state.chat_history = []

# Optional: Reset chat
if st.button("🔄 Reset Conversation"):
    st.session_state.chat_history = []
    st.session_state.orchestrator_agent.symptom = None
    st.session_state.orchestrator_agent.questions = []
    st.session_state.orchestrator_agent.answers = []
    st.session_state.orchestrator_agent.question_index = 0
    st.session_state.orchestrator_agent.awaiting_appointment_confirmation = False
    st.session_state.chat_history.append(("assistant", "🔄 Conversation has been reset. How can I assist you now?"))

# Welcome message
if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown("👋 Hello! How can I assist with your health today?")

# Chat input
user_input = st.chat_input("Describe your symptoms or ask a question...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.listener_agent.listen(user_input)

    # Handle user input through Orchestrator
    response = st.session_state.orchestrator_agent.handle_input(user_input)

    # ✅ Handle main message
    main_message = response.get("message", "🤖 I'm processing your input...")
    if main_message:
        st.session_state.chat_history.append(("assistant", main_message))

    # 🧾 Display structured medical record
    if response.get("structured_data"):
        st.session_state.chat_history.append(("assistant", "**🗂️ Your Medical Record:**"))
        st.session_state.chat_history.append(("assistant", f"```json\n{response['structured_data']}\n```"))

    # 🚨 Display emergency response
    if response.get("emergency_result") and response["emergency_result"].get("is_emergency"):
        st.session_state.chat_history.append(("assistant", f"🚨 {response['emergency_result']['explanation']}"))

    # 📅 Show available doctors if appointment is triggered
    if response.get("appointment_result"):
        result = response["appointment_result"]
        doctors = result.get("doctors", [])
        if doctors:
            st.session_state.chat_history.append(("assistant", "**📅 Available Doctors:**"))
            for doc in doctors:
                st.session_state.chat_history.append((
                    "assistant",
                    f"- **Dr. {doc['name']}** ({doc['specialization']}) — {doc['available_day']} at {doc['available_time']}"
                ))
        elif not result.get("success", True):
            st.session_state.chat_history.append(("assistant", result.get("message", "❌ No doctors found.")))

# 🔁 Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)
