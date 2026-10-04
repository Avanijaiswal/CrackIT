class Question:
    def __init__(self, id, round_id, question_text, topic):
        self.id = id
        self.round_id = round_id
        self.question_text = question_text
        self.topic = topic

    def __repr__(self):
        return f"Question(id={self.id}, topic='{self.topic}')"