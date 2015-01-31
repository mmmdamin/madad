# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table(u'page_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.Comment'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Member'])),
            ('text', self.gf('ckeditor.fields.RichTextField')()),
        ))
        db.send_create_signal(u'page', ['Comment'])

        # Adding model 'Resource'
        db.create_table(u'page_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('r_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('r_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('r_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'page', ['Resource'])

        # Adding model 'Page'
        db.create_table(u'page_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('ckeditor.fields.RichTextField')()),
        ))
        db.send_create_signal(u'page', ['Page'])

        # Adding M2M table for field offered_courses on 'Page'
        db.create_table(u'page_page_offered_courses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'page.page'], null=False)),
            ('offeredcourse', models.ForeignKey(orm[u'page.offeredcourse'], null=False))
        ))
        db.create_unique(u'page_page_offered_courses', ['page_id', 'offeredcourse_id'])

        # Adding M2M table for field resources on 'Page'
        db.create_table(u'page_page_resources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'page.page'], null=False)),
            ('resource', models.ForeignKey(orm[u'page.resource'], null=False))
        ))
        db.create_unique(u'page_page_resources', ['page_id', 'resource_id'])

        # Adding model 'TeacherAssistant'
        db.create_table(u'page_teacherassistant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.Page'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Student'])),
            ('can_grade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_add_resource', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_post', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_edit_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_add_assignment', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'page', ['TeacherAssistant'])

        # Adding model 'Grade'
        db.create_table(u'page_grade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Student'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.Assignment'])),
            ('grade', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'page', ['Grade'])

        # Adding model 'OfferedCourse'
        db.create_table(u'page_offeredcourse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Course'])),
            ('professor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Professor'])),
            ('group_number', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('term', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.EducationalYear'])),
            ('exam_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'page', ['OfferedCourse'])

        # Adding unique constraint on 'OfferedCourse', fields ['course', 'group_number', 'term', 'year']
        db.create_unique(u'page_offeredcourse', ['course_id', 'group_number', 'term', 'year_id'])

        # Adding model 'Assignment'
        db.create_table(u'page_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('a_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.Page'])),
        ))
        db.send_create_signal(u'page', ['Assignment'])


    def backwards(self, orm):
        # Removing unique constraint on 'OfferedCourse', fields ['course', 'group_number', 'term', 'year']
        db.delete_unique(u'page_offeredcourse', ['course_id', 'group_number', 'term', 'year_id'])

        # Deleting model 'Comment'
        db.delete_table(u'page_comment')

        # Deleting model 'Resource'
        db.delete_table(u'page_resource')

        # Deleting model 'Page'
        db.delete_table(u'page_page')

        # Removing M2M table for field offered_courses on 'Page'
        db.delete_table('page_page_offered_courses')

        # Removing M2M table for field resources on 'Page'
        db.delete_table('page_page_resources')

        # Deleting model 'TeacherAssistant'
        db.delete_table(u'page_teacherassistant')

        # Deleting model 'Grade'
        db.delete_table(u'page_grade')

        # Deleting model 'OfferedCourse'
        db.delete_table(u'page_offeredcourse')

        # Deleting model 'Assignment'
        db.delete_table(u'page_assignment')


    models = {
        u'account.member': {
            'Meta': {'object_name': 'Member'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'account.professor': {
            'Meta': {'object_name': 'Professor', '_ormbases': [u'account.Member']},
            u'member_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.Member']", 'unique': 'True', 'primary_key': 'True'}),
            'research_interest': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'room_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'room_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'account.student': {
            'Meta': {'object_name': 'Student', '_ormbases': [u'account.Member']},
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'member_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.Member']", 'unique': 'True', 'primary_key': 'True'}),
            'start_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.EducationalYear']", 'null': 'True', 'blank': 'True'}),
            'std_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'base.course': {
            'Meta': {'object_name': 'Course'},
            'course_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'base.educationalyear': {
            'Meta': {'object_name': 'EducationalYear'},
            'current': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'page.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'a_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.Page']"}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['account.Student']", 'null': 'True', 'through': u"orm['page.Grade']", 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'page.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Member']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.Comment']"}),
            'text': ('ckeditor.fields.RichTextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'page.grade': {
            'Meta': {'object_name': 'Grade'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.Assignment']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Student']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'page.offeredcourse': {
            'Meta': {'unique_together': "(('course', 'group_number', 'term', 'year'),)", 'object_name': 'OfferedCourse'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Course']"}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'exam_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Professor']"}),
            'term': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.EducationalYear']"})
        },
        u'page.page': {
            'Meta': {'object_name': 'Page'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offered_courses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['page.OfferedCourse']", 'null': 'True', 'blank': 'True'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['page.Resource']", 'symmetrical': 'False'}),
            'teacher_assistant': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.Student']", 'through': u"orm['page.TeacherAssistant']", 'symmetrical': 'False'}),
            'text': ('ckeditor.fields.RichTextField', [], {})
        },
        u'page.resource': {
            'Meta': {'object_name': 'Resource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'r_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'r_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'page.teacherassistant': {
            'Meta': {'object_name': 'TeacherAssistant'},
            'can_add_assignment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_add_resource': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_edit_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_grade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.Page']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Student']"})
        }
    }

    complete_apps = ['page']