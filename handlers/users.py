import re
from handlers import TemplateHandler
from lib.signing import make_password_hash, sign, validate, validate_password
import models
import logging


def get_logged_in_user(request):
    return validate(request.cookies.get('name'))


def authenticate(function):
    def login_if_not_signed_in(*args, **kwargs):
        if get_logged_in_user(args[0].request):
            function(*args, **kwargs)
        else:
            args[0].redirect('/login')
    return login_if_not_signed_in

class IdentityHandler(TemplateHandler):
    def drop_user_cookie(self, username):
        signed_cookie_val = sign(username)
        self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % signed_cookie_val)


class Signup(IdentityHandler):
    def get(self):
        self.render('sign_up.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify =self.request.get('verify')
        email = self.request.get('email')

        model = {'username': username, 'password': password, 'verify': verify, 'email': email}
        errors = {}

        if not self._validate_username(username):
            errors['username_error'] = 'Invalid username'
        if not self._validate_password(password):
            errors['password_error'] = 'Invalid password'
        if not self._validate_verify(password, verify):
            errors['verify_error'] = 'Passwords do not match'
        if not self._validate_email(email):
            errors['email_error'] = 'Invalid email'

        if errors:
            model.update(errors)
            self.render('sign_up.html', **model)
        else:
            if self._save_user_if_new(username, password, email):
                self.drop_user_cookie(username)
                self.redirect('/welcome')
            else:
                model['username_error'] = 'Choose another username'
                self.render('sign_up.html', **model)


    def _validate_username(self, username):
        if not username:
            return False
        regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return regex.match(username)

    def _validate_password(self, password):
        if not password:
            return False
        regex = re.compile(r"^.{3,20}$")
        return regex.match(password)


    def _validate_verify(self, password, verify):
        if not password:
            return False
        if not verify:
            return False
        if not password == verify:
            return False

        return True

    def _validate_email(self, email):
        if not email:
            return True

        regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return regex.match(email)


    def _save_user_if_new(self, username, password, email):
        if models.User.get_by_key_name(username):
            return False
        else:
            passwd_hash = make_password_hash(password, username)
            return models.User.get_or_insert(username, passwd_hash=passwd_hash, email=email)

class Welcome(IdentityHandler):
    @authenticate
    def get(self):
        self.render('welcome.html', username=get_logged_in_user(self.request))


class Login(IdentityHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        model = {}
        model['username'] = self.request.get('username')
        model['password'] = self.request.get('password')

        if self._validate_user(**model):
            self.drop_user_cookie(model['username'])
            self.redirect('/welcome')

        else:
            model['login_error'] = 'Invalid login'
            self.render('login.html', **model)

    def _validate_user(self, username, password):
        user = models.User.get_by_key_name(username)
        return user and validate_password(username, password, user.passwd_hash)




class Logout(TemplateHandler):
    pass
