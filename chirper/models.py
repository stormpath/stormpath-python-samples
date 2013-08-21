from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)

class StormpathUserManager(BaseUserManager):

    def create_user(self, email, username, given_name, surname, url, password):

        if not email:
            raise ValueError("Users must have an email address")

        if not given_name or not surname:
            raise ValueError("Users must provide a given name and a surname")

        user = self.model(email=StormpathUserManager.normalize_email(email),
            given_name=given_name, surname=surname, url=url)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args):

        user = self.create_user(args)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class StormpathUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255)
    given_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'given_name', 'surname']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = StormpathUserManager()

    def get_full_name(self):
        return "{0} {1}".format(self.given_name, self.surname)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.get_full_name()
