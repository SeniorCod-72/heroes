from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///heroes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
db.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
