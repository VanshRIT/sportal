# students/models.py
from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=10, unique=True)

    # Add other fields specific to a student

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
