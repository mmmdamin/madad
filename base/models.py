from django.db import models
from model_utils import Choices

YEAR_TERM = Choices((0, 'not current'), (1, 'fall'), (2, 'spring'), (3, 'summer'))


class Logged(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        abstract = True


class Named(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class EducationalYear(models.Model):
    year = models.IntegerField()
    current = models.PositiveSmallIntegerField(choices=YEAR_TERM)

    def __unicode__(self):
        return unicode(self.year)


class Course(Named):
    course_number = models.CharField(max_length=10, unique=True)