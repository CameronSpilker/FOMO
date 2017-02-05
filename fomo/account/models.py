from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class FomoUser(AbstractUser):

#username
#password
#
# CONTACT_CHOICES = (
# ['text', 'Test'],
# ['email', 'Email'],
# ['voice', 'Voice'],
# )


    birthdate = models.DateTimeField(null=True)
    gender = models.CharField(max_length=1)
    shipping_address = models.CharField(max_length=100, null=True)
    billing_address = models.CharField(max_length=100, null=True)
    credit_card = models.CharField(max_length=20)
    cc_exp_date = models.DateTimeField(null=True)
    cc_code = models.CharField(max_length=4)
    # pref_contact = models.CharField(null=True, blank=True, choices=CONTACT_CHOICES)

    def get_age(self):
        age = datetime.datetime.now() - self.birthdate
        return age.days
