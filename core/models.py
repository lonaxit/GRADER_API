from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Term(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    

class Session(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    
class SchoolClass(models.Model):
    class_name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.class_name
    
# subject model
class Subject(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    subject_code = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


# subject per class
class SubjectPerClass(models.Model):
    sch_class = models.ForeignKey(SchoolClass,on_delete=models.CASCADE)
    term = models.ForeignKey(Term,on_delete=models.CASCADE)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    no_subject = models.IntegerField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.sch_class.class_name


class AttendanceSetting(models.Model):
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    days_open = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
    days_closed = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.days_open
    

class ResumptionSetting(models.Model):
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    current_term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    current_term_ends = models.DateField(null=True,blank=True)
    next_term_begins = models.DateField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.current_term

class StudentProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='studentprofile')
    guardian = models.CharField(max_length=200,null=True,blank=True)
    local_govt = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    session_admitted = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term_admitted = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    class_admitted = models.ForeignKey(SchoolClass,on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.sur_name

    
    
class TeacherProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacherprofile')
    local_govt = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    qualification = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.sur_name

# assign subject teacher  
class SubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    classroom = models.ForeignKey(SchoolClass,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='teachersubjects')
    status = models.CharField(max_length=50, default='Active')
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.teacher.sur_name
   

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
