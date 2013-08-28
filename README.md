stormpath-django-samples
========================

Sample applications for Django that use Stormpath for authentication.

# django-stormpath

The sample applications use django-stormpath's backend, models and views.
You should download django-stormpath and install it.

# chirper
Chirper is a sample Twitter-like application.

## Setup

To use Chirper, aside from
the settings required for django-stormpath (please see django-stormpath docs),
you need to change the following in your settings.py file to the correct values:

STORMPATH_ADMINISTRATORS = "https://api.stormpath.com/v1/groups/GROUP_ID"
STORMPATH_PREMIUMS = "https://api.stormpath.com/v1/groups/GROUP_ID"

Chirper uses these two groups to determine determine the type of the user.
These groups are aren't in any way special. They're just ordinary Stormpath
groups used to keep track of application Administrators etc.

You need to make sure database and other standard Django settings are correct.
E.g. Chirper has to be specified in INSTALLED_APPS of the project.

##

Running Chirper is the same as running any other Django application.

```sh
$ python manage.py syncdb
$ python manage.py runserver
```

