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

from core.api.utilities import *


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


class ClassTeacherDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]


# scores
class ScoresListAPIView(generics.ListAPIView):
    queryset = Scores.objects.all()
    serializer_class = ScoresSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]

# create individual score
class ScoresCreateAPIView(generics.CreateAPIView):
    queryset = Scores.objects.all()
    serializer_class = ScoresSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
    def get_queryset(self):
        # just return the subjectteacher object
        return Scores.objects.all()
     
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        
        # get movie
        user= User.objects.get(pk=pk)
        
        term = serializer.validated_data['term']
        studentclass = serializer.validated_data['studentclass']
        session = serializer.validated_data['session']
        subject = serializer.validated_data['subject']
        
        teacher = self.request.user
        
        _isteacher = SubjectTeacher.objects.filter(teacher=teacher,classroom=studentclass,session=session,subject=subject)
        if not _isteacher:
            raise ValidationError("You are not a subject teacher for this class")
            
        
        # logic to prevent multple creation of record
        _queryset = Scores.objects.filter(user=user,term=term,studentclass=studentclass,session=session,subject=subject)
        
        if _queryset.exists():
            
            raise ValidationError("Record already exist")
        
        serializer.save(user=user,subjectteacher=SubjectTeacher.objects.get(pk=teacher.pk))
        

# score detail
class ScoresDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scores.objects.all()
    serializer_class = ScoresSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]



    
class CreateResult(generics.CreateAPIView):
    serializer_class = ResultSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Result.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        
        with transaction.atomic():
            
            try:
                # Access form values from the request object
                _class = request.data.get('studentclass')
                term = request.data.get('term')
                session = request.data.get('session')
                
                classObj = SchoolClass.objects.get(pk=_class)
                termObj = Term.objects.get(pk=term)
                sessionObj = Session.objects.get(pk=session)
                
                loggedInUser = request.user
                
                _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                if not _isteacher:
                    raise ValidationError("You are not a class teacher for this class")
                
                
                # process terminal result
                processTerminalResult(request,classObj,termObj,sessionObj)

                    # process terminal result
                    # processAnnualResult(score)

                    # Add auto comment
                    # autoAddComment(score.studentclass,score.session,score.term)

                    # proccess Affective domain
                    # processAffective(score)

                    # process Psychomotor domain
                    # processPsycho(score)
                
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Result created successfully'},
                status = status.HTTP_201_CREATED
                )
    


# List all result based on term, class, session
class GetResult(generics.ListAPIView):
    serializer_class = ResultSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        _class = self.request.data.get('classroom')
        _session = self.request.data.get('session')
        _term = self.request.data.get('term')
        
        # Example: Fetching data based on a filter field named 'filter_field'
        queryset = Result.objects.filter(studentclass=_class,session=_session,term=_term)
        
        if not queryset:
            raise ValidationError("No records matching your criteria")
        return queryset

# Detail Result
class ResultDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

# retrieve all result given a student id
class UserResultList(generics.ListAPIView):
    serializer_class = ResultSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
        pk = self.kwargs.get('pk')
        
        # Example: Fetching data based on a filter field named 'filter_field'
        queryset = Result.objects.filter(student=pk)
        
        if not queryset:
            raise ValidationError("No records available")
        return queryset
    

class CreateStudentAffectiveTraits(generics.CreateAPIView):
    serializer_class = StudentaffectiveSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Studentaffective.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        
        with transaction.atomic():
            
            try:
                # Access form values from the request object
                _class = request.data.get('studentclass')
                term = request.data.get('term')
                session = request.data.get('session')
                
                classObj = SchoolClass.objects.get(pk=_class)
                termObj = Term.objects.get(pk=term)
                sessionObj = Session.objects.get(pk=session)
                
                loggedInUser = request.user
                
                _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                if not _isteacher:
                    raise ValidationError("You are not a class teacher for this class")
                
                
               # proccess Affective domain
                processAffective(classObj,sessionObj,termObj)

            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Student affective traits created successfully'},
                status = status.HTTP_201_CREATED
                )
        
class CreateStudentPsychoTraits(generics.CreateAPIView):
    serializer_class = StudentpsychomotorSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Studentpsychomotor.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        
        with transaction.atomic():
            
            try:
                # Access form values from the request object
                _class = request.data.get('studentclass')
                term = request.data.get('term')
                session = request.data.get('session')
                
                classObj = SchoolClass.objects.get(pk=_class)
                termObj = Term.objects.get(pk=term)
                sessionObj = Session.objects.get(pk=session)
                
                loggedInUser = request.user
                
                _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                if not _isteacher:
                    raise ValidationError("You are not a class teacher for this class")

                # process Psychomotor domain
                processPsycho(classObj,sessionObj,termObj)

                    
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Student psycho traits created successfully'},
                status = status.HTTP_201_CREATED
                )
        

# ratings
class RatingCreateAPIView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class RatingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
# Psychomotor
class PsychomotorCreateListAPIView(generics.ListCreateAPIView):
    queryset = Psychomotor.objects.all()
    serializer_class = PsychomotorSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class PyschomotorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Psychomotor.objects.all()
    serializer_class = PsychomotorSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
class AffectiveCreateListAPIView(generics.ListCreateAPIView):
    queryset = Affective.objects.all()
    serializer_class = AffectiveSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
class AffectiveDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Affective.objects.all()
    serializer_class = AffectiveSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
# List all student affective traits based on term, class, session
class GetStudentAffectiveTraits(generics.ListAPIView):
    serializer_class = StudentaffectiveSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        userid = self.kwargs.get('userid')
        _class = self.kwargs.get('classroom')
        _term = self.kwargs.get('term')
        _session = self.kwargs.get('session')
        
        classObj = SchoolClass.objects.get(pk=_class)
        termObj = Term.objects.get(pk=_term)
        sessionObj = Session.objects.get(pk=_session)
        user = User.objects.get(pk=userid)
        
        
        # Example: Fetching data based on a filter field named 'filter_field'
        queryset = Studentaffective.objects.filter(studentclass=classObj,session=sessionObj,term=termObj,student=user)
        
        if not queryset:
            raise ValidationError("No records matching your criteria")
        return queryset
    

# List all student affective traits based on term, class, session
class GetStudentPsychoTraits(generics.ListAPIView):
    serializer_class = StudentpsychomotorSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        userid = self.kwargs.get('userid')
        _class = self.kwargs.get('classroom')
        _term = self.kwargs.get('term')
        _session = self.kwargs.get('session')
        
        classObj = SchoolClass.objects.get(pk=_class)
        termObj = Term.objects.get(pk=_term)
        sessionObj = Session.objects.get(pk=_session)
        user = User.objects.get(pk=userid)
        
        
        # Example: Fetching data based on a filter field named 'filter_field'
        queryset = Studentpsychomotor.objects.filter(studentclass=classObj,session=sessionObj,term=termObj,student=user)
        
        if not queryset:
            raise ValidationError("No records matching your criteria")
        return queryset
    
    


# Enroll student in class room
class EnrollStudent(generics.CreateAPIView):
    serializer_class = ClassroomSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Classroom.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        
        with transaction.atomic():
            
            try:
                activeTerm = Term.objects.get(status='True')
                activeSession = Session.objects.get(status='True')
                # Access form values from the request object
                _class = request.data.get('studentclass')
                admission_number = request.data.get('admission_number')
                student = StudentProfile.objects.get(admission_number=admission_number)
                classObj = SchoolClass.objects.get(pk=_class)
                
                
                # check if student is already enrolled
                studentEnrolled = Classroom.objects.filter(Q(term=activeTerm) & Q(session=activeSession) & Q (class_room=classObj.pk) & Q(student=student.user.pk))
                
                if studentEnrolled:
                    raise ValidationError("You are already enrolled")
                
                enrollObj = Classroom.objects.create(
                        class_room=classObj,
                        session = activeSession,
                        term = activeTerm,
                        student = student.user
                        )
                enrollObj.save()
  
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Enrollment created successfully'},
                status = status.HTTP_201_CREATED
                )
        
# List all student in classroom based on term, class, session
class RollCall(generics.ListAPIView):
    serializer_class = ClassroomSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
        _class = self.request.data.get('classroom')
        _term = self.request.data.get('term')
        _session = self.request.data.get('session')
        
        classObj = SchoolClass.objects.get(pk=_class)
        termObj = Term.objects.get(pk=_term)
        sessionObj = Session.objects.get(pk=_session)
        
        queryset = Classroom.objects.filter(class_room=classObj,session=sessionObj,term=termObj)
        
        if not queryset:
            raise ValidationError("No records matching your criteria")
        return queryset


# Detail Classroom
class ClassroomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]