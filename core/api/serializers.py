from dataclasses import fields
from rest_framework import serializers
# import models
from core.models import *
from django.db.models import Q, Sum, Avg, Max, Min, Count
from django.db.models import F
User = get_user_model()

class TermSerializer(serializers.ModelSerializer):

    class Meta:
        model = Term
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = "__all__"

class SchoolClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolClass
        fields = "__all__"
        
class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"
        
        
class SubjectPerClassSerializer(serializers.ModelSerializer):
    term_name = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    class Meta:
        model = SubjectPerClass
        fields = "__all__"
        
    def get_term_name(self,object):
               
        term = Term.objects.get(pk=object.term.pk)
        return term.name
    
    def get_session_name(self,object):
               
        session = Session.objects.get(pk=object.session.pk)
        return session.name
    
    def get_class_name(self,object):
               
        classObj = SchoolClass.objects.get(pk=object.sch_class.pk)
        return classObj.class_name
    
    
class AttendanceSettingSerializer(serializers.ModelSerializer):
    
    term_name = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSetting
        fields = "__all__"
        
    def get_term_name(self,object):
               
        term = Term.objects.get(pk=object.term.pk)
        return term.name
    
    def get_session_name(self,object):
               
        session = Session.objects.get(pk=object.session.pk)
        return session.name
        

class ResumptionSettingSerializer(serializers.ModelSerializer):
    term_current = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()

    class Meta:
        model = ResumptionSetting
        fields = "__all__"
    
    def get_term_current(self,object):
               
        term = Term.objects.get(pk=object.current_term.pk)
        return term.name
    
    def get_session_name(self,object):
               
        session = Session.objects.get(pk=object.session.pk)
        return session.name


# subject teacher serializer
class SubjectTeacherSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField(read_only=True)
    teacher_name = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    class Meta:
        model = SubjectTeacher
        fields = "__all__"
    
    def get_teacher_name(self,object):
               
        teacherObj = User.objects.get(pk=object.teacher.pk)
        return teacherObj.sur_name + ' ' + teacherObj.first_name
    
    def get_session_name(self,object):
               
        session = Session.objects.get(pk=object.session.pk)
        return session.name
    
    def get_class_name(self,object):
               
        _class = SchoolClass.objects.get(pk=object.classroom.pk)
        return _class.class_name
    
    def get_subject_name(self,object):
               
        _subject = Subject.objects.get(pk=object.subject.pk)
        return _subject.name


class SubjectTeacherToggleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubjectTeacher
        fields = "__all__"