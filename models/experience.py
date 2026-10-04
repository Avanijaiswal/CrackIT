class Experience:
    def __init__(self, id, user_id, company_id, role, outcome,is_anonymous=False, created_at=None):
        self.id = id
        self.user_id = user_id
        self.company_id = company_id
        self.role = role
        self.outcome = outcome
        self.is_anonymous = is_anonymous
        self.created_at = created_at

    def __repr__(self):
        return f"Experience(id={self.id}, role='{self.role}', outcome='{self.outcome}')"