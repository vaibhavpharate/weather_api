from .models import SiteConfig, VDbApi

class MyDBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model == SiteConfig:
            return 'site_configs'
        elif model == VDbApi:
            return 'data_api'
        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model == SiteConfig:
            return 'site_configs'
        elif model == VDbApi:
            return 'data_api'
        return None

