from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# overriding usermanager
class CustomUserManager(BaseUserManager):

    # overriding user based authentication methord to email base authentiction
    def _create_user(self, system_id, password, **extra_fields):

        if not system_id:
            raise ValueError("The given mail must be set")
        system_id = self.normalize_email(system_id)
        user = self.model(system_id=system_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, system_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(system_id, password, **extra_fields)


    def create_superuser(self, system_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(system_id, password, **extra_fields)


# custom customer for user 
# extrafields are added to by inheriting the django user
class NetworkSystems(AbstractUser):

    # field doesnot needed
    username = None
    first_name = None
    last_name = None

    # extra fields
    system_id = models.CharField(unique=True)
    
    USERNAME_FIELD = "system_id"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


# system general information table
class SystemPerformance(models.Model):
    network_system = models.ForeignKey(NetworkSystems, on_delete=models.CASCADE)
    prosessor_usage = models.CharField()
    memmory_usage = models.CharField()
    hdd_usage = models.CharField()


# all pachages which is installed in the system
class SystemPackages(models.Model):
    network_system = models.ForeignKey(NetworkSystems, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=50)
    # other_info
    installed_time_stamp = models.DateTimeField(auto_now=True)


class PackageUsageHistory(models.Model):
    system_package = models.ForeignKey(SystemPackages, on_delete=models.CASCADE)
    # other package fields
    time_stamp = models.DateTimeField(auto_now=False)
    is_running = models.BooleanField(default=False)
