from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# overriding usermanager
class CustomUserManager(BaseUserManager):

    # overriding user based authentication methord to system_usermane base authentiction
    def _create_user(self, system_username, password, **extra_fields):

        if not system_username:
            raise ValueError("The given mail must be set")
        system_username = self.normalize_email(system_username)
        user = self.model(system_username=system_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, system_username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(system_username, password, **extra_fields)


    def create_superuser(self, system_username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(system_username, password, **extra_fields)


# extrafields are added by inheriting the django default user
class NetworkSystems(AbstractUser):

    # field doesnot needed
    username = None
    last_name = None
    first_name = None

    # extra fields
    system_username = models.CharField(unique=True, max_length=50)


    USERNAME_FIELD = "system_username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



# all packages which is installed in the system
class SystemProcesses(models.Model):
    network_system = models.ForeignKey(NetworkSystems, on_delete=models.CASCADE)
    process_name = models.CharField(max_length=50)
    

# process history
class ProcessHistory(models.Model):
    system_package = models.ForeignKey(SystemProcesses, on_delete=models.CASCADE)
    memory_percent = models.FloatField()
    memory_usage = models.FloatField()
    time_stamp = models.DateTimeField(auto_now=True)

    # default sorting
    class Meta:
        ordering = ['time_stamp']