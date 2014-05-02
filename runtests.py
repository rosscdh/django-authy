# -*- coding: utf-8 -*-
import os, sys
from django.conf import settings
from django.core.management import call_command

DIRNAME = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DIRNAME, 'database.db'),
    }
}

settings.configure(DEBUG = True,
                   DATABASES=DATABASES,
                   USE_TZ=True,
                   AUTHY_KEY='12345678910111213141516171819201234567891011121314151617181920',
                   ROOT_URLCONF='authy.urls',
                   PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),  # simple fast hasher but not secure
                   INSTALLED_APPS = ('django.contrib.auth',
                                     'django.contrib.contenttypes',
                                     'django.contrib.sessions',
                                     'django.contrib.admin',
                                     'authy',))


from django.test.simple import DjangoTestSuiteRunner

call_command('syncdb', interactive=False)

failures = DjangoTestSuiteRunner().run_tests(['authy',], verbosity=1)
if failures:
    sys.exit(failures)