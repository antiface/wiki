import logging
from handlers import TemplateHandler
from handlers.users import authenticate
import models


class WikiPage(TemplateHandler):
    def get(self, page_id):
        page = models.Page.get_by_key_name(page_id)
        if page:
            self.render('page_template.html', page=page)
        else:
            self.redirect('/_edit%s' % page_id)

class EditPage(TemplateHandler):
    @authenticate
    def get(self, page_id):
        page = models.Page.get_or_insert(page_id)
        self.render('edit_page.html', page=page, page_id=page_id)

    @authenticate
    def post(self, *args):
        page_id = self.request.get('page_id')
        page = models.Page.get_or_insert(page_id)
        page.content = self.request.get('content')
        page.put()
        logging.error("I'm redirecting to %s" % page_id)
        self.redirect(page_id)