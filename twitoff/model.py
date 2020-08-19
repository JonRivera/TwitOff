from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users that we pull and analyze Tweets for"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    # to do a one to many, we don't need ref from user to tweet, instead
    # we need a user id for every tweet
    # Tweet IDs are ordinal ints, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)
        # self b/c were inside the class
        # Now we will see the user's name


class Tweet(DB.Model):
    """Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    embedding = DB.Column(DB.PickleType, nullable=False)
    # we have a foreign key
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # tweet.user, we can get user directly
    # user will have a tweets field --- will not be stored in data based, but
    # loaded lazily
    # That's the job of backref: when we interact --instance class the user class will have a tweet field and the
    # tweet class will have a user field.
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    # helps us get user directly.

    def __repr__(self):
        return '-Twe et {}-'.format(self.text)


