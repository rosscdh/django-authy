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


__Example Implementation__


```views.py
```


__TODO__

1. tests
