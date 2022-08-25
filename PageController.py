from django.conf import settings
import os

from .Controller import Controller

class PageController(Controller):

    def __init__(self, request):
        Controller.__init__(self, request)
        self.template_name = 'page.html'

    def home(self):
        self.template_name = 'base.html'
        return self.render()


    def page(self, name):
      self.name = name
      rpath = 'con/'+name+'.md'
      with open(os.path.join(settings.BASE_DIR, rpath)) as f:
        content = f.read()

      self.context.update( 
        {'name' : name, 
        'con'   : content,
        }
      )
      return self.render()

