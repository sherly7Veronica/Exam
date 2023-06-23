from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin

from .models import CustomUser, SuperAdmin, Teacher, Student

admin.site.register(CustomUser)
admin.site.register(SuperAdmin, GroupAdmin)
admin.site.register(Teacher, GroupAdmin)
admin.site.register(Student, GroupAdmin)
