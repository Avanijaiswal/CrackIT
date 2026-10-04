from dao.round_dao import RoundDAO


def add_round(experience_id, round_number, round_type):
    round_dao = RoundDAO()
    round_id = round_dao.insert(experience_id, round_number, round_type)

    if round_id is None:
        print(f"Could not add round {round_number}.")
        return None

    print(f"Round {round_number} ({round_type}) added.")
    return round_id


if __name__ == "__main__":
    add_round(experience_id=1, round_number=1, round_type="Technical")