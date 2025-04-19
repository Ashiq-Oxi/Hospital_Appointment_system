# agents/intent_analyzer_agent.py

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class IntentAnalyzerAgent:
    def __init__(self, model_name="mistral"):
        self.llm = Ollama(model=model_name)
        self.prompt = PromptTemplate.from_template("""
        You are an intelligent healthcare assistant agent. Analyze the user's query and return the INTENT in lowercase.
        
        Possible intents:
        - book_appointment
        - report_symptoms
        - specific_doctor
        - cancel_appointment
        - follow_up

        User query: "{query}"
        Return only the intent.
        """)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def analyze_intent(self, query: str):
        result = self.chain.run(query=query).strip().lower()
        return result
