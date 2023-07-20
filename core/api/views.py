import random
import string
import math
import json
from io import BytesIO

import pandas as pd
from users.serializers import *
from core.api.serializers import *
# from profiles.api.serializers import *
from core.api.permissions import *
# from core.api.utilities import *
from django.http import HttpResponse,JsonResponse

import csv

# # import models
from core.models import *
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, Avg, Max, Min
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
from openpyxl import Workbook
from rest_framework.renderers import JSONRenderer
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
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
    
    

class StudentProfileListAPIView(generics.ListAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
# create student profile using user id
class StudentProfileCreate(generics.CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
    def get_queryset(self):
        # just return the subjectteacher object
        return StudentProfile.objects.all()
     
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        
        # get movie
        user= User.objects.get(pk=pk)
        
        guardian = serializer.validated_data['guardian']
        local_govt = serializer.validated_data['local_govt']
        address = serializer.validated_data['address']
        session_admitted = serializer.validated_data['session_admitted']
        term_admitted = serializer.validated_data['term_admitted']
        class_admitted = serializer.validated_data['class_admitted']
        
        
        serializer.save(user=user)

    
class StudentProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

# class TeacherProfileCreateAPIView(generics.ListCreateAPIView):
#     # ListCreateAPIView gives us both the get and post methods
#     queryset = TeacherProfile.objects.all()
#     serializer_class = TeacherProfileSerializer
#     # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]

class TeacherProfileCreateAPIView(generics.CreateAPIView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    
    def get_queryset(self):
        # just return the subjectteacher object
        return TeacherProfile.objects.all()
     
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        
        # get movie
        user= User.objects.get(pk=pk)
        
        qualification = serializer.validated_data['qualification']
        local_govt = serializer.validated_data['local_govt']
        address = serializer.validated_data['address']
        
        serializer.save(user=user)
    
class TeacherProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
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
        
        # get user
        user= User.objects.get(pk=pk)
        
        term = serializer.validated_data['term']
        studentclass = serializer.validated_data['studentclass']
        session = serializer.validated_data['session']
        subject = serializer.validated_data['subject']
        firstscore = serializer.validated_data['firstscore']
        secondscore = serializer.validated_data['secondscore']
        thirdscore = serializer.validated_data['thirdscore']
        examscore = serializer.validated_data['examscore']
        
        totalca = 0
        subjecttotal =0
        
        if math.isnan(firstscore):
            firstscore = 0
        else:
            firstscore = firstscore
        
        if math.isnan(secondscore):
            secondscore = 0
        else:
            secondscore = secondscore
        
        if math.isnan(thirdscore):
            firstscore = 0
        else:
            thirdscore = thirdscore
        
        if math.isnan(examscore):
            examscore = 0
        else:
            examscore = examscore
        
        totalca = firstscore + secondscore + thirdscore
        subjecttotal = totalca + examscore
        
        teacher = self.request.user
        
        _isteacher = SubjectTeacher.objects.filter(teacher_id=teacher.pk,classroom=studentclass.pk,session=session.pk,subject=subject.pk)
        if not _isteacher:
            raise ValidationError("You are not a subject teacher for this class")
            
        
        # logic to prevent multple creation of record
        _queryset = Scores.objects.filter(user=user,term=term,studentclass=studentclass,session=session,subject=subject)
        
        if _queryset.exists():
            
            raise ValidationError("Record already exist")
        
        serializer.save(user=user,subjectteacher=SubjectTeacher.objects.get(teacher=teacher),firstscore=firstscore,secondscore=secondscore,thirdscore=thirdscore,totalca=totalca,subjecttotal=subjecttotal)
        processScores(subject,studentclass,term,session)
        
        
# get scores based on subject, term, session and class
class FindScoresAPIView(APIView):
    def get(self, request):
        payload = request.query_params
        
        subjObj = Subject.objects.get(pk=payload.get('subject'))
        classObj = SchoolClass.objects.get(pk=payload.get('studentclass'))
        termObj = Term.objects.get(pk=payload.get('term'))
        sessionObj = Session.objects.get(pk=payload.get('session'))

        # Example usage: filtering queryset based on payload parameters
        queryset = Scores.objects.filter(subject=subjObj,studentclass=classObj,session=sessionObj,term=termObj)
        if not queryset:
            raise ValidationError("No records matching your criteria")
        
        # Serialize the data and return the response
        serializer = ScoresSerializer(queryset, many=True)
        return Response(serializer.data)
        

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
                
                # _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                # if not _isteacher:
                #     raise ValidationError("You are not a class teacher for this class")
                
                
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
# class ExportSheet(APIView):
#     # serializer_class = ClassroomSerializer
#     # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
#     renderer_classes = [XLSXRenderer, JSONRenderer]
    
#     def get(self,request):
#         try:
#             payload = request.query_params
            
#             activeTerm = Term.objects.get(status='True')
#             activeSession = Session.objects.get(status='True')
            
#             classObj = SchoolClass.objects.get(pk=payload.get('classroom'))
#             subjObj = Subject.objects.get(pk=payload.get('subject'))

            
#             teacher = self.request.user
        
#             # _isteacher = SubjectTeacher.objects.filter(teacher_id=teacher.pk,classroom=classObj.pk,session=activeSession.pk,subject=subjObj.pk)
#             # if not _isteacher:
#             #     raise ValidationError("You are not a subject teacher for this class")

#             response = Response(content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename=CA_SHEET_'+subjObj.name+'_'+classObj.class_name+'_'+activeTerm.name+'_'+activeSession.name+'.csv'
#             writer = csv.writer(response)
            
#             writer.writerow(['StudentID','Name','Class','Subject','FirstCA','SecondCA','ThirdCA','Exam'])
            
#             rollcall = Classroom.objects.filter(Q(session=activeSession) & Q(class_room=classObj) & Q(term=activeTerm)).order_by('student__sur_name')
#             # subject = Subject.objects.get(pk=subject)
            
#             for item in rollcall:
#                 writer.writerow([item.student.pk,item.student.sur_name + "  " + item.student.first_name,classObj.class_name,subjObj.subject_code,0,0,0,0])

#             return response
    
#         except Exception as e:
            
#             raise ValidationError("Unable to download the sheet")

# export sheet 
class ExportSheet(APIView):
    # 1 this works Adopt this one
    def get(self, request):
        
        payload = request.query_params
        
        classname = payload.get('classname')
        subjname = payload.get('subjname')
        classid = payload.get('classid')
        subjectid = payload.get('subjectid')
        
        classObj = SchoolClass.objects.get(pk=classid)    
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')
        
        rollcall = Classroom.objects.filter(Q(session=activeSession) & Q(class_room=classObj) & Q(term=activeTerm)).order_by('student__sur_name')

        # Create an in-memory Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active

        # Write headers to the worksheet
        headers = ['STDID', 'NAME', 'CLASS','CLASSID','SUBJNAME','SUBJID','TRM','SESS','CA1','CA2','CA3','EXAM']
        ws.append(headers)

        # Write data to the worksheet
        for item in rollcall:
            row = [item.student.id,item.student.sur_name +' '+ item.student.first_name, classname,classid,subjname, subjectid, activeTerm.name,activeSession.name,0,0,0,0]
            ws.append(row)

        # Create a response object with the appropriate content type and headers
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=your_data.xlsx'

        # Save the workbook to the response
        wb.save(response)

        return response
    
    
    # 2 works as well 
    # def get(self, request):
        
    #     custom_header = ['Product1', 'Price2','Product3', 'Price4','Product5', 'Price6','Product7', 'Price8']
    #     userObj = Classroom.objects.all()
    #     serializer = ClassroomSerializer(userObj, many=True)
    #     df = pd.DataFrame(serializer.data)
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename="out.xlsx"'
    #     df.to_excel(response, na_rep='N/A', header=custom_header, index=False)

    #     return response
 

# upload/import CA EXCEL SHEET
class ImportAssessment(generics.CreateAPIView):
    serializer_class = ScoresSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Scores.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        with transaction.atomic():
              
            try:
                 if 'file' not in request.FILES:
                    
                     raise ValidationError({"msg":"no file chosen"})
                 else:
                    data = request.FILES['file']
                   
                    reader = pd.read_excel(data)
                    reader = reader.where(pd.notnull(reader), None)
                    dtframe = reader
                  
                
                    for dtframe in dtframe.itertuples():
                        studentObj=User.objects.get(pk=int(dtframe.STDID))
                        classObj = SchoolClass.objects.get(pk=int(dtframe.CLASSID)) 
                        subjectObj = Subject.objects.get(pk=int(dtframe.SUBJID))   
                        activeTerm = Term.objects.get(status='True')
                        activeSession = Session.objects.get(status='True')
                     
                    
                        # check for subject teacher
                        teacher = self.request.user
                     
                       
        
                        _isteacher = SubjectTeacher.objects.filter(teacher_id=teacher.pk,classroom=int(dtframe.CLASSID),session=activeSession.pk,subject=dtframe.SUBJID)
                        
                        if not _isteacher:
                            raise ValidationError("You are not a subject teacher for this class")
                        else:
                            # check if studentexist in class
                            isEnrolled = Classroom.objects.filter(session=activeSession,term=activeTerm,class_room = classObj,student=int(dtframe.STDID)).exists()
                            if  not isEnrolled:
                                pass
                            else:
                                # check for existence of scores
                                scoresExist = Scores.objects.filter(session=activeSession,term=activeTerm,subject=int(dtframe.SUBJID),studentclass=int(dtframe.CLASSID),user=int(dtframe.STDID)).exists()
                    
                                if scoresExist:
                                    pass
                                else:
                                    
                                    ca1 = 0
                                    ca2 = 0
                                    ca3 = 0
                                    exam = 0
                    
                                    if not math.isnan(dtframe.CA1):
                                        ca1 = dtframe.CA1
                                    elif not math.isnan(dtframe.CA2):
                                        ca2 = dtframe.CA2
                                    elif not math.isnan(dtframe.CA3):
                                        ca3 = dtframe.CA3
                                    elif not math.isnan(dtframe.EXAM):
                                        exam = dtframe.EXAM
                        
                                    obj = Scores.objects.create(
                                            firstscore=ca1,
                                            secondscore=ca2,
                                            thirdscore=ca3,
                                            totalca=ca1 + ca2 + ca3,
                                            examscore=exam,
                                            subjecttotal=exam + ca1 + ca2 + ca3,
                                            session=activeSession,
                                            term=activeTerm,
                                            user=studentObj,
                                            studentclass=classObj,
                                            subjectteacher= SubjectTeacher.objects.get(teacher=teacher.pk),
                                            subject=subjectObj,
                                        )
                                        
                                    obj.save()
                    
                                    # process scores
                    processScores(subjectObj,classObj,activeTerm,activeSession)
                  
            except Exception as e:
                
                raise ValidationError(e)
           
        return Response(
                {'msg':'Assessment created successfully'},
                status = status.HTTP_201_CREATED
                )
        

# List all result based on term, class, session
class GetResult(generics.ListAPIView):
    serializer_class = ResultSerializer
    # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # _class = self.request.data.get('classroom')
        # _session = self.request.data.get('session')
        # _term = self.request.data.get('term')
        payload = self.request.query_params
        
        classObj = SchoolClass.objects.get(pk=payload.get('classroom'))
        termObj = Term.objects.get(pk=payload.get('term'))
        sessionObj = Session.objects.get(pk=payload.get('session'))
        
        # Example: Fetching data based on a filter field named 'filter_field'
        queryset = Result.objects.filter(studentclass=classObj,session=sessionObj,term=termObj)
        
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
                
                # _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                # if not _isteacher:
                #     raise ValidationError("You are not a class teacher for this class")
                
                
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
                
                # _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                # if not _isteacher:
                #     raise ValidationError("You are not a class teacher for this class")

                # process Psychomotor domain
                processPsycho(classObj,sessionObj,termObj)

                    
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Student psycho traits created successfully'},
                status = status.HTTP_201_CREATED
                )
        
        
        
class AddAutoComents(generics.CreateAPIView):
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
                
                # _isteacher = ClassTeacher.objects.filter(tutor=loggedInUser,classroom=classObj,session=sessionObj,term=termObj)
                
                # if not _isteacher:
                #     raise ValidationError("You are not a class teacher for this class")
                
                scores = Scores.objects.filter(session=sessionObj,term=termObj,studentclass=classObj).exists()

                if not scores:
                    raise ValidationError("You are not a class teacher for this class")
                    # Add auto comment
                autoAddComment(classObj,sessionObj,termObj)

            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'comments created successfully'},
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
                _class = request.data.get('class_room')
                admission_number = request.data.get('student')
            
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
        
# # List all student in classroom based on term, class, session
# class RollCall(generics.ListAPIView):
#     serializer_class = ClassroomSerializer
#     # permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
#     def get_queryset(self):
        
#         _class = self.request.data.get('classroom')
#         _term = self.request.data.get('term')
#         _session = self.request.data.get('session')
#         # classObj = SchoolClass.objects.get(pk=_class)
#         termObj = Term.objects.get(pk=_term)
#         sessionObj = Session.objects.get(pk=_session)
        
#         queryset = Classroom.objects.filter(session=sessionObj,term=termObj)
        
#         if not queryset:
#             raise ValidationError("No records matching your criteria")
#         return queryset
    
class RollCallAPIView(APIView):
    def get(self, request):
        payload = request.query_params
        # Access the query parameters
        # Use payload to filter and retrieve the desired records
        classObj = SchoolClass.objects.get(pk=payload.get('classroom'))
        termObj = Term.objects.get(pk=payload.get('term'))
        sessionObj = Session.objects.get(pk=payload.get('session'))

        # Example usage: filtering queryset based on payload parameters
        queryset = Classroom.objects.filter(class_room=classObj,session=sessionObj,term=termObj)
        if not queryset:
            raise ValidationError("No records matching your criteria")
        
        # Serialize the data and return the response
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(serializer.data)

# roll call for assessment sheet
class AssessmentSheetRollCallAPIView(APIView):
    def get(self, request):
        payload = request.query_params
        # Access the query parametersF
        # Use payload to filter and retrieve the desired records
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')
        classObj = SchoolClass.objects.get(pk=payload.get('classroom'))

        # Example usage: filtering queryset based on payload parameters
        queryset = Classroom.objects.filter(class_room=classObj,session=activeSession,term=activeTerm)
        if not queryset:
            raise ValidationError("No records matching your criteria")
        
        # Serialize the data and return the response
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(serializer.data)
    
# Detail Classroom
class ClassroomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    # permission_classes =[IsAuthenticated & IsAuthOrReadOnly]