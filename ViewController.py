from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.conf import settings

from .BaseCtrl import BaseCtrl

import logging
lg = logging.getLogger('root')


class DjMixin(BaseCtrl):
  # kann anders heissen
  def djflow_context_data(self):
    """ load context data of navigation and user """
    c = self.get_user_context()
    self.yaml_load()
    menudata = self.yamlmenu()
    menu = {'menudata': menudata}
    c.update(menu)
    return c


class ViewControllerSupport(BaseCtrl):
    """ lightweight ctrl methods to add abilities to django
        generic views:
        - navigation blocks
        - custom render method
    """
    context = {}

    def init_ctrl(self):
        lg.debug('init_ctrl - VCS')
        self.context = self.get_user_context()
        self.fields_noshow = []
        if settings.DEBUG2:
            self.context['debug2'] = True
        self.msg = ''
        self.context['show_nav'] = True   # show navbar by default

        self.yaml_load()
        menudata = self.yamlmenu()
        #lg.debug(menudata)
        self.context.update( {'menudata':menudata} )

        if self.request.GET:
            GET = self.request.GET
            if 'msg' in GET:
                self.context['msg'] = GET['msg']

    def helper_detailview(self):
        modlabel = self.model._meta.label
        try:
            app, modl = modlabel.split('.')
        except:
            app = 'na'
            modl = modlabel

        test = 'BROKEN'
        try:
            url = self.model.get_absolute_url()
            test = 'OK'
        except:
            url = '/{0}/{1}'.format(app,modl.lower())
#            url = 'BROKEN'
        c = {
            'keys'  : self.fields,
            'url'   : url,
        }
        if settings.DEBUG:
            c['debug'] = True
            c['test'] = test
        return c

    def listview_helper(self):
        keys = self.model._meta.get_fields()
        field_names = [k.name for k in keys]
#        self.lg.debug('removed fields from display: %s', self.fields_noshow)
        for f in self.fields_noshow:
            if f in field_names:
                field_names.remove(f)
        field_names.remove('id')
        (app, modl) = self.model._meta.label.split('.')
        try:
            url = self.model.get_absolute_url()
        except:
            url = '/{0}/{1}'.format(app,modl.lower())
        url_detail = url
        c = {
            'app'   : app.capitalize(),
            'modl'  : modl,
            'keys'  : field_names,
            'url'   : url,
            'url_detail': url_detail,
        }
        if settings.DEBUG:
            c['debug'] = True
        return c

    def render(self):
        lg.debug(self.template_name)
        t = loader.get_template(self.template_name)
        if (hasattr(self, 'msg') and self.msg):
            self.context['msg'] = self.msg
        html = t.render(self.context, request=self.request)
        response = HttpResponse( )
        response.write(html)
        return response
