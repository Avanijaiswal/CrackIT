from services.auth_service import register_user, login_user
from services.experience_service import create_experience, get_experiences_by_company
from services.round_service import add_round
from services.question_service import add_question
from services.report_service import get_topic_frequency, get_round_type_breakdown, get_crack_rate
from services.social_service import toggle_like, add_comment
from utils import get_non_empty_input


current_user = None

def show_main_menu():
    print("\n====== CrackIT ======")
    print("1. Register")
    print("2. Login")
    print("3. Post an Interview Experience")
    print("4. View Experiences by Company")
    print("5. Company Intelligence Report")
    print("6. Exit")

def handle_register():
    print("\n--- Register a New Account ---")
    name = get_non_empty_input("Enter your name: ")
    email = get_non_empty_input("Enter your email: ")
    password = get_non_empty_input("Enter a password: ")
    success = register_user(name, email, password)
    if success:
        print("You can now log in with your new account.")

def handle_login():
    global current_user
    print("\n--- Login ---")
    email = get_non_empty_input("Enter your email : ")
    password = get_non_empty_input("Enter your password : ")
    user = login_user(email, password)
    if user is not None:
        current_user = user

def handle_post_experience():
    global current_user

    if current_user is None:
        print("You must be logged in to post an experience")
        return

    print("\n---Post an Interview Exprerience ---")
    company_name = get_non_empty_input("Company name : ")
    role = get_non_empty_input("Role applied for : ")
    valid_outcomes = ["Selected", "Rejected", "Pending"]
    while True:
        outcome = get_non_empty_input("Outcome (Selected/Rejected/Pending): ")
        if outcome.capitalize() in valid_outcomes:
            outcome = outcome.capitalize()
            break
        print("Please enter exactly one of: Selected, Rejected, Pending.")

    anonymous_input = get_non_empty_input("Post this anonymously? (yes/no): ")
    is_anonymous = anonymous_input.strip().lower() == "yes"

    experience_id = create_experience(
        user_id=current_user.id,
        company_name=company_name,
        role=role,
        outcome=outcome,
        is_anonymous=is_anonymous
    )

    if experience_id is None:
        print("Something went wrong creating the experience. Stopping.")
        return

    while True:
        rounds_input = get_non_empty_input("How many interview rounds did you have? : ")
        try:
            num_rounds = int(rounds_input)
            if num_rounds <= 0:
                print("Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    for i in range(1, num_rounds + 1):
        print(f"\n-- Round {i} --")
        round_type = input(f"Round {i} type (Technichal/HR/Management/GD/Aptitude) : ")
        round_id = add_round(
            experience_id=experience_id,
            round_number=i,
            round_type=round_type
        )

        if round_id is None:
            print(f"Skipping questions for round {i} — round couldn't be saved.")
            continue

        print(f"Enter questions for round {i}, one at a time. Type 'done' when finished.")
        while True:
            question_text = input("Question (or 'done'): ")
            if question_text.strip().lower() == "done":
                break
            add_question(round_id=round_id, question_text=question_text)

    print("\nExperience fully posted! Thank you for contributing.")

def handle_view_experiences():
    print("\n--- View Experiences by Company ---")
    company_name = get_non_empty_input("Enter a company name to search : ")

    experiences = get_experiences_by_company(company_name,)

    if not experiences:
        print(f"No experiences found for '{company_name}' yet.")
        return

    for e in experiences:
        display_name = "Anonymous" if e["is_anonymous"] else e["user_name"]
        print(f"\n=== [ID: {e['experience_id']}] {e['role']} | Outcome: {e['outcome']} | By: {display_name} | 👍 {e['like_count']} likes ===")
        for r in e["rounds"]:
            print(f" Round {r['round_number']} ({r['round_type']}):")
            for q in r['questions']:
                print(f"   -{q['question_text']}   [Topic : {q['topic']}]")
        if e["comments"]:
            print("  Comments:")
            for c in e["comments"]:
                print(f"    {c['user_name']}: {c['comment_text']}")

    global current_user
    if current_user is None:
        return

    print("\n--- Interact with an Experience ---")
    action = input("Type an experience ID to like/comment on it, or press Enter to skip: ")

    if action.strip() == "":
        return

    try:
        experience_id = int(action)
    except ValueError:
        print("Invalid ID.")
        return

    print("1. Like/Unlike this experience")
    print("2. Add a comment")
    sub_choice = input("Choose an option: ")

    match sub_choice:
        case "1":
            toggle_like(user_id=current_user.id, experience_id=experience_id)
        case "2":
            comment_text = input("Your comment: ")
            add_comment(experience_id=experience_id, user_id=current_user.id, comment_text=comment_text)
        case _:
            print("Invalid option.")

def handle_company_report():
    print("\n--- Company Intelligence Report ---")
    company_name = get_non_empty_input("Enter a company name : ")

    topic_data = get_topic_frequency(company_name)
    round_data = get_round_type_breakdown(company_name)
    crack_data = get_crack_rate(company_name)

    if not topic_data and not round_data:
        print(f"No data found '{company_name}' yet. Be the first to post an experience.")
        return

    print(f"\n===== Report: {company_name} =====")

    if crack_data:
        print(f"\nCrack Rate: {crack_data['crack_rate']}% "
              f"({crack_data['selected_count']} of {crack_data['total_count']} reported as Selected)")

    print("\n== Round Type Breakdown ==")
    if round_data:
        for row in round_data:
            print(f" {row['round_type']}: {row['type_count']} rounds ({row['percentage']}%)")
    else:
        print(" No round data available yet.")

    print("\nTopics Asked (Most to Least Frequent):")
    if topic_data:
        for row in topic_data:
            print(f"  {row['topic']}: {row['topic_count']} question(s)")
    else:
        print("  No question data available yet.")

    
def main():
    while True:
        show_main_menu()
        choice = input("Choose an option : ")

        match choice:
            case "1":
                handle_register()
            case "2":
                handle_login()
            case "3":
                handle_post_experience()
            case "4":
                handle_view_experiences()
            case "5":
                handle_company_report()
            case "6":
                print("Goodbye!")
                break

            case _:
                print("Invalid Choice.")

if __name__ == "__main__":
    main()