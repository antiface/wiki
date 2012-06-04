import hashlib
import random
import string

import hmac

SECRET = 'great big secret badger boy'

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def sign(string):
    return str("%s|%s" % (string, hash_str(string)))


def validate(signed_string):
    try:
        (string, hash) = signed_string.split('|')
        if hash_str(string) == hash:
            return string
    except:
        pass


def validate_password(username, password, passwd_hash):
    (hash, salt) = passwd_hash.split('|')
    return hash == hashlib.sha256(username + password + salt).hexdigest()


def make_password_hash(password, username):
    salt = ''.join(random.choice(string.letters) for i in range(5))
    hash = hashlib.sha256(username + password + salt).hexdigest()
    return '%s|%s' % (hash, salt)