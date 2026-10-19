from dao.social_dao import SocialDAO
from dao.user_dao import UserDAO

LIKE_POINTS = 2


def add_comment(experience_id, user_id, comment_text):
    social_dao = SocialDAO()
    comment_id = social_dao.insert_comment(experience_id, user_id, comment_text)

    if comment_id is None:
        print("Could not add comment.")
        return None

    print("Comment added.")
    return comment_id


def get_comments_for_experience(experience_id):
    social_dao = SocialDAO()
    return social_dao.find_comments_by_experience_id(experience_id)


def toggle_like(user_id, experience_id):
    social_dao = SocialDAO()
    user_dao = UserDAO()
    existing_like_id = social_dao.find_like(user_id, experience_id)

    if existing_like_id is not None:
        social_dao.delete_like(existing_like_id)
        user_dao.add_points_to_experience_owner(experience_id, -LIKE_POINTS, user_id)
        print("👎 Like removed.")
    else:
        social_dao.insert_like(user_id, experience_id)
        user_dao.add_points_to_experience_owner(experience_id, LIKE_POINTS, user_id)
        print("👍 Experience liked!")


def get_like_count(experience_id):
    social_dao = SocialDAO()
    return social_dao.count_likes(experience_id)