from rest_framework import serializers
from .models import *
import re 
from django.apps import apps


class UserSerializer(serializers.ModelSerializer):



    class Meta:
        model= User
        fields = ['email','password','first_name','last_name','profile_pic','user_role','long','lat','address']

    def create(self,validated_data):
        user = User.objects.create(
            # username= validated_data['email'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_pic = validated_data['profile_pic'],
            user_role = validated_data['user_role'],
            lat = validated_data['lat'],
            long = validated_data['long'],
            address = validated_data['address']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user



# ########### FORM SERIALZIERSSS ##############


class FormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Form
        # fields= "__all__"
        # exclude = ['created_at','updated_at']
        exclude = ['updated_at']



def makeResponseSerializer(id):
    
    attrs = {
            '__module__': __name__,
            
        }

    class Meta:
        model = apps.get_model(app_label='formasticApp', model_name='form_'+ id)
        fields= "__all__"
        # exclude = ['created_at','updated_at']
    attrs['Meta'] = Meta

    serializer = type('Serializer_Form', (serializers.ModelSerializer,), attrs)
    # admin.site.register(model)
    return serializer

