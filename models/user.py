class User:
    def __init__(self, id, name, email, password_hash, contributor_score=0):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.contributor_score = contributor_score

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"