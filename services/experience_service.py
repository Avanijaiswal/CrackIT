
import re

from dao.experience_dao import ExperienceDAO
from dao.user_dao import UserDAO
from services.company_service import get_or_create_company
from dao.round_dao import RoundDAO
from dao.question_dao import QuestionDAO
from services.social_service import (
    get_comments_for_experience,
    get_like_count
)

POST_POINTS = 10

QUESTION_RE = re.compile(
    r"^Q(?:uestion)?\s*\d+\s*[.):\-]",
    re.IGNORECASE
)

OPTION_RE = re.compile(
    r"^[A-Da-d]\s*[).:\-]",
    re.IGNORECASE
)

STATEMENT_RE = re.compile(
    r"^(?:Statements?:|Options?:|Conclusions?:|\d+\s*[.)])",
    re.IGNORECASE
)


def group_questions(question_records):
    """
    Combine separately saved question and option records
    into one question for display.

    Does not modify the database.
    """

    records = sorted(question_records, key=lambda q: q.id)

    cleaned_records = []

    for record in records:
        text = (record.question_text or "").strip()

        if not text:
            continue

        # Remove bullets accidentally saved with the option.
        text = re.sub(r"^[•*–-]\s*", "", text)

        cleaned_records.append((record, text))

    has_numbered_questions = any(
        QUESTION_RE.match(text)
        for _, text in cleaned_records
    )

    grouped = []
    current_lines = []
    current_topic = "General"

    def save_current():
        nonlocal current_lines, current_topic

        if current_lines:
            grouped.append({
                "question_text": "\n".join(current_lines),
                "topic": current_topic
            })

        current_lines = []
        current_topic = "General"

    for record, text in cleaned_records:

        is_new_question = bool(QUESTION_RE.match(text))
        is_option = bool(OPTION_RE.match(text))
        is_statement = bool(STATEMENT_RE.match(text))

        if is_new_question:
            save_current()

            current_lines = [text]
            current_topic = record.topic or "General"
            continue

        if not current_lines:
            current_lines = [text]
            current_topic = record.topic or "General"
            continue

        if has_numbered_questions:
            # Everything after Q1 belongs to Q1 until Q2 appears.
            current_lines.append(text)

        elif is_option or is_statement:
            # Combine old MCQ options and statement lines.
            current_lines.append(text)

        else:
            save_current()

            current_lines = [text]
            current_topic = record.topic or "General"

    save_current()

    return grouped


def create_experience(
    user_id,
    company_name,
    role,
    outcome,
    is_anonymous=False
):
    company_id = get_or_create_company(company_name)

    if company_id is None:
        print("Could not create experience — company lookup failed.")
        return None

    experience_dao = ExperienceDAO()

    experience_id = experience_dao.insert(
        user_id,
        company_id,
        role,
        outcome,
        is_anonymous
    )

    if experience_id is None:
        print("Could not create experience.")
        return None

    UserDAO().add_points(user_id, POST_POINTS)

    print(
        f"Experience created (id: {experience_id}) "
        f"for company '{company_name}'."
    )

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

            question_records = question_dao.find_by_round_id(rnd.id)

            # IMPORTANT: Group old and new question records.
            questions = group_questions(question_records)

            rounds_with_questions.append({
                "round_number": rnd.round_number,
                "round_type": rnd.round_type,
                "questions": questions
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
        user_id=1,
        company_name="Amazon",
        role="SDE-1",
        outcome="Selected",
        is_anonymous=False
    )
