from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom User Manager to handle user creation with email instead of username
class UserManager(BaseUserManager):
    """
    Custom manager for User model where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        # Normalize the email address by lowercasing the domain part of it
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # Safely hash the password before saving
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model inheriting from AbstractBaseUser
# This completely replaces Django's default User model giving us full control
class User(AbstractBaseUser):
    """
    Custom User model representing a registered user in the system.
    Users can be admins, residents, or security guards based on their role.
    """
    
    # Required methods to handle Django admin permissions
    def has_perm(self, perm, obj=None):
        """
        Checks if the user has a specific permission.
        Admins have all permissions.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Checks if the user has permissions to view the app `app_label`.
        Admins have all module permissions.
        """
        return self.is_admin
        
    # We use email as the primary unique identifier for authentication
    email = models.EmailField(unique=True)
    
    # RBAC Support: defining the available roles
    role_choice =(
        ('admin','Admin'),
        ('resident','Resident'),
        ('security','Security Guard'),
    )
    # The default role for any new user is resident
    role = models.CharField(max_length=20,choices=role_choice,default='resident')
    
    # Standard fields for Django administration and user state
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Link our custom User model to our custom UserManager
    objects = UserManager()

    # Override the default username field to use email for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # String representation of the object, helpful for Django Admin panel
    def __str__(self):
        return self.email

class OTPVerification(models.Model):
    """
    Model to store OTP codes sent to users for password reset.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_requests')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.otp_code}"