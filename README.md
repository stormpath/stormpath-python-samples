#Stormpath is Joining Okta
We are incredibly excited to announce that [Stormpath is joining forces with Okta](https://stormpath.com/blog/stormpaths-new-path?utm_source=github&utm_medium=readme&utm-campaign=okta-announcement). Please visit [the Migration FAQs](https://stormpath.com/oktaplusstormpath?utm_source=github&utm_medium=readme&utm-campaign=okta-announcement) for a detailed look at what this means for Stormpath users.

We're available to answer all questions at [support@stormpath.com](mailto:support@stormpath.com).

stormpath-python-samples
========================

Sample Python applications demonstrating the various Stormpath use cases.

# Chirper

Chirper is a sample Twitter-like application.

The sample application uses the
[stormpath-django](https://github.com/stormpath/stormpath-django) plugin for
providing Django authentication backend, User models and views integrated
with the Stormpath authentication service.

You should have the `stormpath-django` Python module installed before trying
to start Chirper sample application.

## Setup

To use Chirper, aside from the settings required for stormpath-django (please
see the django-stormpath documentation), you need to change the following in
your settings.py file to the correct values:

    STORMPATH_ADMINISTRATORS = "https://api.stormpath.com/v1/groups/GROUP_ID"
    STORMPATH_PREMIUMS = "https://api.stormpath.com/v1/groups/GROUP_ID"

Chirper uses these two groups to determine determine the type of the user.
These groups are aren't in any way special. They're just ordinary Stormpath
groups used to keep track of application Administrators etc.

You need to make sure database and other standard Django settings are correct.
E.g. Chirper has to be specified in INSTALLED_APPS of the project.

## Running it

Running Chirper is the same as running any other Django application.

```sh
$ python manage.py syncdb
$ python manage.py runserver
```
