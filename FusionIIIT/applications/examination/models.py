from django.db import models
from django.utils import timezone

# your_app/models.py


from django.db import models

class Authentication(models.Model):
    authenticator_1 = models.BooleanField(default=False)
    authenticator_2 = models.BooleanField(default=False)
    authenticator_3 = models.BooleanField(default=False)
    course = models.CharField(max_length=255, default="")
    timestamp = models.DateTimeField(default=timezone.now)  
    def save(self, *args, **kwargs):

        self.timestamp = timezone.now()
        super(Authentication, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course} - Auth1: {self.authenticator_1}, Auth2: {self.authenticator_2}, Auth3: {self.authenticator_3}"


class hidden_grades(models.Model):
    student_id = models.CharField(max_length=20)
    course_id = models.CharField(max_length=50)
    semester_id = models.CharField(max_length=10)
    grade = models.CharField(max_length=5,default="C")