from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices
from model_utils.managers import InheritanceManager

from base.models import EducationalYear


LEVEL = Choices((1, 'bs'), (2, 'ms'), (3, 'doc'))


class Member(AbstractUser):
    image = models.ImageField(blank=True, null=True, upload_to='images')



class Student(Member):
    level = models.PositiveSmallIntegerField(choices=LEVEL, blank=True, null=True)
    start_year = models.ForeignKey(EducationalYear, blank=True, null=True)
    std_id = models.CharField(max_length=20, null=True, blank=True)


class Professor(Member):
    room_number = models.CharField(max_length=7, null=True, blank=True)
    room_phone = models.CharField(max_length=15, null=True, blank=True)
    research_interest = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)