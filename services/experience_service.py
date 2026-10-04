from dao.experience_dao import ExperienceDAO
from services.company_service import get_or_create_company
from dao.round_dao import RoundDAO
from dao.question_dao import QuestionDAO
from services.social_service import get_comments_for_experience, get_like_count


def create_experience(user_id, company_name, role, outcome, is_anonymous=False):
    company_id = get_or_create_company(company_name)

    if company_id is None:
        print("Could not create experience — company lookup failed.")
        return None

    experience_dao = ExperienceDAO()
    experience_id = experience_dao.insert(user_id, company_id, role, outcome, is_anonymous)

    if experience_id is None:
        print("Could not create experience.")
        return None

    print(f"Experience created (id: {experience_id}) for company '{company_name}'.")
    return experience_id

def get_experiences_by_company(company_name):
    experience_dao = ExperienceDAO()
    round_dao = RoundDAO()
    question_dao = QuestionDAO()

    experiences = experience_dao.find_by_company_name(company_name)

    results = []
    for exp in experiences:
        rounds = round_dao.find_by_experience_id(exp.id)

        rounds_with_questions = []
        for rnd in rounds:
            questions = question_dao.find_by_round_id(rnd.id)
            rounds_with_questions.append({
                "round_number": rnd.round_number,
                "round_type": rnd.round_type,
                "questions": [{"question_text": q.question_text, "topic": q.topic} for q in questions]
            })

        comments = get_comments_for_experience(exp.id)
        like_count = get_like_count(exp.id)

        results.append({
            "experience_id": exp.id,
            "role": exp.role,
            "outcome": exp.outcome,
            "is_anonymous": exp.is_anonymous,
            "user_name": exp.user_name,
            "rounds": rounds_with_questions,
            "comments": comments,
            "like_count": like_count
        })

    return results

if __name__ == "__main__":
    create_experience(
        user_id = 1,
        company_name = "Amazon",
        role = "SDE-1",
        outcome = "Selected",
        is_anonymous = False
    )