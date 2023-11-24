from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model

from .models import Clients,Plans, ClientPlans, SiteConfig,VDbApi
admin.site.register(Plans)
admin.site.register(get_user_model())
admin.site.register(ClientPlans)
admin.site.register(SiteConfig)
admin.site.register(VDbApi)

 