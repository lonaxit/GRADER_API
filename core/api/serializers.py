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

    class Meta:
        model = SubjectPerClass
        fields = "__all__"
        
class AttendanceSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceSetting
        fields = "__all__"
        

class ResumptionSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResumptionSetting
        fields = "__all__"
        


class StudentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile
        fields = "__all__"

class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = "__all__"