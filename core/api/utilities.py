
import random
import string

import io, csv, pandas as pd
from core.api.serializers import *
from core.api.permissions import *
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


def processTerminalResult(request,classObj,termObj,sessionObj):
    
    # find distint students in the scores table
    students = Scores.objects.filter(session=sessionObj,term=termObj,studentclass=classObj).distinct('user')
    
    
    
    # filter scores based on session, term and class
    scoresList = Scores.objects.filter(studentclass=classObj,term=termObj,session=sessionObj)
    
    # # filter result based on session,class and term
    result = Result.objects.filter(studentclass=classObj, term=termObj,session=sessionObj)
    
    
    for student in students:
        scores = scoresList.filter(user=student.user).aggregate(subject_total=Sum('subjecttotal'))
        

        # check for existence of record
        if result.filter(student=student.user).exists():
            # update the record
            result.filter(student=student.user).update(termtotal=scores['subject_total'])
                  
        else:
            
            
            # create a new record
            resultObj = Result.objects.create(
                                 termtotal = scores['subject_total'],
                                 classteacher = ClassTeacher.objects.get(tutor=request.user.pk),
                                 session = sessionObj,
                                 studentclass = classObj,
                                 term = termObj,
                                 student = student.user
                                     )
            resultObj.save()

        # update term average
    # terminalAverage(scoresObj.student,scoresObj.studentclass,scoresObj.term.pk,   scoresObj.session.pk)
    
    # new code 
    terminalAverage(classObj,termObj,sessionObj)

    # update  term position
    terminalPosition(classObj,termObj,sessionObj)
 
 
 
#    
def processPsycho(classroom,session,term):

 
    # list psycho items
    psychoList = Studentpsychomotor.objects.filter(studentclass=classroom.pk,term=term.pk,session=session.pk)
    
    if not psychoList:
        # select Distinct students from result table
        studentsResultList = Result.objects.filter(studentclass=classroom.pk,session=session.pk,term=term.pk).distinct('student')

        # Get class teacher
  
        for student in studentsResultList:
            
            # check for existence of record
            if psychoList.filter(student=student.student.pk).exists():
                pass
            else:
                # select three random random skills
                psycho_skills = Psychomotor.objects.all().order_by("?")[:3]
                # select rating
                rating = Rating.objects.get(pk=1)

            for i in  psycho_skills:
                
                studentPsycho = Studentpsychomotor.objects.create(
                    session = session,
                    studentclass = classroom,
                    term = term,
                    student = student.student,
                    psychomotor = Psychomotor.objects.get(pk=i.pk),
                    rating= rating,
                                     )
                studentPsycho.save()

# 
def processAffective(classroom,session,term):
    
    # list affetive items
    affective = Studentaffective.objects.filter(studentclass=classroom.pk,term=term.pk,session=session.pk)
    
    if not affective:
        
        # select Distinct students from result table
        studentsResultList = Result.objects.filter(studentclass=classroom,session=session,term=term).distinct('student')

    
        for student in studentsResultList:
        
            # check for existence of record
            if affective.filter(student=student.student.pk).exists():
                pass
            else:
                # select three random affective skills
                affective_skills = Affective.objects.all().order_by("?")[:3]
                # select rating
                rating = Rating.objects.get(pk=1)

            for i in affective_skills:

                # create a new record
                studentAffective = Studentaffective.objects.create(
                        session = session,
                        studentclass = classroom,
                        term = term,
                        student = student.student,
                        affective = Affective.objects.get(pk=i.pk),
                        rating= rating,
                        )
                studentAffective.save()

    

def terminalAverage(classroom,term,session):

    resultList = Result.objects.filter(studentclass=classroom,term=term,session=session)
    # get subject per class
    no_subj_per_class = SubjectPerClass.objects.get(sch_class=classroom,term=term,session=session)

    for result in resultList:

    # scores = Scores.objects.filter(student=studentid,studentclass=classroom,term=termObj,session=sessionObj).aggregate(term_sum=Sum('subjecttotal'))

    # term_sum = scores['term_sum']
    

        class_av = result.termtotal/no_subj_per_class.no_subject

        result = resultList.filter(student=result.student.pk).update(termaverage=class_av)

# assign terminal result position
def terminalPosition(classroom,term,session):


    results = Result.objects.filter(studentclass=classroom,term=term,session=session)
    ordered_scores = []
    counter = 1
    repeated_counter = 0

    previous_score = Result.objects.none()
    for result in results.order_by("-termtotal"):
        # repeated_counter = 0
        if counter == 1:
            # this is the first iteration, just assign the first position
            position = counter
             # update the database
            result_entity = Result.objects.get(pk=result.pk)
            result_entity.termposition = position
            result_entity.save()


            # ordered_scores.append({
            # "position": position,
            # "id": score.pk,
            # "subjecttotal": score.subjecttotal
            # })
            previous_score = result
            counter += 1
        else:

            # check for duplicate
            if result.termtotal == previous_score.termtotal:
                # update database
                result_entity = Result.objects.get(pk=result.pk)
                result_entity.termposition = position
                result_entity.save()

                # position = counter
                # ordered_scores.append({
                # "position": position,
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                # position = previous_score.position
                repeated_counter +=1

            else:
                position = counter + repeated_counter
                # update database
                result_entity = Result.objects.get(pk=result.pk)
                result_entity.termposition = position
                result_entity.save()

                # ordered_scores.append({
                # "position": position,
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })

                previous_score = result
                # previous_position = position
                # repeated_counter = position
                counter += 1
