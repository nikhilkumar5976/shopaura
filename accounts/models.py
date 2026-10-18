from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ==============================================================================
# Custom User Manager
# ==============================================================================

class MyAccountManager(BaseUserManager):
    """
    Custom manager for the Account model.
    Handles regular user creation and superuser creation using email as the unique identifier.
    """
    def create_user(self, first_name, last_name, username, email, password=None):
        """
        Create and return a standard user with an email, username, first name, and last name.
        """
        if not email:
            raise ValueError('User must provide an email address.')

        if not username:
            raise ValueError('User must provide a username.')

        # Normalize the email domain and instantiate model
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        # Hash and set the password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        """
        Create and return a superuser with full administrative permissions.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        # Grant elevated administrative privileges
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# ==============================================================================
# Custom Account Model
# ==============================================================================

class Account(AbstractBaseUser):
    """
    Custom user model extending AbstractBaseUser.
    Uses 'email' instead of 'username' for authentication (USERNAME_FIELD = 'email').
    Includes custom fields and administrative permission checks.
    """
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10)

    # Required system tracking fields
    date_joined  = models.DateTimeField(auto_now_add=True)
    last_login   = models.DateTimeField(auto_now_add=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=False)
    is_superadmin= models.BooleanField(default=False)

    # Authentication field configuration
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Check if user has a specific permission. Admins have all permissions."""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Check if user has permissions to view the app/module."""
        return True