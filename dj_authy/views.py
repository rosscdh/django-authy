# -*- coding: utf-8 -*-
from django.core import signing
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView

from . import _url_to_appropriate_authy_page
from .models import AuthyProfile
from .forms import AuthyRegisterForm, Authy2FAForm

import logging
logger = logging.getLogger('django.request')


class ProfileView(UpdateView):
    model = AuthyProfile
    form_class = AuthyRegisterForm

    def get_object(self):
        return self.request.user.authy_profile

    def get_success_url(self):
        return self.request.GET.get('next', '/')


class HoldingPageView(UpdateView):
    """
    View to prompt the user to enter their Authy Token to authenticate and continue
    """
    model = AuthyProfile
    template_name = 'dj_authy/authyholding_page.html'
    form_class = Authy2FAForm
    token = None

    def dispatch(self, request, *args, **kwargs):
        self.token = request.GET.get('token', None)

        # decode the passed in token
        if self.token:
            self.token = signing.loads(self.token, salt=settings.SECRET_KEY)
            logger.debug('Authy Session Token decoded as: %s' % self.token)

        return super(HoldingPageView, self).dispatch(request=request, *args, **kwargs)

    def get_object(self):
        return self.request.user.authy_profile

    def get_success_url(self):
        url = self.request.GET.get('next', '/')
        logger.debug('Authy HoldingPage redirect to: %s' % url)
        return url

    def form_valid(self, form):
        # setup the session
        self.request.session[self.token] = True
        logger.debug('Authy HoldingPage form is valid, now setting session token: %s to True' % self.token)
        return super(HoldingPageView, self).form_valid(form=form)


class AuthyRequiredViewMixin(object):
    """
    CBV mixin that requires authy_authentication for a specific DetailView
    """

    @property
    def authy_required_session_token(self):
        """
        provide the session token name that were validating for
        """
        return 'authy_authentication-%s-%d' % (self.__class__.__name__.lower(), self.object.pk)

    @property
    def requires_authy_authentication(self):
        """
        Check the object for the data attrib
        """
        if hasattr(self.object, 'require_authy_authentication'):
            return self.object.require_authy_authentication
        else:
            return self.object.data.get('require_authy_authentication', False)

    @property
    def is_authy_authenticated(self):
        """
        Check the session for the key
        """
        return self.authy_required_session_token in self.request.session

    def authy_redirect(self):
        """
        Redirect to our authy holding page OR redirect to the we need more info
        authy page for this user
        """
        return _url_to_appropriate_authy_page(self.request, self.authy_required_session_token)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.
        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        if not hasattr(self, 'object'):
            raise Exception('AuthyRequiredViewMixin requires a self.object in order to work')

        if self.requires_authy_authentication is True:

            if self.is_authy_authenticated is False:

                return HttpResponseRedirect(self.authy_redirect())

        return super(AuthyRequiredViewMixin, self).render_to_response(context=context, **response_kwargs)
