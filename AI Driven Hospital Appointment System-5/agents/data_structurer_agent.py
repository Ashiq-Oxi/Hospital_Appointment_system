# agents/data_structurer_agent.py

class DataStructurerAgent:
    def __init__(self):
        self.data = {
            "name": None,
            "age": None,
            "gender": None,
            "symptoms": [],
            "symptom_details": {},  # Dynamic: stores answers per symptom
            "duration": None,
            "history": [],
            "contact": None
        }

    def set_basic_info(self, name=None, age=None, gender=None, duration=None, history=None, contact=None):
        """Sets the basic profile and health info."""
        if name:
            self.data["name"] = name.strip().title()
        if age:
            self.data["age"] = int(age)
        if gender:
            self.data["gender"] = gender.strip().lower()
        if duration:
            self.data["duration"] = duration.strip()
        if history:
            self.data["history"] = history if isinstance(history, list) else [history]
        if contact:
            self.data["contact"] = contact.strip()

    def update_field(self, key, value):
        """Update a single field if key exists."""
        if key in self.data:
            self.data[key] = value

    def add_symptom(self, symptom):
        """Add a new symptom to the symptom list and prepare detail container."""
        symptom = symptom.strip().lower()
        if symptom not in self.data["symptoms"]:
            self.data["symptoms"].append(symptom)
            self.data["symptom_details"][symptom] = {}

    def add_symptom_detail(self, symptom, question_key, answer):
        """Add a follow-up answer for a specific symptom."""
        symptom = symptom.strip().lower()
        if symptom not in self.data["symptom_details"]:
            self.data["symptom_details"][symptom] = {}
        self.data["symptom_details"][symptom][question_key.strip()] = answer.strip()

    def is_complete(self):
        """Check if essential fields are filled in for emergency assessment."""
        required_fields = ["name", "age", "gender", "symptoms"]
        return all(self.data.get(field) for field in required_fields)

    def get_missing_fields(self):
        """Return a list of missing required fields."""
        required_fields = ["name", "age", "gender", "symptoms"]
        return [field for field in required_fields if not self.data.get(field)]

    def get_structured_data(self):
        """Returns the current structured data."""
        return self.data
