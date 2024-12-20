from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
import json

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_text = Column(String)
    system_response = Column(String)
    grammar_errors = Column(Text)  # JSON list
    pronunciation_errors = Column(Text)  # JSON list
    pattern_analysis = Column(Text)  # JSON dict

    def set_grammar_errors(self, errors):
        self.grammar_errors = json.dumps(errors)

    def get_grammar_errors(self):
        return json.loads(self.grammar_errors) if self.grammar_errors else []

    def set_pronunciation_errors(self, errors):
        self.pronunciation_errors = json.dumps(errors)

    def get_pronunciation_errors(self):
        return json.loads(self.pronunciation_errors) if self.pronunciation_errors else []

    def set_pattern_analysis(self, analysis):
        self.pattern_analysis = json.dumps(analysis)

    def get_pattern_analysis(self):
        return json.loads(self.pattern_analysis) if self.pattern_analysis else {}
