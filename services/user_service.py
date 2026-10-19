from dao.user_dao import UserDAO


def get_leaderboard(limit=20):
    return UserDAO().find_top_contributors(limit)