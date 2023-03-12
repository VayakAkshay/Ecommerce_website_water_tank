from django.db import models

# Create your models here.
class OTP_Data(models.Model):
    otp_id = models.AutoField
    email_id = models.EmailField(max_length=254)
    otp = models.IntegerField(default=0)

    def __str__(self):
        return self.email_id + " " + str(self.otp)