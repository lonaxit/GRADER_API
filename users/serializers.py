from dataclasses import fields
import profile
from rest_framework import serializers


# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model
# from core.api.serializers import *
User = get_user_model()

# user app
class UserSerializer(serializers.ModelSerializer):
    
    # savinguser = SavingSerializer(many=True,read_only=True)
    # totalSaving = serializers.SerializerMethodField()
    
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
        


