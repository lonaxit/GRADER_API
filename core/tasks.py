from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.contrib.auth import get_user_model
from core.models import Session
from django.db import transaction
User = get_user_model()
from rest_framework.exceptions import ValidationError
import math
import io, csv, pandas as pd
import json
import datetime
from core.api.utilities import *

# from midas.celery import app

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task
def mul(x, y):
    print( x * y)   
    

# @app.task
@shared_task
def migrate_academic_session(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():

                # _date_stamp=row.entry_date
                # _date_timestamp_ms = int(_date_stamp) / 1000
                # _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                Session.objects.create(
                    name = row.session,
                    code = row.code
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")

@shared_task
def migrate_school_class(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():

                # _date_stamp=row.entry_date
                # _date_timestamp_ms = int(_date_stamp) / 1000
                # _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                SchoolClass.objects.create(
                    class_name = row.class_name,
                    code = row.code
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")  



# 
@shared_task
def migrate_subjectsperclass(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():

                SubjectPerClass.objects.create(
                    sch_class = SchoolClass.objects.get(pk=row.class_id),
                    term = Term.objects.get(pk=row.term),
                    session = Session.objects.get(pk=row.session),
                    no_subject = row.no_subject
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")  
        

@shared_task
def migrate_subjects(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                
                Subject.objects.create(
                    name = row.name,
                    subject_code = row.subject_code
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")  


@shared_task
def migrate_users_task(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                _date_stamp=row.dob
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                userObj = User.objects.create(
                        username = row.student_username,
                        first_name = row.first_name,
                        sur_name =  row.sur_name,
                        other_name =  row.other_name,
                        gender = row.sex,
                        phone = row.user_id,
                        dob = _date,
                        is_staff = True,
                        is_student = False,
                                    )
                userObj.set_password(str(row.student_username))
                userObj.save()
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}") 
        
        
@shared_task
def migrate_subject_teachers(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                # _date_stamp=row.dob
                # _date_timestamp_ms = int(_date_stamp) / 1000
                # _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                # sub = row.subject_id
                # classid = row.classroom_id
                # sess = row.session_id
                # teacherid= row.NEW_USER_ID
                
                
                SubjectTeacher.objects.create(
                    subject = Subject.objects.get(pk=row.subject_id),
                    classroom = SchoolClass.objects.get(pk=row.classroom_id),
                    session = Session.objects.get(pk=row.session_id),
                    teacher =User.objects.get(pk=row.NEW_USER_ID),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}") 

# class teacher
@shared_task
def migrate_class_teachers(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                # _date_stamp=row.dob
                # _date_timestamp_ms = int(_date_stamp) / 1000
                # _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                # sub = row.subject_id
                # classid = row.classroom_id
                # sess = row.session_id
                # teacherid= row.NEW_USER_ID
                
                
                ClassTeacher.objects.create(
                    term = Term.objects.get(pk=row.term_id),
                    classroom = SchoolClass.objects.get(pk=row.classroom_id),
                    session = Session.objects.get(pk=row.session_id),
                    tutor =User.objects.get(pk=row.NEW_ID),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}") 

# scores

@shared_task
def migrate_scores(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                # _date_stamp=row.dob
                # _date_timestamp_ms = int(_date_stamp) / 1000
                # _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                # sub = row.subject_id
                # classid = row.classroom_id
                # sess = row.session_id
                # teacherid= row.NEW_USER_ID
                
                Scores.objects.create(
                    user =User.objects.get(pk=row.NEW_STD_ID),
                    term = Term.objects.get(pk=row.term_id),
                    session = Session.objects.get(pk=row.session_id),
                    studentclass = SchoolClass.objects.get(pk=row.studentclass_id),
                    subject = Subject.objects.get(pk=row.subject_id),
                    subjectteacher = SubjectTeacher.objects.get(pk=row.NEW_TEACHER_ID),
                    
                    firstscore =row.firstscore,
                    secondscore = row.secondscore,
                    thirdscore =row.thirdscore,
                    totalca = row.totalca,
                    subjaverage = row.subjaverage,
                    examscore = row.examscore,
                    subjectposition = row.subjectposition,
                    subjecttotal = row.subjecttotal,
                   
                    subjectgrade = row.subjectgrade,
                    subjectrating = row.subjectrating,
                    highest_inclass = row.highest_inclass,
                    lowest_inclass = row.lowest_inclass,
                    
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}") 



@shared_task
def migrate_result(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
               
                
                Result.objects.create(
                    student =User.objects.get(pk=row.NEW_STD_USERID),
                    term = Term.objects.get(pk=row.term_id),
                    session = Session.objects.get(pk=row.session_id),
                    studentclass = SchoolClass.objects.get(pk=row.studentclass_id),
                  
                    classteacher = ClassTeacher.objects.get(pk=row.classteacher_id),
                    
                    termtotal =row.termtotal,
                    termaverage = row.termaverage,
                    termposition =row.termposition,
                    classteachercomment = row.classteachercomment,
                    headteachercomment = row.headteachercomment,
                    attendance = row.attendance,
                    
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}") 


# enrollment
@shared_task
def migrate_enrollment(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
               
                
                Classroom.objects.create(
                    student =User.objects.get(pk=row.NEW_USER_ID),
                    term = Term.objects.get(pk=row.term_id),
                    session = Session.objects.get(pk=row.session_id),
                    class_room = SchoolClass.objects.get(pk=row.class_room_id),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")
        
        
# admission number
@shared_task
def migrate_admissionnumber(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
               
                
                AdmissionNumber.objects.create(
                    serial_no =row.serial_no,
                    status = row.status,
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")


# students affective
@shared_task
def migrate_studentaffective(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
               
                
                Studentaffective.objects.create(
                    student =User.objects.get(pk=row.NEW_USERID),
                    term = Term.objects.get(pk=row.term_id),
                    session = Session.objects.get(pk=row.session_id),
                    studentclass = SchoolClass.objects.get(pk=row.studentclass_id),
                    affective = Affective.objects.get(pk=row.affective_id),
                    rating = Rating.objects.get(pk=row.rating_id),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")


# students psychomotor
@shared_task
def migrate_studentpsychomotor(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
               
                
                Studentpsychomotor.objects.create(
                    student =User.objects.get(pk=row.NEW_USERID),
                    term = Term.objects.get(pk=row.term_id),
                    session = Session.objects.get(pk=row.session_id),
                    studentclass = SchoolClass.objects.get(pk=row.studentclass_id),
                    psychomotor = Psychomotor.objects.get(pk=row.psychomotor_id),
                    rating = Rating.objects.get(pk=row.rating_id),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")
        


# upload student profile
@shared_task
def migrate_student_profile(data):
  
    data_frame = pd.read_json(data)
 
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
               
                
                StudentProfile.objects.create(
                    user =User.objects.get(pk=row.NEW_USERID),
                    term = Term.objects.get(pk=row.term_id),
                    session = Session.objects.get(pk=row.session_id),
                    studentclass = SchoolClass.objects.get(pk=row.studentclass_id),
                    psychomotor = Psychomotor.objects.get(pk=row.psychomotor_id),
                    rating = Rating.objects.get(pk=row.rating_id),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")



# @shared_task
# def createLoanDeductions(userid):
#     # get all active master deduction records
#         masterDeductions= MasterLoanDeduction.objects.filter(active=True)
        
#         if masterDeductions.exists():
           
#             for master in masterDeductions:
                
#                 try:
#                     # total cumulative deduction for a particular ippis number
#                     ippis_Deduction = master.cumulative_amount
                    
#                     user_ = User.objects.filter(id=master.ippis_number)
#                     countUser = user_.count()
#                     if countUser > 1 or countUser == 0:
#                         continue
#                     else:
                    
#                         # get the user profile based on that IPPIS Number
#                         profile = User.objects.get(id=master.ippis_number)
                        
#                         # get all active loans for a user
#                         myLoans = Loan.objects.filter(active=True, owner=profile).order_by('tenor')
                        
                        
#                         #total Monthly Deduction for all user loans
#                         total_MonthlyDedcution = myLoans.aggregate(totalMonthlyDeduction=Sum('monthly_deduction'))
                        
#                         userTotalMonthlyDeduction = total_MonthlyDedcution['totalMonthlyDeduction']
                        
#                         # greater than
#                         if ippis_Deduction > userTotalMonthlyDeduction:
#                             # distribute the loans equally but pay the remaining balance on the last loan
#                             for index, loanItem in enumerate(myLoans):
                                
#                                 # check for last loan
#                                 if index == myLoans.count() - 1:
                                    
#                                     # pay what ever that is remaining on the last loan
#                                     Deduction.objects.create(  
#                                         loanee=profile,
#                                         loan= loanItem,
#                                         credit = ippis_Deduction,
#                                         narration = master.narration,
#                                         transaction_date = master.entry_date,
#                                         transaction_code = master.transaction_code,
#                                         created_by=User.objects.get(id=userid),
#                                         )
                                
#                                     deactivateLoan(loanItem)
#                                 else:
#                                     loanDeductions = Deduction.objects.filter(loan=loanItem)
                                
#                                     # # get principal loan amount
#                                     loanPrincipal  = loanItem.approved_amount
#                                     total_credit = loanDeductions.aggregate(credit=Sum('credit'))['credit'] or 0
#                                     total_debit = loanDeductions.aggregate(debit=Sum('debit'))['debit'] or 0
                                    
#                                     payments = total_credit - total_debit
#                                     bal = loanPrincipal-payments
                                    
#                                     if bal <= loanItem.monthly_deduction:
                                        
#                                         ippis_Deduction = ippis_Deduction-bal
#                                         Deduction.objects.create(  
#                                         loanee=profile,
#                                         loan= loanItem,
#                                         credit = bal,
#                                         narration = master.narration,
#                                         transaction_date = master.entry_date,
#                                         transaction_code = master.transaction_code,
#                                         created_by=User.objects.get(id=userid),
#                                         )
#                                         deactivateLoan(loanItem)
                                        
#                                     elif bal > loanItem.monthly_deduction:
#                                         ippis_Deduction = ippis_Deduction-loanItem.monthly_deduction
#                                         Deduction.objects.create(  
#                                         loanee=profile,
#                                         loan= loanItem,
#                                         credit = loanItem.monthly_deduction,
#                                         narration = master.narration,
#                                         transaction_date = master.entry_date,
#                                         transaction_code = master.transaction_code,
#                                         created_by=User.objects.get(id=userid),
#                                         )
#                                         deactivateLoan(loanItem)
                                    
#                         elif ippis_Deduction == userTotalMonthlyDeduction:
                            
#                             for index, loanItem in enumerate(myLoans):
#                                 Deduction.objects.create(  
#                                         loanee=profile,
#                                         loan= loanItem,
#                                         credit = loanItem.monthly_deduction,
#                                         narration = master.narration,
#                                         transaction_date = master.entry_date,
#                                         transaction_code = master.transaction_code,
#                                         created_by=User.objects.get(id=userid),
#                                         )
#                                 deactivateLoan(loanItem)
                                
#                         elif ippis_Deduction < userTotalMonthlyDeduction:
                    
#                             for index, loanItem in enumerate(myLoans):
#                                 if index == myLoans.count() - 1:
                                    
#                                     # pay what ever that is remaining on the last loan
#                                     Deduction.objects.create(  
#                                         loanee=profile,
#                                         loan= loanItem,
#                                         credit = ippis_Deduction,
#                                         narration = master.narration,
#                                         transaction_date = master.entry_date,
#                                         transaction_code = master.transaction_code,
#                                         created_by=User.objects.get(id=userid),
#                                         )
                                
#                                     deactivateLoan(loanItem)
#                                 else:
                                
#                                     if ippis_Deduction > loanItem.monthly_deduction:
                                        
#                                         ippis_Deduction = ippis_Deduction-loanItem.monthly_deduction
#                                         Deduction.objects.create(  
#                                             loanee=profile,
#                                             loan= loanItem,
#                                             credit = loanItem.monthly_deduction,
#                                             narration = master.narration,
#                                             transaction_date = master.entry_date,
#                                             transaction_code = master.transaction_code,
#                                             created_by=User.objects.get(id=userid),
#                                             )
#                                         deactivateLoan(loanItem)
#                                     elif ippis_Deduction <= loanItem.monthly_deduction:
#                                         ippis_Deduction = ippis_Deduction-ippis_Deduction
#                                         Deduction.objects.create(  
#                                             loanee=profile,
#                                             loan= loanItem,
#                                             credit = ippis_Deduction,
#                                             narration = master.narration,
#                                             transaction_date = master.entry_date,
#                                             transaction_code = master.transaction_code,
#                                             created_by=User.objects.get(id=userid),
#                                             )
#                                         deactivateLoan(loanItem)
                                
#                     # update the master record to inactive
#                     master.active = False
#                     master.save()
                            
#                 except Profile.DoesNotExist:
#                     continue
                
#             return Response(
#                 {'msg':'Loan deductions created successfully'},
#                 status = status.HTTP_201_CREATED
#                 )
#         else:
#             raise ValidationError('No unprocessed deductions yet!')
                            
    
   
# # update loan deduction swith correct loan ids
# @shared_task
# def update_loan_deduction_loanids():
#     """
#     Update the 'loan' field of all deductions based on the related loan subscription ID.

#     This function loops through all loans, filters deductions based on their
#     subscription ID, and updates their 'loan' field to match the corresponding
#     loan's ID.
#     """
#     loans = Loan.objects.all()

#     with transaction.atomic():
#         for loan in loans:
#             deductions = Deduction.objects.filter(deduction_sub_id=loan.sub_id)

#             if deductions.exists():
#                 deductions.update(loan=loan.id)
#             else:
#                 # If there are no deductions for this loan, do nothing
#                 pass
            
# # upload user savings   
# @shared_task
# def upload_user_savings(request,data):

#     # convert the JSON data to a DataFrame
#     data_frame = pd.read_json(data)
    
#     with transaction.atomic():
#         try:
#             for row in data_frame.itertuples():
#                 credit_amt = None
#                 debit_amt = None
                
#                 if pd.isnull(row.amount_saved):
#                     # Do something if the cell is empty
#                     pass
#                 else:
#                     credit_amt = row.amount_saved
                    
#                 if pd.isnull(row.amount_withdrawn):
#                     # Do something if the cell is empty
#                     pass
#                 else:
#                     debit_amt = row.amount_withdrawn

#                 _date_stamp=row.entry_date
#                 _date_timestamp_ms = int(_date_stamp) / 1000
#                 _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
#                 Saving.objects.create(
#                     user=User.objects.get(pk=row.user_id),
#                     credit = credit_amt,
#                     debit = debit_amt,
#                     transaction_code=row.ref_string.replace('-', ''), 
#                     transaction_date=_date,
#                     narration = row.notes,
#                     created_by=request.user,
#                 )
                    
#         except ValueError as e:
#             raise ValueError(f"Invalid value: {e}")
#         except TypeError as e:
#             raise TypeError(f"Type error: {e}")


# @shared_task
# def update_profile(data):
#     """
#     Update the 'profile' field of all users based on the related user ID.

#     This function loops through all profiles, filters prodile based on their
#     user ID, and updates relevant fields.
#     """
#     data_frame = pd.read_json(data)
    
#     # profiles = Profile.objects.all()
#     with transaction.atomic():
#         for  row in data_frame.itertuples():
            
#             try:
#                 # Attempt to get the order for the user
#                 profile= Profile.objects.get(user_id=row.id)
               
#                 # If the order exists, update it with the user's ID
#                 profile.staff_id = row.staff_no
#                 profile.home_address = row.home_add
#                 profile.email = row.email
#                 profile.employment_type = row.employ_type
#                 profile.gender = row.sex
#                 profile.job_cadre = row.job_cadre
#                 profile.marital_status = row.marital_status
#                 profile.phone = row.phone
#                 profile.dept = row.dept
#                 profile.title = row.title
#                 profile.member_type = row.membership_type
#                 profile.save()
#             except Profile.DoesNotExist:
#                 pass
             

             
# @shared_task
# def update_nok(data):
#     """
#     Update the 'profile'  next of kin details.

    
#     """
#     data_frame = pd.read_json(data)
    
#     # profiles = Profile.objects.all()
#     with transaction.atomic():
#         for  row in data_frame.itertuples():
#             surname = row.first_name
#             firstname = row.last_name
#             othername = row.other_name
            
#             full_name = surname + ' ' + firstname + ' ' + othername
            
#             try:
#                 # Attempt to get the order for the user
#                 profile= Profile.objects.get(user_id=row.user_id)
#                 #update profile
#                 profile.nok_fullName = full_name
#                 profile.nok_relationship = row.relationship
#                 profile.nok_phone = row.phone
#                 profile.save()
#             except Profile.DoesNotExist:
#                 pass
            
# @shared_task
# def update_bank(data):
#     """
#     Update the 'profile'  next of kin details.

    
#     """
#     data_frame = pd.read_json(data)
    
#     # profiles = Profile.objects.all()
#     with transaction.atomic():
#         for  row in data_frame.itertuples():
          
            
#             try:
#                 # Attempt to get the order for the user
#                 profile= Profile.objects.get(user_id=row.user_id)
#                 #update profile
#                 profile.bank = row.bank_name
#                 profile.bank_account = row.acct_number
#                 profile.save()
#             except Profile.DoesNotExist:
#                 pass
            
# @shared_task
# def upload_master_loan_deduction(userid,data):

#     # convert the JSON data to a DataFrame
#     data_frame = pd.read_json(data)
    
#     with transaction.atomic():
#         try:
#             for row in data_frame.itertuples():
            
#                 _date_stamp=row.entry_date
#                 _date_timestamp_ms = int(_date_stamp) / 1000
#                 _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
#                 MasterLoanDeduction.objects.create(
#                     name=row.name,
#                     ippis_number=row.ippis_no,
#                     cumulative_amount = row.cumulative_amount,
#                     narration = row.description,
#                     transaction_code=row.master_reference.replace('-', ''),
#                     active = row.status, 
#                     entry_date=_date,
#                     created_by=User.objects.get(pk=userid),
#                 )
                    
#         except ValueError as e:
#             raise ValueError(f"Invalid value: {e}")
#         except TypeError as e:
#             raise TypeError(f"Type error: {e}")
        
        
# # upload master savings 
# @shared_task
# def upload_master_saving(userid,data):

#     # convert the JSON data to a DataFrame
#     data_frame = pd.read_json(data)
#     with transaction.atomic():
        
#         try:
#             for row in data_frame.itertuples():
            
#                 _date_stamp=row.entry_date
#                 _date_timestamp_ms = int(_date_stamp) / 1000
#                 _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
#                 SavingMaster.objects.create(
#                     name=row.name,
#                     ippis_number=row.ippis_no,
#                     amount = row.saving_cumulative,
#                     narration = row.notes,
#                     transaction_code=row.ref_identification.replace('-', ''),
#                     active = row.status, 
#                     transaction_date=_date,
#                     uploaded_by=User.objects.get(pk=userid),
#                 )
                    
#         except ValueError as e:
#             raise ValueError(f"Invalid value: {e}")
#         except TypeError as e:
#             raise TypeError(f"Type error: {e}")