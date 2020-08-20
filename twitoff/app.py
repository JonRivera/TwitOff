from decouple import config
from flask import Flask, render_template, request
from .twitter import insert_example_users, add_or_update_user
from .model import DB, User
from .predict import predict_user


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    # Before whenever we created a user it just ran in memory
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # can't leave ENV like this based on documentation
    # app.config['ENV'] = config('ENV')
    DB.init_app(app)  # initialise application, this is the data base, this is how u connect to it

    # persist data in that sql file
    @app.route('/')
    def root():
        # render_template know which directory to look in to find the template
        return render_template('base.html', title='Home', users=User.query.all())
        # return 'Hello TwitOff!'

    @app.route('/compare', methods=['POST'])
    def compare():
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        # error handling
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction',
                               message=message)

    @app.route('/update')
    def update():
        # Reset the database
        insert_example_users()
        return render_template('base.html', title='Users updated!', users=User.query.all())

    # decorating twice, decor are functions that take functions return functions
    # to add users we need a post request
    # to get users were going to need a get request
    # The get request needs a parameter but the post doesn't, b/c when we add a user
    # were going to have a form
    # The name needs a default value,b/c might not exit, exist with get rec but not for post
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message = ''
        # semicolon lets u execute two statements in one line, set trace says enter pdb
        # python debugger
        # import pdb; pdb.set_trace()
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'USER {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database:')

    return app
