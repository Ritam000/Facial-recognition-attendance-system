from django.db import models

class Student(models.Model):
    roll_number = models.CharField(max_length=20)
    enrollment_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    stream = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='student_photos/')

    def __str__(self):
        return self.name