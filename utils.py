def get_non_empty_input(prompt):
    while True:
        value = input(prompt)
        if value.strip() != "":
            return value.strip()
        print("This field can't be empty. Please try again.")
        