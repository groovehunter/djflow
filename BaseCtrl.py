
import yaml
from os.path import join
from django.conf import settings

import logging
lg = logging.getLogger('root')


class BaseCtrl:
    """ common methods for gui """

    def yaml_load(self):
        c = open(join(settings.BASE_DIR, 'djflow/menu.yaml'), encoding='utf8').read()
        lg.debug('loading menu')
        self.tree = yaml.load(c, Loader=yaml.BaseLoader)

    def yamlmenu(self):
        """ create datastructure for menu rendering in template
            using menu.yaml config file """

        menudata = []

        if not self.tree:
            return
        for section in self.tree:
            #self.lg.debug('section %s', section )
            sec = list(section.values())[0]
            id = sec['id']
            #self.lg.debug('id %s', id )
            #self.lg.debug('sec %s', sec )
            if True:
                menudata.append( sec )
            else:
                cus_sec = {
                    'href'  :sec['href'],
                    'id'    :sec['id'],
                    'name'  :sec['name'],
                    'links' :[],
                }
                self.lg.debug('sec links %s', sec['links'])
                for item in sec['links']:
                    href = item['href']
                    if self.perm[id][href] == True:
                        cus_sec['links'].append(item)
                menudata.append( cus_sec )

        self.context['menudata'] = menudata
#        self.lg.debug('menudata %s', menudata)

    def check_user(self):
        lg.debug('check_user')
        lg.debug(self.request.user)
        if self.request.user.is_authenticated:
          self.context['logged_in'] = True
          self.context['username'] = self.request.user.username
        else:
          self.context['username'] = "Not logged in"
          self.context['logged_in'] = False
          self.prepare_tg_widget()
          self.context['username'] = "Nobody !"

    """
    def init_logging(self):
        self.lg = logging.getLogger('test')
        if not getattr(self.lg, 'handler_set', None):
            fh = logging.handlers.TimedRotatingFileHandler(TMPPATH+'/log/debug.log', when='midnight')
            fmt = '%(module)s,%(lineno)d - %(levelname)s - %(message)s'
            form = logging.Formatter(fmt=fmt)
            fh.setFormatter(form)
            self.lg.addHandler(fh)
            self.lg.setLevel(logging.DEBUG)
        self.handler_set = True
    """

    def access_denied(self):
        # self.context needed
        self.init_ctrl()
        self.template_name = 'access_denied.html'
        return self.render()

