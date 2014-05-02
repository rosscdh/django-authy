from setuptools import setup

setup(
    name="authy",
    packages=['authy'],
    version='0.1.0',
    author="Ross Crawford-d'Heureuse",
    license="MIT",
    author_email="ross@lawpal.com",
    url="https://github.com/rosscdh/django-authy",
    description="A Django app for integrating with authy",
    zip_safe=False,
    include_package_data=True,
    install_requires = [
        'authy',
        'django-phonenumber-field',
    ]
)
