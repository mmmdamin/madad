from django.db import models

# Create your models here.
from model_utils import Choices
from account.models import Professor, Student, Member
from base.models import EducationalYear, Course, Named, Logged
from ckeditor.fields import RichTextField

TERM = Choices((1, 'fall'), (2, 'spring'), (3, 'summer'))
R_TYPE = Choices((1, 'link'), (2, 'file'))


class OfferedCourse(models.Model):
    course = models.ForeignKey(Course)
    professor = models.ForeignKey(Professor)
    group_number = models.SmallIntegerField(default=1)
    term = models.PositiveSmallIntegerField(choices=TERM)
    year = models.ForeignKey(EducationalYear)
    exam_time = models.DateTimeField(null=True, blank=True)
    capacity = models.IntegerField()
    details = models.CharField(max_length=255)

    class Meta:
        unique_together = ("course", "group_number", "term", "year")

    def __unicode__(self):
        return "%s-%d - %s - %s  " % (
            unicode(self.course.course_number), self.group_number, unicode(self.course), self.professor.name)


class Grade(Logged):
    student = models.ForeignKey(Student)
    assignment = models.ForeignKey('Assignment')
    grade = models.IntegerField(null=True, blank=True)


class Assignment(Named, Logged):
    deadline = models.DateTimeField(null=True, blank=True)
    a_file = models.FileField(null=True, blank=True, upload_to='assignments')
    details = models.TextField(null=True, blank=True)
    students = models.ManyToManyField(Student, through=Grade, null=True, blank=True)
    page = models.ForeignKey('Page')


class TeacherAssistant(models.Model):
    page = models.ForeignKey('Page')
    student = models.ForeignKey(Student)
    can_grade = models.BooleanField(default=False)
    can_add_resource = models.BooleanField(default=False)
    can_post = models.BooleanField(default=False)
    can_edit_page = models.BooleanField(default=False)
    can_add_assignment = models.BooleanField(default=False)


class Resource(models.Model):
    r_url = models.URLField(null=True, blank=True)
    r_file = models.FileField(null=True, blank=True, upload_to='resources')
    r_type = models.PositiveSmallIntegerField(choices=R_TYPE)


class Page(models.Model):
    offered_courses = models.ManyToManyField(OfferedCourse, null=True, blank=True)
    resources = models.ManyToManyField(Resource)
    teacher_assistant = models.ManyToManyField(Student, through=TeacherAssistant)
    text = RichTextField(config_name='full_ckeditor')


class Comment(Logged):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self')
    author = models.ForeignKey(Member)
    text = RichTextField(config_name='full_ckeditor')