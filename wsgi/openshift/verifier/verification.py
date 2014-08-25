from praw import Reddit


def verify(moderator_username, moderator_password,
           username, subreddit,
           flair_text=None, flair_css=None):
    print('Verifying {user} by {moderator} with password {pwd} for {subreddit} with flair {flair_text} and {flair_css}.'.\
    format(user=username, moderator=moderator_username, pwd=moderator_password, subreddit=subreddit,
            flair_text=flair_text, flair_css=flair_css))
    pass
