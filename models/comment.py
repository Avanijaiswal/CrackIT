class Comment:
    def __init__(self, id, experience_id, user_id, comment_text, created_at=None):
        self.id = id
        self.experience_id = experience_id
        self.user_id = user_id
        self.comment_text = comment_text
        self.created_at = created_at

    def __repr__(self):
        return f"Comment(id={self.id}, text='{self.comment_text}')"