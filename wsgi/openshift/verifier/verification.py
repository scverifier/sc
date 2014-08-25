import praw
import settings
from praw import Reddit


class RedditAPIException(Exception):
    pass


class InvalidLoginException(RedditAPIException):
    pass


class RateLimitExceededException(RedditAPIException):
    pass


class ModeratorRequiredException(RedditAPIException):
    pass


class InvalidCSSException(RedditAPIException):
    pass


class InvalidUserException(RedditAPIException):
    pass


def verify(moderator_username, moderator_password,
           username, subreddit,
           flair_text=None, flair_css=None):
    api = Reddit(user_agent=settings.USER_AGENT)
    try:
        api.login(moderator_username, moderator_password)
        subreddit = api.get_subreddit(subreddit)
        subreddit.add_contributor(username)
        api.set_flair(subreddit, username, flair_text, flair_css)
    except praw.errors.RateLimitExceeded:
        raise RateLimitExceededException
    except praw.errors.ModeratorRequired:
        raise ModeratorRequiredException
    except praw.errors.InvalidUserPass:
        raise InvalidLoginException
    except praw.errors.BadCSS:
        raise InvalidCSSException
    except praw.errors.InvalidUser:
        raise InvalidUserException
    except praw.errors.APIException as e:
        raise RedditAPIException(e)
    except praw.errors.ClientException as e:
        raise RedditAPIException(e)
