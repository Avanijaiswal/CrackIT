import os
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, abort

load_dotenv()

from services.auth_service import register_user, login_user
from services.experience_service import create_experience, get_experiences_by_company
from services.round_service import add_round
from services.question_service import add_question
from services.report_service import get_topic_frequency, get_round_type_breakdown, get_crack_rate
from services.social_service import toggle_like, add_comment
from services.user_service import get_leaderboard
from dao.user_dao import UserDAO
from dao.admin_dao import AdminDAO

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if not UserDAO().is_admin(session["user_id"]):
            abort(403)
        return view(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/experiences")
def experiences():
    company = request.args.get("company")
    results = get_experiences_by_company(company)
    return render_template("experiences.html", company=company, experiences=results)


@app.route("/report")
def report():
    company = request.args.get("company")
    topic_data = get_topic_frequency(company) or []
    round_data = get_round_type_breakdown(company) or []
    crack_data = get_crack_rate(company)

    max_count = max([int(r["topic_count"]) for r in topic_data], default=1) or 1
    topics = []
    for r in topic_data:
        count = int(r["topic_count"])
        topics.append({
            "topic": r["topic"],
            "count": count,
            "width": round(count / max_count * 100)
        })

    rounds = []
    for r in round_data:
        rounds.append({
            "round_type": r["round_type"],
            "count": int(r["type_count"]),
            "percentage": round(float(r["percentage"]), 1)
        })

    crack = None
    if crack_data:
        crack = {
            "rate": round(float(crack_data["crack_rate"]), 1),
            "selected": int(crack_data["selected_count"]),
            "total": int(crack_data["total_count"])
        }

    return render_template(
        "report.html",
        company=company,
        topics=topics,
        rounds=rounds,
        crack=crack
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        success = register_user(name, email, password)
        if success:
            return redirect("/login")
        return render_template("register.html", error="Registration failed. That email may already be in use.")
    return render_template("register.html", error=None)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = login_user(email, password)
        if user is not None:
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["is_admin"] = UserDAO().is_admin(user.id)
            return redirect("/")
        return render_template("login.html", error="Wrong email or password.")
    return render_template("login.html", error=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/post", methods=["GET", "POST"])
def post_experience():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        company_name = request.form.get("company_name")
        role = request.form.get("role")
        outcome = request.form.get("outcome")
        is_anonymous = request.form.get("anonymous") == "on"

        experience_id = create_experience(
            user_id=session["user_id"],
            company_name=company_name,
            role=role,
            outcome=outcome,
            is_anonymous=is_anonymous
        )

        if experience_id is None:
            return "Something went wrong creating the experience."
        return redirect(url_for("add_rounds", experience_id=experience_id, round_number=1, company=company_name))

    return render_template("post.html")


@app.route("/post/<int:experience_id>/rounds/<int:round_number>", methods=["GET", "POST"])
def add_rounds(experience_id, round_number):
    if "user_id" not in session:
        return redirect("/login")

    company = request.args.get("company")

    if request.method == "POST":
        round_type = request.form.get("round_type")
        questions_text = request.form.get("questions") or ""
        action = request.form.get("action")

        round_id = add_round(
            experience_id=experience_id,
            round_number=round_number,
            round_type=round_type
        )
        if round_id is None:
            return "Could not save this round."

        
import re

lines = [
    line.strip().lstrip("•*-– ").strip()
    for line in questions_text.splitlines()
    if line.strip()
]

groups = []

# Check whether the input uses question numbers like Q1, Q2, Q3.
has_question_numbers = any(
    re.match(r"^Q(?:uestion)?\s*\d+\s*[.):\-]", line, re.IGNORECASE)
    for line in lines
)

current_question = []

for line in lines:
    is_new_question = bool(
        re.match(
            r"^Q(?:uestion)?\s*\d+\s*[.):\-]",
            line,
            re.IGNORECASE
        )
    )

    is_option = bool(
        re.match(r"^[A-Da-d]\s*[).:-]", line)
    )

    if has_question_numbers:
        if is_new_question:
            if current_question:
                groups.append("\n".join(current_question))
            current_question = [line]
        elif current_question:
            current_question.append(line)
        else:
            current_question = [line]

    else:
        if is_option and current_question:
            current_question.append(line)
        else:
            if current_question:
                groups.append("\n".join(current_question))
            current_question = [line]

if current_question:
    groups.append("\n".join(current_question))

for question in groups:
    add_question(
        round_id=round_id,
        question_text=question
    )

        if action == "another":
            return redirect(url_for("add_rounds", experience_id=experience_id,
                                    round_number=round_number + 1, company=company))
        return redirect(url_for("experiences", company=company))

    return render_template("add_round.html", round_number=round_number)


@app.route("/like/<int:experience_id>", methods=["POST"])
def like(experience_id):
    if "user_id" not in session:
        return redirect("/login")

    company = request.form.get("company")
    toggle_like(user_id=session["user_id"], experience_id=experience_id)
    return redirect(url_for("experiences", company=company))


@app.route("/comment/<int:experience_id>", methods=["POST"])
def comment(experience_id):
    if "user_id" not in session:
        return redirect("/login")

    company = request.form.get("company")
    comment_text = request.form.get("comment_text", "").strip()

    if comment_text:
        add_comment(
            experience_id=experience_id,
            user_id=session["user_id"],
            comment_text=comment_text
        )
    return redirect(url_for("experiences", company=company))


@app.route("/leaderboard")
def leaderboard():
    top_users = get_leaderboard()
    return render_template("leaderboard.html", top_users=top_users)


# ---------------- Admin ----------------

ADMIN_SECTIONS = ["experiences", "questions", "comments", "likes", "users", "companies"]

KIND_TO_SECTION = {
    "experience": "experiences",
    "question": "questions",
    "comment": "comments",
    "like": "likes",
    "user": "users",
    "company": "companies",
}


@app.route("/admin")
@admin_required
def admin():
    return render_template("admin.html", section="overview", counts=AdminDAO().get_counts(), rows=[])


@app.route("/admin/<section>")
@admin_required
def admin_section(section):
    if section not in ADMIN_SECTIONS:
        abort(404)
    rows = AdminDAO().list_section(section)
    return render_template("admin.html", section=section, rows=rows, counts={})


@app.route("/admin/delete/<kind>/<int:item_id>", methods=["POST"])
@admin_required
def admin_delete(kind, item_id):
    if kind not in KIND_TO_SECTION:
        abort(404)
    if kind == "user" and item_id == session["user_id"]:
        return redirect("/admin/users")
    AdminDAO().delete_item(kind, item_id)
    return redirect("/admin/" + KIND_TO_SECTION[kind])


@app.route("/admin/user/<int:user_id>/role", methods=["POST"])
@admin_required
def admin_set_role(user_id):
    if user_id != session["user_id"]:
        AdminDAO().set_admin(user_id, request.form.get("make_admin") == "1")
    return redirect("/admin/users")


@app.route("/admin/recalculate", methods=["POST"])
@admin_required
def admin_recalculate():
    AdminDAO().recalculate_points()
    return redirect("/admin")


if __name__ == "__main__":
    from livereload import Server
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch("static/")
    server.watch("templates/")
    server.serve(port=5000)
