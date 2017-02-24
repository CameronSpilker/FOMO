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


    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)
    shipping_address = models.CharField(max_length=100, null=True)
    billing_address = models.CharField(max_length=100, null=True)
    credit_card = models.CharField(max_length=20, null=True)
    cc_exp_date = models.DateField(null=True)
    cc_code = models.CharField(max_length=4, null=True)



    def get_age(self):
        age = datetime.datetime.now() - self.birthdate
        return age.days
