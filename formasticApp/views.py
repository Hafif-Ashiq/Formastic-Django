

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core import management

import ipinfo
# from FormsAPIs import *

access_token = 'bb1397e42e6439'

# Create your views here.


# Getting all users
@api_view(['GET'])

def get_all_users(request):
    try:
        # make_migrations()
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response({
            "status" : 404 
        })


# Register all users either admin or basic user

# The data['is_staff'] have to be true for admin 
# Else the user created will be basic user with no admin rights
class RegisterUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required= ['email','password','first_name','last_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                'user_role': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='user, admin or super_admin'),
            },
        ),
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                    'user_role': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='user, admin or super_admin'),
                },
            ),
            400: "Bad request response",
        }
    )
    def post(self,request):
            # print('here')
            # print(request.data)
        
        try:
            data = request.data.copy()
            # print('here')
            print(data)
            
            data['user_role'] = 'user'

            # ip_address = request.META.get("REMOTE_ADDR")
            
            # print(ip)

            handler = ipinfo.getHandler(access_token)
            ip_address = '203.82.53.201'
            details = handler.getDetails(ip_address)
            
            # print(details.all)

            data['lat'] = details.latitude
            data['long'] = details.longitude
            data['address'] = details.hostname

            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email = serializer.data['email'])
                token_obj , _ = Token.objects.get_or_create(user = user)
                return Response(
                    {
                    'user' : serializer.data,
                    'token' : str(token_obj)
                },status=201)
            print(serializer.errors)
            return Response(serializer.errors,status=400)
        except Exception as e:
            print('The error : ' ,e)
            return Response({
                'status' : str(e)
            },status=400)
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                'user_role': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='user, admin or super_admin'),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                    'user_role': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='user, admin or super_admin'),
                },
            ),
            400: "Bad request response",
        }
    )
    def patch(self,request):
        try:
            obj = User.objects.get(email=request.data['email'])

            serializer = UserSerializer(obj,data = request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'data' : serializer.data,
                    
                })
            return Response(serializer.errors)
        except Exception as e:
            print(e)
            return Response({
                'status' : str(e)
            },status=400)
    
@api_view(['GET'])
def validateEmail(request):
    email = request.GET['email']
    user = User.objects.filter(email = email)
    print(user)
    if len(user) != 0:
        return Response({"status" : False},status=400)

    return Response({'status':True},status=200)


@api_view(["GET"])
def getIpInfo(request):
    ip = request.META.get("REMOTE_ADDR")
            
    print(ip)

    handler = ipinfo.getHandler(access_token)
    ip_address = '203.82.53.201'
    details = handler.getDetails(ip_address)
    print(details.all)

    return Response(details.all)

class LoginUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email','password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='User data'),
                    
                    'token': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='returns token e.g (<tokenobject>)'),
                },
            ),
            400:openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_OBJECT, description='False'),
                },
            )
        }
    )
    def post(self,request):
        try:
            # print(request.data)
            email = request.data["email"]
            password = request.data["password"]
            user = authenticate(request=request, email=email, password=password)
            
            
            if(user is not None):
                serializer = UserSerializer(user)

                token_obj , _ = Token.objects.get_or_create(user = user)
                return Response({
                'user' : serializer.data,
                'token' :str(token_obj) ,
            })
            return Response({
                'status' : False
            },status=400)
        except Exception as e:
            print(e)
            return Response({
                'status' : str(e)
            },status=404)
        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserData(request):
    # print(request.META)
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split(' ')
    # print(token)
    token = token[1]
    user_id = Token.objects.get(key=token).user_id
    user = User.objects.get(id=user_id)
    userSer = UserSerializer(user)
    return Response(userSer.data,status=200)


class RegisterAdmin(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Can be added by super-Admin only',
            required= ['email','password','first_name','last_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                
            },
        ),
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                    'user_role': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='user, admin or super_admin'),
                },
            ),
            400: "Bad request response",
        }
    )
    def post(self,request):
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.split(' ')
            token = token[1]
            
            
            user_id = Token.objects.get(key=token).user_id

            user = User.objects.get(id=user_id)
            userSer = UserSerializer(user)
            if not userSer.data['user_role'] == 'superadmin' :
                return Response({'status' : False},status=400)
            data = request.data.copy()

        # try:
            data['user_role'] = 'admin'
            data['is_staff'] = True
            
            ip_address = request.META.get("REMOTE_ADDR")
            
            # print(ip)

            handler = ipinfo.getHandler(access_token)
            ip_address = '203.82.53.201'
            details = handler.getDetails(ip_address)
            
            print(details.all)

            data['lat'] = details.latitude
            data['long'] = details.longitude
            data['address'] = details.hostname
            
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email = serializer.data['email'])
                token_obj , _ = Token.objects.get_or_create(user = user)
                return Response({
                    
                    'data' : serializer.data,
                    'token' : str(token_obj)
                },status=201)
            return Response(serializer.errors,status=400)
       
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                    'user_role': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='user, admin or super_admin'),
                },
            ),
            400: "Bad request response",
        }
    )
    def patch(self,request):
        try:
            obj = User.objects.get(email=request.data['email'])

            serializer = UserSerializer(obj,data = request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'data' : serializer.data,
                    
                })
            return Response(serializer.errors)
        except Exception as e:
            print(e)
            return Response({
                'status' : str(e)
            },status=400)



# ############################# FORMS API    (POST, GET, DELETE, UPDATE)



# Making dynamic Response Models
def makeResponseModel(id,meta):
        print(id)
        print(meta)
        

        lines_toAdd = [
            "from django.db import models"
        ]


        class_name = "class Form_"  +str(id) +"(models.Model):"

        fields = [
            '   created_at = models.DateTimeField(auto_now_add=True)',
            '   approved = models.BooleanField(default=False)',
        ]

        sections = json.loads(meta)['sections']
        index = 0
        for section in sections:
            for question in section['questions']:
                field_name = question['question'].replace(' ','_')
                
                if question['type'] == 'textarea':
                    # attrs[field_name +  str(index)] = models.TextField(default="")
                    fields.append(f'   {field_name + str(index)} = models.TextField(default="")')
                elif question['type'] == 'date':
                    # attrs[field_name + str(index)] = models.DateField()
                    fields.append(f'   {field_name + str(index)} = models.DateField()')
                elif question['type'] == 'file':
                    # attrs[field_name + str(index)] = models.FileField(upload_to ='uploads/', null=True)
                    fields.append(f"   {field_name + str(index)} = models.FileField(upload_to ='uploads/', null=True)")

                elif question['type'] == 'checkbox' or  question['type'] == 'multiplechoice':
                    # attrs[field_name +  str(index)] = models.CharField()
                    fields.append(f"   {field_name + str(index)} = models.CharField()")

                else:
                    # attrs[field_name +  str(index)] = models.CharField(default="")
                    fields.append(f"   {field_name + str(index)} = models.CharField()")
                
                index += 1



        file_path = os.path.join(BASE_DIR,"formasticApp", "models","Form_" + str(id) + ".py")
        file_path2 = os.path.join(BASE_DIR,"formasticApp", "models","__init__.py")

        lines_toAdd.append(class_name)
        for field in fields:
            lines_toAdd.append(field)

        with open(file_path, "w") as file:
            for line in lines_toAdd:
                file.write(line+'\n')

        with open(file_path2, "a") as file:
            file.write(f'from .Form_{str(id)} import Form_{str(id)}\n')

       



# Run migrations

def make_migrations():
    # try:
        # Replace 'your_app_name' with the name of your app or leave it as None to make migrations for all apps.
        management.call_command('makemigrations', 'formasticApp')
        management.call_command('migrate', 'formasticApp')

        print("Migrations have been created successfully.")
    # except Exception as e:
    #     print(f"An error occurred while running migrations: {e}")
    



# Slugify for slug field in questions
def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s



class FormAPI(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request):
        # try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.split(' ')
            token = token[1]
            print(token)
            
            user_id = Token.objects.get(key=token).user_id
            data = request.data.copy()
            data['user_id'] = user_id
            data['slug'] = slugify(data['title'])
            # print(data)
            serializer = FormSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # print(responseform)
                return Response({
                    "status" : True,
                    'data' : serializer.data
                })
            return Response(serializer.errors)
        # except Exception as e:
        #     print(e)
        #     return Response({
        #         'status' : 404
        #     })

    def get(self,request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.split(' ')
            token = token[1]
            
            user_id = Token.objects.get(key=token).user_id
            forms = Form.objects.filter(user_id = user_id)

            serializer = FormSerializer(forms,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'status' : 404
            })

    def delete(self,request):
        
        forms = Form.objects.filter(id = request.data['id'])
        print(forms)
        forms.delete()
         
        return Response({
        'status' : True
        })
            
    def patch(self,request):
        data = request.data

        form = Form.objects.get(id = data['id'])

        serializer = FormSerializer(form,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            
            
            return Response(serializer.data)
            
        return Response(serializer.errors)



@api_view(['GET'])
def get_form(request,id):
    try:
        # make_migrations()
        form = Form.objects.get(id=id)
        fields = ''
        serializer = FormSerializer(form)
        
        if serializer.data['published']:
            response_table = apps.get_model(app_label='formasticApp', model_name='form_'+ str(id))
            
            fields = [field.name for field in response_table._meta.get_fields()]
        return Response({
            'data' : serializer.data,
            'fields' : fields
        })
    except Exception as e:
        print(e)
        return Response(status=404)



@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def publishForm(request):
    data = request.data
    data = data.copy()

    form = Form.objects.get(id = data['id'])
    print(form)
    serializer = FormSerializer(form,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        makeResponseModel(data['id'],serializer.data['meta'])
        
        data['form_table'] = 'formasticApp_form_' + str(data['id'])
        data['published'] = True
        serializer = FormSerializer(form,data=data,partial=True)
        if serializer.is_valid():
            make_migrations()   
            serializer.save()
        
            return Response(serializer.data)
        return Response(serializer.errors)
    return Response(serializer.errors)
    

@api_view(['POST'])

def post_response(request,id):
    serializerClass = makeResponseSerializer(id)
    data = request.data
    serializer = serializerClass(data=data)

    # print(data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors,status=400)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

def get_responses(request,id):
    response_table = apps.get_model(app_label='formasticApp', model_name='Form_'+ str(id))
    serializerClass = makeResponseSerializer(id)
    responses = response_table.objects.all()
    serializer = serializerClass(responses,many=True)
    return Response(serializer.data)