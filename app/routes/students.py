from flask import Blueprint, request, jsonify, render_template, redirect, url_for, abort
from app.database import get_db_connection
from datetime import datetime

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.route("/", methods=["GET"])
def get_all_students():
    db = get_db_connection()
    students = db.execute("SELECT * FROM students;").fetchall()
    return render_template("student/list.html", students=students)


@students_bp.route("/api", methods=["GET"])
def get_all_students_json():
    db = get_db_connection()
    students = db.execute("SELECT * FROM students;").fetchall()
    return jsonify([dict(s) for s in students]), 200


@students_bp.route("/<int:student_id>", methods=["GET"])
def get_single_student(student_id):
    db = get_db_connection()
    student = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        abort(404)
    return render_template("student/single.html", student=student)


@students_bp.route("/create", methods=["GET", "POST"])
def create_student():
    if request.method == "GET":
        return render_template("student/create.html")
    if request.method == "POST":
        data = request.form
        db = get_db_connection()
        db.execute(
            "INSERT INTO students (dni, name, age, grade, is_approved) VALUES (?, ?, ?, ?, ?)",
            (data["dni"], data["name"], data["age"], data["grade"], 1 if data.get("is_approved") else 0)
        )
        db.commit()
        return redirect(url_for("students.get_all_students"))


@students_bp.route("/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    db = get_db_connection()
    student = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        abort(404)
    if request.method == "GET":
        return render_template("student/update.html", student=student)
    if request.method == "POST":
        data = request.form
        now = datetime.utcnow().isoformat()
        db.execute(
            "UPDATE students SET dni=?, name=?, age=?, grade=?, is_approved=?, updated_at=? WHERE id=?",
            (data["dni"], data["name"], data["age"], data["grade"], 1 if data.get("is_approved") else 0, now, student_id)
        )
        db.commit()
        return redirect(url_for("students.get_all_students"))


@students_bp.route("/delete/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    db = get_db_connection()
    student = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        abort(404)
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    return "", 200


@students_bp.route("/bulk", methods=["POST"])
def bulk_create_students():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Se esperaba una lista"}), 400
    db = get_db_connection()
    for student in data:
        db.execute(
            "INSERT INTO students (dni, name, age, grade, is_approved) VALUES (?, ?, ?, ?, ?)",
            (student["dni"], student["name"], student.get("age"), student.get("grade"), student.get("is_approved", 0))
        )
    db.commit()
    return jsonify({"message": f"{len(data)} estudiantes creados"}), 201


@students_bp.route("/average", methods=["GET"])
def average_grade():
    db = get_db_connection()
    result = db.execute("SELECT AVG(grade) as average FROM students;").fetchone()
    return jsonify({"average": result["average"]}), 200


@students_bp.route("/table", methods=["GET"])
def students_table():
    db = get_db_connection()
    students = db.execute("SELECT * FROM students;").fetchall()
    return render_template("partials/students_table.html", students=students)