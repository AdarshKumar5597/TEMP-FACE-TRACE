from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyStudentManager(BaseUserManager):
    def create_user(self, email, studentid, studentname, password=None):
        if not email:
            raise ValueError('Student must have an email address')
        if not studentid:
            raise ValueError('Student must have a studentid')

        user = self.model(
            email=self.normalize_email(email),
            studentid=studentid,
            studentname = studentname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, studentid, password, studentname):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            studentid=studentid,
            studentname = studentname
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class Student(AbstractBaseUser):
    studentname = models.CharField(max_length=50)
    studentid = models.IntegerField(unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=100, default="")
    domain = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images", default="")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['studentid', 'studentname']

    objects = MyStudentManager()

    def __str__(self) -> str:
        return self.studentname
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        db_table = 'students'


# Attendance Database
class Attendance(models.Model):
    studentname = models.CharField(max_length=50)
    studentid = models.IntegerField()
    domain = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images", default="")
    date = models.DateField()

    def __str__(self) -> str:
        return self.studentname
    
    class Meta:
        db_table = 'attendancedb'


class Queries(models.Model):
    studentname = models.CharField(max_length=50)
    studentid = models.IntegerField()
    date = models.DateField()
    query = models.CharField(max_length=300)
    image = models.ImageField(upload_to="images", default="")

    def __str__(self) -> str:
        return self.studentname
    
    class Meta:
        db_table = 'queriesdb'