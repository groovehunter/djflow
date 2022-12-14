
import yaml
from os.path import join
from django.conf import settings

import logging
lg = logging.getLogger('root')


class BaseCtrl:
    """ common methods for gui """

    def get_user_context(self):
        context = {}
        if not hasattr(self.request, 'user'):
          return {}
        if self.request.user.is_authenticated:
          context['logged_in'] = True
          context['username'] = self.request.user.username
        else:
          context['logged_in'] = False
          context['username'] = "Nobody !"
        lg.debug(context)
        return context

    def yaml_load(self):
        c = open(settings.MENU_FILE, encoding='utf8').read()
        #lg.debug('loading menu')
        self.tree = yaml.load(c, Loader=yaml.BaseLoader)

    def yamlmenu(self):
        """ create datastructure for menu rendering in template
            using menu.yaml config file """

        menudata = []
        if not self.tree:
          return menudata

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

        return menudata

    def access_denied(self):
        # self.context needed
        self.init_ctrl()
        self.template_name = 'access_denied.html'
        return self.render()
