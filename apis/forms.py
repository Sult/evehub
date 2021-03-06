import re

from django import forms

from .models import Api
from utils.common import convert_timestamp

import utils


class ApiForm(forms.Form):

    key_ID = forms.CharField(min_length=6, max_length=7, required=True)
    verification_code = forms.CharField(
        min_length=64,
        max_length=64,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ApiForm, self).__init__(*args, **kwargs)

    def clean_key_ID(self):
        data = self.cleaned_data['key_ID']
        try:
            int(data)
        except ValueError:
            raise forms.ValidationError("Should only numbers")
        if len(data) > 7 or len(data) < 6:
            raise forms.ValidationError("Should contain 6 or 7 numbers")
        return data

    def clean_verification_code(self):
        data = self.cleaned_data['verification_code']
        if not re.match("^[A-Za-z0-9]*$", data) or len(data) != 64:
            raise forms.ValidationError(
                "Should only contain 64 letters and numbers"
            )
        return data

    def clean(self):
        key = self.cleaned_data.get('key_ID')
        vcode = self.cleaned_data.get('verification_code')
        if not key:
            return
        if not vcode:
            return

        if Api.objects.filter(key=key, vcode=vcode, user=self.user).exists():
            raise forms.ValidationError(
                "This key has already been entered, try to update it"
            )

        #connect with api and validate key
        api = utils.connection.api_connect()
        auth = api.auth(keyID=key, vCode=vcode)
        try:
            keyinfo = auth.account.APIKeyInfo()
        except RuntimeError:
            raise forms.ValidationError(
                "Invallid credentials, cannot connect to api"
            )

    def save(self, user):
        key = self.cleaned_data['key_ID']
        vcode = self.cleaned_data['verification_code']

        #connect with api and validate key
        api = utils.connection.api_connect()
        auth = api.auth(keyID=key, vCode=vcode)
        info = auth.account.APIKeyInfo()

        api = Api.objects.create(
            user=user,
            key=key,
            vcode=vcode,
            accounttype=unicode(info.key.type),
            expires=convert_timestamp(info.key.expires),
            accessmask=int(info.key.accessMask),
        )

        if api.access_to("AccountStatus"):
            account = utils.connection.accountstatus(api)
            api.paid_until = convert_timestamp(account.paidUntil)
            api.save()

        ##create related data tables
        api.create_related(info)

#https://github.com/ntt/eveapi/blob/master/apitest.py
#http://wiki.eve-id.net/APIv2_Page_Index#Character
