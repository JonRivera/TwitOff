from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users that we pull and analyze Tweets for"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    # to do a one to many, we don't need ref from user to tweet, instead
    # we need an user id for every tweet
    # newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)
        # self b/c were inside the class
        # Now we will see the user's name


class Tweet(DB.Model):
    """Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    # we have a foreign key
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # tweet.user, we can get user directly
    # user will have a tweets field --- will not be stored in data based, but
    # loaded lazily
    # embedding = DB.Column(DB.PickleType, nullable=False)
    # That's the job of backref: when we interact --instance class the user class will have a tweet field and the
    # twee class will have a user field.
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    # helps us get user directly.

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_users():
    # Making Users
    austen = User(id=5, name='austen')
    elon = User(id=2, name='Elonmusk')
    Jon = User(id=3, name='Jonny')

    # Making Tweets
    t1 = Tweet(id=1, text='lambda Rocks', user_id=5)
    t2 = Tweet(id=2, text='Flask is awesome', user_id=3)
    t3 = Tweet(id=3, text='I am learning flask', user_id=5)
    t4 = Tweet(id=4, text='I will master as much flask as possible', user_id=4)
    t5 = Tweet(id=5, text='Tesla will give away 100 free teslas', user_id=2)
    t6 = Tweet(id=6, text='Lambda school is transforming peoples lives', user_id=4)

    # Append Tweets, not necessary as u can just do DB.session(tweet) to add append tweets to users
    austen.tweets.append(t1)
    Jon.tweets.append(t2)
    elon.tweets.append(t3)

    # Adding users and corresponding tweets to session
    DB.session.add(austen)
    DB.session.add(elon)
    DB.session.add(Jon)
    DB.session.add(t4)
    DB.session.add(t5)
    DB.session.add(t6)
    DB.session.commit()
