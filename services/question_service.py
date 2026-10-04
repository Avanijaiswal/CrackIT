from dao.question_dao import QuestionDAO
from services.tagging_service import detect_topic


def add_question(round_id, question_text):
    topic = detect_topic(question_text)
    question_dao = QuestionDAO()
    question_id = question_dao.insert(round_id, question_text, topic)

    if question_id is None:
        print("Could not add question.")
        return None

    print(f"Question added (topic: {topic}).")
    return question_id


if __name__ == "__main__":
    add_question(round_id=1, question_text="Write a query to find the second highest salary")