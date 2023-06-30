from dataclasses import fields
import profile
from rest_framework import serializers
from core.api.serializers import *


# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model

User = get_user_model()

# other serializers

class StudentProfileSerializer(serializers.ModelSerializer): #child model
   
    class Meta:
        model = StudentProfile
        fields = "__all__"
        
   
# user app
class UserSerializer(serializers.ModelSerializer):
    studentprofile = StudentProfileSerializer(read_only=True) #parent model
   
    
    class Meta:
        model = User
        # fields = ('id','username','first_name')
        # fields = '__all__'
        exclude=('password','last_login','is_superuser','user_permissions','groups',)
 

class TeacherProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeacherProfile
        fields = "__all__"       
   
   
        
class UserTeacherSerializer(serializers.ModelSerializer):
    teacherprofile = TeacherProfileSerializer(read_only=True) #parent model
   
    
    class Meta:
        model = User
        # fields = ('id','username','first_name')
        # fields = '__all__'
        exclude=('password','last_login','is_superuser','user_permissions','groups',)
        
        
        



# 
class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','password')


class UpdatePasswordWithUsernameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','password','username')
        


