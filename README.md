django-authy
====================

A Django app for integrating with authy


Installation
------------

1. python setup.py
2. pip install requirements.txt
3. add dj_authy to INSTALLED_APPS

Settings
--------


__Required__


```
AUTHY_KEY : the authy key for your app (ensure to use production key for production and sandbox key for dev)
AUTHY_IS_SANDBOXED : this should be True when you are using the sandbox
```


__Overview__

dj_authy appends authy_profile to the default django User object

```
user = User.objects.get(pk=1)

profile = user.authy_profile

profile.cellphone = '+4917627266561'
# note the +49 this is important, as profile.cellphone.national_number and profile.cellphone.country_code are derived from this 
profile.save()

service = profile.service  # the authy service wrapper
# service will automatically create the authy.user if we dont already have an authy_id for it
service.verify_token(0000000)  # user entered token;
```



__TODO__

1. tests
