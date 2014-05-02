django-dj_authy
====================

A Django app for integrating with dj_authy


Installation
------------

1. python setup.py
2. pip install requirements.txt
3. add dj_authy to INSTALLED_APPS

Settings
--------


__Required__


```
AUTHY_KEY : the authy key for your app
```


__Example Implementation__


```views.py
```


__Please Note__

A signal will be issued when recieving callbacks from dj_authy


__Signal Example Implementation__


```signals.py
from django.dispatch import receiver

from dj_authy.signals import dj_authy_event


@receiver(dj_authy_event)
def on_dj_authy_callback(sender, stamp_serial, **kwargs):
    # do something amazing with the data in the kwargs dict
    pass
```


__TODO__

1. tests
