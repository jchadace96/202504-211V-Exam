import sqlite3

connection = sqlite3.connect("students.db")

with open("schema.sql", "w") as f:
    f.write("""
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    age INTEGER,
    grade REAL,
    is_approved INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")

with open("schema.sql", "r") as f:
    connection.executescript(f.read())

def insert_student(dni, name, age, grade, is_approved):
    connection = sqlite3.connect("students.db")
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO students (dni, name, age, grade, is_approved) VALUES (?, ?, ?, ?, ?)",
        (dni, name, age, grade, is_approved)
    )
    connection.commit()
    connection.close()

insert_student("12345678", "Juan Perez", 20, 15.5, 1)
insert_student("87654321", "Maria Garcia", 22, 12.0, 0)
insert_student("11223344", "Carlos Lopez", 19, 18.0, 1)