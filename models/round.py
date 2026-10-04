class Round:
    def __init__(self, id, experience_id, round_number, round_type):
        self.id = id
        self.experience_id = experience_id
        self.round_number = round_number
        self.round_type = round_type

    def __repr__(self):
        return f"Round(id={self.id}, number={self.round_number}, type='{self.round_type}')"