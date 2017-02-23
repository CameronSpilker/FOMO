from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class FomoUser(AbstractUser):

#username
#password
#firstname
#lastname
#email
#birthdate

    birthdate = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    shipping_address = models.CharField(max_length=100, null=True, blank=True)
    billing_address = models.CharField(max_length=100, null=True, blank=True)
    credit_card = models.CharField(max_length=20, null=True, blank=True)
    cc_exp_date = models.DateTimeField(null=True, blank=True)
    cc_code = models.CharField(max_length=4, null=True, blank=True)



    def get_age(self):
        age = datetime.datetime.now() - self.birthdate
        return age.days
