class EntityExtractor:
    def extract(self, doc):
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
