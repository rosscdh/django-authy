# -*- coding: utf-8 -*-
from django.core import signing
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy


def _url_to_appropriate_authy_page(request, authy_required_session_token):
    profile = request.user.authy_profile

    if profile.cellphone is None:
        message = 'Please complete the following details before you can authenticate using authy (https://www.authy.com/).'
        url = reverse_lazy('dj_authy:profile')
    else:
        message = 'Please authenticate yourself using authy (https://www.authy.com/).'
        url = reverse_lazy('dj_authy:holding')

    token = signing.dumps(authy_required_session_token, salt=settings.SECRET_KEY)
    next = request.get_full_path()

    messages.info(request, message)

    return '{url}?token={token}&next={next}'.format(url=url, token=token, next=next)
