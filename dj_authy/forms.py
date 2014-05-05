# -*- coding: utf-8 -*-
from django import forms

from .models import AuthyProfile


class BaseAuthyMediaForm(forms.ModelForm):
    """
    Use provided authy media
    """
    class Media:
        css = {
            'all': ('//cdnjs.cloudflare.com/ajax/libs/authy-forms.css/2.0/form.authy.min.css',)
        }
        js = ('//cdnjs.cloudflare.com/ajax/libs/authy-forms.js/2.0/form.authy.min.js',)


class AuthyRegisterForm(BaseAuthyMediaForm):
    """
    For the user to change or create their authy profile
    """
    country = forms.CharField(label='Your Country', widget=forms.Select(attrs={'id': 'authy-countries'}))
    cellphone = forms.CharField(label='Your Cellphone Number', widget=forms.TextInput(attrs={'id': 'authy-cellphone'}))
    is_smartphone = forms.BooleanField(help_text='Smartphones generally; are those with a touch screen', initial=True)

    class Meta:
        model = AuthyProfile
        fields = ('country', 'cellphone', 'is_smartphone',)

    def __init__(self, instance, *args, **kwargs):
        super(AuthyRegisterForm, self).__init__(*args, instance=instance, **kwargs)

        # override the attrs with our initial value (as authy forms doesnt handle this case)
        attrs = self.fields['country'].widget.attrs
        attrs.update({'data-initial': self._get_country_prefix(instance=instance)})
        self.fields['country'].widget.attrs = attrs

        # set the modified cellphone (removes the country code)
        self.initial['cellphone'] = self._get_cellphone(instance=instance)
        self.fields['cellphone'].initial = self.initial['cellphone']

    def _get_country_prefix(self, instance):
        return instance.cellphone.country_code

    def _get_cellphone(self, instance):
        return instance.cellphone.national_number

    def clean_cellphone(self):
        """
        1. Remove the leading 0 (if present)
        2. prepend the countries prefix
        """
        country = self.cleaned_data.get('country')
        cellphone = self.cleaned_data.get('cellphone')
        cellphone = cellphone[1:] if cellphone[0] == '0' else cellphone
        # prepend + to the country and number
        return '+%s%s' % (country, cellphone)

    def save(self, *args, **kwargs):
        self.cleaned_data.pop('country')  # remove the country as its not actually part of this object

        obj = super(AuthyRegisterForm, self).save(*args, **kwargs)
        #
        # Get the authy user_id from authy
        #
        if obj.authy_id is None:
            obj.service  # call the service which automatically checks the user is present

        return obj


class Authy2FAForm(BaseAuthyMediaForm):
    """
    Authentication Form for Authy
    """
    token = forms.CharField(label='Authy Token', help_text='Please enter the authy token obtained by installing the authy app on your cellphone or the browser extension.', widget=forms.TextInput(attrs={'id': 'authy-token'}))

    class Meta:
        model = AuthyProfile
        fields = ()

    def clean_token(self):
        token = self.cleaned_data.get('token')
        authy_service = self.instance.service

        if authy_service.verify_token(token) is False:
            raise forms.ValidationError('Sorry, that Authy Token is not valid: %s' % authy_service.errors.get('message', 'Unknown Error'))


    def save(self, *args, **kwargs):
        """
        Do nothing here, were using modelForm to get access to the instance
        but not actually updating anythign just validating the authy token
        """
        return self.instance
