from django.db import models
from django.contrib.auth.models import User
from flp.settings import BASE_URL


class MailVerification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_code = models.CharField(max_length=200, null=True, blank=True)
    mail_id = models.CharField(max_length=200)
    time_limit = models.DateField(null=True)
    mail_type = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    # Mail Types:
    # 1. 0 --> User registration verification
    # 2. 1 --> User Forgot password
    # 3. 2 --> User email change


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pic = models.FileField(upload_to='pics/', blank=True, null=True)

    def __str__(self):
        return self.user.__str__()