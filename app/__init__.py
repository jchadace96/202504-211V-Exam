from flask import Flask, render_template
from app.routes.students import students_bp
from app.database import close_db_connection


def create_app():
    app = Flask(__name__)

    app.teardown_appcontext(close_db_connection)

    # Registrar Blueprints
    app.register_blueprint(students_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app