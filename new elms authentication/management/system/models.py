from django.db import models

from django.contrib.auth.models import User

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("add_employee", "Can add employees"),
        ]
    

    def __str__(self):
        return self.user.username
    @property
    def employees(self):
        
        return self.employees.all()


class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE,related_name='employees')

    def __str__(self):
        return self.username