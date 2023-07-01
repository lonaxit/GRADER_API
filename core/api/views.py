import random
import string
import math
import json
import io, csv, pandas as pd
from users.serializers import *
from core.api.serializers import *
# from profiles.api.serializers import *
from core.api.permissions import *
# from core.api.utilities import *

# # import models
from core.models import *
from django.contrib.auth import get_user_model
# from django.db.models import Q, Sum, Avg, Max, Min
from django.db import transaction
from django.shortcuts import get_object_or_404
# # from rest_framework import mixins
from rest_framework import generics, status
# # import validation errors
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import *
# # import Response
from rest_framework.response import Response
# # import here below used for class based views
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser,FormParser

import openpyxl
User = get_user_model()


class TermListCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class TermDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Term.objects.all()
    serializer_class = TermSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

class SessionListCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class SessionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Session.objects.all()
    serializer_class = SessionSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class SchoolClassCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class SchoolClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

class SubjectCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class SubjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    

class SubjectPerClassCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = SubjectPerClass.objects.all()
    serializer_class = SubjectPerClassSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class SubjectPerClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =SubjectPerClass.objects.all()
    serializer_class = SubjectPerClassSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
    
class AttendanceSettingsCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = AttendanceSetting.objects.all()
    serializer_class = AttendanceSettingSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class AttendanceSettingsClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =AttendanceSetting.objects.all()
    serializer_class = AttendanceSettingSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    


class ResumptionSettingsCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = ResumptionSetting.objects.all()
    serializer_class = ResumptionSettingSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class ResumptionSettingsClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResumptionSetting.objects.all()
    serializer_class = ResumptionSettingSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    

class StudentProfileCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class StudentProfileClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

class TeacherProfileCreateAPIView(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class TeacherProfileClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

class SubjectTeacherListAPIView(generics.ListAPIView):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
# create a subject teacher given a userid
class SubjectTeacherCreateAPIView(generics.CreateAPIView):
    
    serializer_class = SubjectTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
    def get_queryset(self):
        # just return the subjectteacher object
        return SubjectTeacher.objects.all()
     
    #  we need to overwrite the current function becos we need to pass the current movie ID for which review is being created
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        
        # get movie
        user= User.objects.get(pk=pk)
        
        subject = serializer.validated_data['subject']
        classroom = serializer.validated_data['classroom']
        
        # subject = Subject.objects.get(pk=subject_id)
        # classroom = SchoolClass.objects.get(pk = classroom_id)
        
        # logic to prevent multple creation of subjectteacher by a user
        _queryset = SubjectTeacher.objects.filter(teacher=user,subject=subject,classroom=classroom)
        
        if _queryset.exists():
            
            raise ValidationError("You are already a subject teacher")
        # custom calculations
        # check if rating is 0 
        # if movie.number_rating == 0:
        #     movie.avg_rating = serializer.validated_data['rating']
        # else:
        #     movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
        # # increase the rating  
        # movie.number_rating = movie.number_rating + 1
        
        # # save
        # movie.save()
        
        # save together with related watchlist and user
        serializer.save(teacher=user)


class ToggleSubjectTeacherAPIView(generics.RetrieveUpdateAPIView):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer
    # lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = not instance.status # Toggle the status
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SubjectTeacherClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]



# create class teacher using userid
class ClassTeacherListAPIView(generics.ListAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
# create a class teacher given a userid
class ClassTeacherCreateAPIView(generics.CreateAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
    def get_queryset(self):
        # just return the subjectteacher object
        return ClassTeacher.objects.all()
     
    #  we need to overwrite the current function becos we need to pass the current movie ID for which review is being created
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        
        # get movie
        user= User.objects.get(pk=pk)
        
        term = serializer.validated_data['term']
        classroom = serializer.validated_data['classroom']
        session = serializer.validated_data['session']
        
        # logic to prevent multple creation of class teacher by a user
        _queryset = ClassTeacher.objects.filter(tutor=user,term=term,classroom=classroom,session=session)
        
        if _queryset.exists():
            
            raise ValidationError("Record already exist")
        
        serializer.save(tutor=user)


class ToggleClassTeacherAPIView(generics.RetrieveUpdateAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
   
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = not instance.status # Toggle the status
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ClassTeacherClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
