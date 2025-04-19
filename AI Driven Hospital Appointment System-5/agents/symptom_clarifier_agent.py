# agents/symptom_clarifier_agent.py

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class SymptomClarifierAgent:
    def __init__(self, model_name="mistral"):
        self.llm = Ollama(model=model_name)

        self.prompt = PromptTemplate.from_template("""
        You are a medical assistant chatbot.
        The patient reported a symptom: "{symptom_input}".

        Your task is to generate 3 to 5 **important** follow-up medical questions 
        to understand the symptom better.

        ⚠️ Rules:
        - Ask ONE question per line, no explanation.
        - Focus on critical risk or triage questions first.
        - Avoid any diagnosis.
        - Do NOT add anything outside the question list.
        - Output only numbered questions like:
            1. ...
            2. ...
            3. ...

        Symptom: {symptom_input}
        """)

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_followup_questions(self, symptom_input: str):
        response = self.chain.run(symptom_input=symptom_input)

        # Extract and clean up each question
        questions = []
        for line in response.strip().split("\n"):
            if "." in line:
                _, question = line.split(".", 1)
                cleaned = question.strip()
                if cleaned:
                    questions.append(cleaned)

        return questions
