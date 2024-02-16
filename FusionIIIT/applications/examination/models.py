from django.db import models
# your_app/models.py



class Authentication(models.Model):
    authenticator_1 = models.BooleanField(default=False)
    authenticator_2 = models.BooleanField(default=False)
    authenticator_3 = models.BooleanField(default=False)
    course = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.course} - Auth1: {self.authenticator_1}, Auth2: {self.authenticator_2}, Auth3: {self.authenticator_3}"
