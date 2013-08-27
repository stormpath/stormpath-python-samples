stormpath-django-samples
========================

Sample applications for Django that use Stormpath for authentication.

# django-stormpath

The sample applications use django-stormpath's backend, models and views.
You should download django-stormpath and install it as per instructions.

# chirper

Chirper is a sample Twitter-like application. To use Chirper, aside from
the settings required for django-stormpath, you need to set the following in
your settings.py file:

STORMPATH_ADMINISTRATORS = "https://api.stormpath.com/v1/groups/GROUP_ID"
STORMPATH_PREMIUMS = "https://api.stormpath.com/v1/groups/GROUP_ID"

Chirper uses these two groups to determine determine the type of the user.
