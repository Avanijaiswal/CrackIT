from database.connection import Database

def create_tables():
    db = Database()
    connection = db.connect()

    if connection is None:
        print("No database connection.")
        return
    cursor = connection.cursor()

    cursor.execute("create table if not exists users (id int primary key auto_increment, name varchar(100) not null, email varchar(150) unique not null, password_hash varchar(255) not null, contributor_score int default 0)ENGINE=InnoDB")

    cursor.execute("create table if not exists companies (id int primary key auto_increment, name varchar(150) unique not null) ENGINE = InnoDB")

    cursor.execute("create table if not exists experiences (id int primary key auto_increment, user_id int, company_id int, role varchar(100), outcome varchar(20), is_anonymous tinyint default 0, created_at datetime default current_timestamp, foreign key (user_id) references users(id), foreign key (company_id) references companies(id)) ENGINE=InnoDB")

    cursor.execute("create table if not exists rounds(id int primary key auto_increment, experience_id int, round_number int, round_type varchar(50), foreign key(experience_id) references experiences(id)) ENGINE=InnoDB")

    cursor.execute("create table if not exists questions(id int primary key auto_increment, round_id int, question_text text, topic varchar(50), foreign key(round_id) references rounds(id)) ENGINE=InnoDB")

    cursor.execute("create table if not exists comments (id int primary key auto_increment, experience_id int, user_id int, comment_text text, created_at datetime default current_timestamp, foreign key(experience_id) references experiences(id), foreign key(user_id) references users(id))ENGINE=InnoDB")

    cursor.execute("create table if not exists likes(id int primary key auto_increment, user_id int, experience_id int, foreign key(user_id) references users(id), foreign key(experience_id)references experiences(id)) ENGINE=InnoDB")

    connection.commit()
    cursor.close()
    connection.close()
    print("All tables created successfully.")

if __name__ == "__main__":
    create_tables()