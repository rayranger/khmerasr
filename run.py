from src import app
from src import db
# import seeders
from waitress import serve

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
        # serve(app, port='5000', host='0.0.0.0', threads=2)
