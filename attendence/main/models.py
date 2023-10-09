from django.db import models


class GroupModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudentModel(models.Model):
    full_name = models.CharField(max_length=100)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name


class AttendanceModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    is_come = models.BooleanField(default=True)
    day = models.DateField()

    def __str__(self):
        return self.student.full_name
