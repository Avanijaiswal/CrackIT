import bcrypt
from mysql.connector import IntegrityError
from dao.user_dao import UserDAO


def hash_password(plain_password):

    password_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def register_user(name, email, plain_password):
    
    hashed_pw = hash_password(plain_password)
    user_dao = UserDAO()

    try:
        user_id = user_dao.insert(name, email, hashed_pw)
        if user_id is None:
            print("Could not register user — no database connection.")
            return False
        print(f"User '{name}' registered successfully!")
        return True
    except IntegrityError:
        print("That email is already registered. Try logging in instead.")
        return False
    except Exception as e:
        print(f"Registration failed: {e}")
        return False


def login_user(email, plain_password):
    
    user_dao = UserDAO()
    user = user_dao.find_by_email(email)

    if user is None:
        print("No account found with that email.")
        return None

    stored_hash = user.password_hash.encode("utf-8")
    entered_password = plain_password.encode("utf-8")

    if bcrypt.checkpw(entered_password, stored_hash):
        print(f"Welcome back, {user.name}!")
        return user
    else:
        print("Incorrect password.")
        return None
        

