from django.contrib import admin

# Register your models here.
from .models import Student, Attendance, Queries, ImageDetails
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Queries)
admin.site.register(ImageDetails)

