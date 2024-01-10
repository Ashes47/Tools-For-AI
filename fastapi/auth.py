import os


def validateToken(token):
    if token == os.environ["token"]:
        return True

    return False
