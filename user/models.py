from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    email=models.EmailField(unique=True)
    username=models.CharField(max_length=50,unique=True)
    mobile=models.CharField(max_length=15,unique=True)
    gender_choice = [
    ('male', 'Male'),
    ('female', 'Female'),
]
    gender=models.CharField(choices=gender_choice, max_length=12)
    nation=models.CharField( max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    mandal=models.CharField(max_length=50)
    village=models.CharField(max_length=50)
    pincode=models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ["email", "mobile", "gender", "nation", "state", "city", "mandal", "village", "pincode"]


    def save(self,*args, **kwargs):
        if self.pk:
            old=User.objects.get(pk=self.pk)
            self.username=old.username
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} ({self.gender})"

    


