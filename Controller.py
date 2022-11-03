from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.conf import settings
from .BaseCtrl import BaseCtrl
import logging
lg = logging.getLogger('root')


class Controller(BaseCtrl):

    def __init__(self, request):
        lg.debug('=========================================  init Controller')
        self.context = {}
        self.request = request
        self.init_ctrl()

    def init_ctrl(self):
        self.msg = ''
        self.context['show_nav'] = True   # show navbar by default
        self.yaml_load()
        self.yamlmenu()

        if self.request.GET:
            GET = self.request.GET
            if 'msg' in GET:
                self.context['msg'] = GET['msg']


    def render(self):
        t = loader.get_template(self.template_name)
        html = t.render(self.context, request=self.request)
        if self.msg:
            self.context['msg'] = self.msg
        self.response = HttpResponse( )
        #self.response['Cache-Control'] = 'no-cache'
        self.response.write(html)
        return self.response

    def redirect(self, url, msg=''):
        lg.debug(url)
        if msg:
            url = url + '?msg=' + msg
        lg.debug(url)
        return HttpResponseRedirect(url)

