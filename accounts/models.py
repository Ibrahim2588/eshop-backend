from django.utils import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser


def userImage(instance, filename):
    email = instance.email
    upload_to = f'img/profile/{email[:5]}/'

    ext = filename.split('.')[-1]
    filename = f'{email[:5]}.{ext}'

    return upload_to+filename



class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user




class UserModel(AbstractUser):

    username = models.CharField(
        _("username"),
        max_length=150,
        null=True,
        blank=True,
    )
    
    email = models.EmailField(
        verbose_name=_("email address"), 
        blank=True,
        unique=True,
    )

    image = models.ImageField(
        verbose_name=_('image'),
        upload_to=userImage,
        null=True,
        blank=True,
    )

    last_login = models.DateTimeField(
        verbose_name=_('last login'), 
        blank=True, 
        null=True
        )
    
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

