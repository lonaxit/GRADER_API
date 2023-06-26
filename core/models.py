# from django.db import models

# # from django.contrib.auth import get_user_model
# # User = get_user_model()

# class Student(models.Model):
#     # user = models.OneToOneField(User,on_delete=models.CASCADE)
#     guradian = models.CharField(max_length=200,null=True,blank=True)
#     local_govt = models.CharField(max_length=200,null=True,blank=True)
#     address = models.CharField(max_length=200,null=True,blank=True)

    
    
# class Teacher(models.Model):
#     # user = models.OneToOneField(User,on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
   

# class Course(models.Model):
#     course_name = models.CharField(max_length=100)
#     course_code = models.CharField(max_length=20, unique=True)


# class AcademicSession(models.Model):
#     _name = models.CharField(max_length=100)
#     _code = models.CharField(max_length=20, unique=True)
    
# class Term(models.Model):
#     _name = models.CharField(max_length=100)
#     _code = models.CharField(max_length=20, unique=True)
    
# class Classroom(models.Model):
#     name = models.CharField(max_length=100)
#     class_code = models.CharField(max_length=20, unique=True)

# class ClassTeacher(models.Model):
#     # student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     score = models.FloatField()
#     date = models.DateField(auto_now_add=True)
    
# class Grade(models.Model):
#     # student = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     score = models.FloatField()
#     date = models.DateField(auto_now_add=True)
