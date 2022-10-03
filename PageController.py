from django.conf import settings
import os

from .Controller import Controller
from .ViewController import DjMixin

#class PageController(TemplateView, DjMixin):
class PageController(Controller):

  template_name = 'page.html'

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
