
import json
import os
from django import utils
from django.db import models

from django.contrib.auth.models import User

from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.apps import apps

from formastic.settings import BASE_DIR

# Create your models here.


# User._meta.get_field('email').blank = False
# User._meta.get_field('first_name').blank = False
# User._meta.get_field('last_name').blank = False
# User._meta.get_field('email')._unique = True
# User._meta.get_field('is_staff').editable = False



# Creating User class so that we could add different fields in it later on as well
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)
    
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be a staff'
            )


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_role', 'superadmin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be a staff'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be a superuser'
            )

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255,blank=False)
    first_name = models.CharField('first name',max_length=150,blank=True)
    last_name = models.CharField('last name',max_length=150,blank=True)
    mobile= models.PositiveBigIntegerField('mobile',null=True,blank=True)
    is_staff = models.BooleanField('staff status',default=False)
    is_active = models.BooleanField('active',default=True)
    is_superuser = models.BooleanField('superuser',default=False)

    date_joined = models.DateTimeField('date joined',default=timezone.now)
    lat = models.CharField('location latitude',default="")
    long = models.CharField('location longitude',default="")
    address = models.CharField('Address',default="")
    profile_pic = models.ImageField('Profile Picture',upload_to='profile_pictures',default='none')
    user_role = models.CharField('Role of User', default="user")
    # admin = models.BooleanField('admin',default=False)
    # long = models.IntegerField()
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name+" "+self.last_name
    


# Other Models





# ############################ FORM MODEL



class Form(models.Model):
    title = models.CharField()
    description = models.CharField(default="",blank=True)
    meta = models.TextField(default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # slug = models.UUIDField(editable=False,default=uuid.uuid4)
    published = models.BooleanField(default=False)
    form_table = models.CharField(default="",blank=True)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)




# Make Dynamic form models
    @property
    def makeResponseModel(self):

        

        lines_toAdd = [
            "from django.db import models"
        ]


        class_name = "class 'Form_'"  +str(self.id) +"(models.Model):"

        fields = [
            '   created_at = models.DateTimeField(auto_now_add=True)',
            '   approved = models.BooleanField(default=False)',
        ]

        sections = json.loads(self.meta)['sections']
        index = 0
        for section in sections:
            for question in section['questions']:
                field_name = question['question'].replace(' ','_')
                
                if question['type'] == 'textarea':
                    # attrs[field_name +  str(index)] = models.TextField(default="")
                    fields.append(f'    {field_name + str(index)} = models.TextField(default="")')
                elif question['type'] == 'date':
                    # attrs[field_name + str(index)] = models.DateField()
                    fields.append(f'    {field_name + str(index)} = models.DateField()')
                elif question['type'] == 'file':
                    # attrs[field_name + str(index)] = models.FileField(upload_to ='uploads/', null=True)
                    fields.append(f"    {field_name + str(index)} = models.FileField(upload_to ='uploads/', null=True)")

                elif question['type'] == 'checkbox' or  question['type'] == 'multiplechoice':
                    # attrs[field_name +  str(index)] = models.CharField()
                    fields.append(f"    {field_name + str(index)} = models.CharField()")

                else:
                    # attrs[field_name +  str(index)] = models.CharField(default="")
                    fields.append(f"    {field_name + str(index)} = models.CharField()")
                
                index += 1



        file_path = os.path.join(BASE_DIR,"formasticApp","models", f"Form_{str(self.id)}.py")

        lines_toAdd.append(class_name)
        for field in fields:
            lines_toAdd.append(field)

        with open(file_path, "w") as file:
            for line in lines_toAdd:
                file.write(line+'\n')

        
        # attrs = {
        #     '__module__': __name__,
            
        # }

        # class Meta:
        #     app_label = 'formasticApp'
        #     verbose_name = self.title + ' Response'
        #     # managed = False
        # attrs['Meta'] = Meta

        
        
        # if self.meta != '':
        #     attrs['created_at'] = models.DateTimeField(auto_now_add=True)
        #     attrs['approved'] = models.BooleanField(default=False)

        #     sections = json.loads(self.meta)['sections']
        #     index = 0
        #     for section in sections:
        #         for question in section['questions']:
        #             field_name = question['question'].replace(' ','_')
                    
        #             if question['type'] == 'textarea':
        #                 attrs[field_name +  str(index)] = models.TextField(default="")
        #             elif question['type'] == 'date':
        #                 attrs[field_name + str(index)] = models.DateField()
        #             elif question['type'] == 'file':
        #                 attrs[field_name + str(index)] = models.FileField(upload_to ='uploads/', null=True)
        #             elif question['type'] == 'checkbox' or  question['type'] == 'multiplechoice':
        #                 attrs[field_name +  str(index)] =models.CharField()
        #             else:
        #                 attrs[field_name +  str(index)] = models.CharField(default="")
                    
        #             index += 1

        # model_name = 'Form_'+str(self.id)
        # model = type(model_name, (models.Model,), attrs)
        # apps.get_app_config('formasticApp').models_module.__dict__[model_name] = model
        # admin.site.register(model)

        # return model




from .Form_22 import Form_22

from .Form_13 import Form_13


from .Form_24 import Form_24
