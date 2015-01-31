from django.contrib import admin

from account.models import Member, Professor, Student


admin.site.register(Member)
admin.site.register(Professor)
admin.site.register(Student)