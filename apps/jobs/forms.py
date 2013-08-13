import logging
from django import forms
from django.forms import ModelForm
from jobs.models import Entry, Company

from tinymce.widgets import TinyMCE
from accounts.models import UserProfile

logger = logging.getLogger(__name__)

class EntryForm(ModelForm):
    class Meta:
        model = Entry 
        fields = ('job_title','location','body_html', 'howto_apply_html', 'salary', 'visibility','categories','company_name',)
        #fields = ('job_title','location','body_html', 'howto_apply_html', 'salary', 'type', 'visibility','categories','company_name',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].queryset = Company.objects.filter(author=self._user)
        

    def save(self, commit=True):
        inst = super(EntryForm, self).save(commit=False)
        inst.author = self._user
        userprofile = UserProfile.objects.get(user=self._user)
        # logger.debug("LOG: %s "  % userprofile.trusted)
        if userprofile.trusted:
            inst.status = Entry.LIVE_STATUS
        if commit:
            inst.save()
        return inst


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name','description_html','address', 'telephone', 'fax','email','url',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(CompanyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(CompanyForm, self).save(commit=False)
        inst.author = self._user
        if commit:
            inst.save()
        return inst

