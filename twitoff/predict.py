import numpy as np
from sklearn.linear_model import LogisticRegression
from .model import User
from .twitter import BASILICA


def predict_user(user1_name, user2_name, tweet_text):
    """
    Determine and return which user is more likeley to say a given TWEEN
    ex__ run: predict('austen, "e;on", 'lambda school')
    Returns 1 (corresponding to first user passed in) or 0 (second)
    """
    # get first user, and second user objects
    # equivalent to query *
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(embeddings, labels)
    # we don data science and made a prediction
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1,-1))
