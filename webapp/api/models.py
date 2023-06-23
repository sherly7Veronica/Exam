from django.contrib.auth.models import AbstractUser, Group

class CustomUser(AbstractUser):
    pass

class SuperAdmin(Group):
    pass

class Teacher(Group):
    pass

class Student(Group):
    pass
