from django.urls import path
from .views import *


urlpatterns = [
    path('get-all-users',get_all_users),
    path('register/',RegisterUser.as_view()),
    path('verify-email',validateEmail),
    path('register-admin/',RegisterAdmin.as_view()),
    path('login/',LoginUser.as_view()),
    path('get-user-data',getUserData),
    path('form-api/',FormAPI.as_view()),
    path('get-form/<id>',get_form),
    path('publish-form',publishForm),
    path('ip-info',getIpInfo),
    path('post-response/<id>',post_response),
    path('get-responses/<id>',get_responses)
]