from decouple import config
from flask import Flask, render_template
from .model import DB, User, insert_example_users


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    # Before whenever we created a user it just ran in memory
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    DB.init_app(app)  # initialise application, this is the data base, this is how u connect to it

    # persist data in that sql file
    @app.route('/')
    def root():
        # render_template know which directory to look in to find the template
        return render_template('base.html', title='Home', users=User.query.all())
        # return 'Hello TwitOff!'

    @app.route('/update')
    def update():
        # Reset the database
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        return render_template('base.html', title='Users updated!', users=User.query.all())

    return app
