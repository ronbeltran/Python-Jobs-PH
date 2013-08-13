from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile
 
class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
    
    username   = forms.CharField(label='Username', max_length=30, min_length=6, required=True, help_text='Max of 30 characters.')
    email      = forms.EmailField(label="Primary email", max_length=50, help_text='will not be shown publictly, used for notifications', required=True)
    first_name = forms.CharField(label='First name', max_length=30, required=True, help_text='Max of 30 characters.')
    last_name  = forms.CharField(label='Last name', max_length=30, required=True, help_text='Max of 30 characters.')

    def clean_username(self):
        """
        Verify that the username isn't already registered
        """
        username = self.cleaned_data.get("username")
        username = ''.join(username.lower().strip().split())
        if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
            raise forms.ValidationError(_("That username has invalid characters. The valid values are letters, numbers and underscore."))

        if User.objects.filter(username__iexact=username).exclude(
            pk=self.instance.user.pk).count() == 0:
            return username
        else:
            raise forms.ValidationError(_("The username is already registered."))
     
    class Meta:
        model = UserProfile
        fields = ('username','first_name','last_name','email','url',)
        exclude = ('user','trusted')

    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.username = self.cleaned_data['username']
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(UserProfileForm, self).save(*args,**kwargs)
        return profile
   
