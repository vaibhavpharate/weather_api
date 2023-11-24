from django.contrib.auth.forms import  UserCreationForm, UserChangeForm
from .models import Clients, SiteConfig
from django.forms import ModelForm

class ClientsForm(UserCreationForm):
    class Meta:
        model = Clients
        fields = ['username','logos','email','password1','password2','client_short','role_type']


class SiteConfigForm(ModelForm):
    class Meta:
        model = SiteConfig
        fields = '__all__'
