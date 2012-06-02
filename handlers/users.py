from handlers import TemplateHandler


class Signup(TemplateHandler):
    def get(self):
        self.render('sign_up.html')

class Login(TemplateHandler):
    pass

class Logout(TemplateHandler):
    pass
