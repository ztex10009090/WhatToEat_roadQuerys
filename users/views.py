# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage
from WhatToEat_roadQuerys.settings import IMAGE_ROOT, IMAGE_USER_URL, IMAGE_OTHER_URL
from users.models import *
from random import randint
import json
import datetime
import os


# Create your views here.
def index(request):
    return HttpResponse("Home")


def login(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    password = data['password']

    # query
    try:
        u = UserAccount.objects.get(
            UserID=user_id,
            Password=password
        )
        u.save()
        result['userId'] = u.UserID
        result['email'] = u.EMail
        result['userName'] = u.UserName
        result['userPicture'] = 'http://' + request.get_host() + '/images/users/' + u.UserPicture
        result['modifyDate'] = str(u.ModifyDate)
        result['weight'] = u.Weight
        result['signInOrigin'] = u.SignInOrigin
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def threePartLogin(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    user_name = data['userName']
    sign_in_origin = data['signInOrigin']

    # query
    try:
        if UserAccount.objects.filter(UserID=user_id).count() == 0:  # signIn
            u = UserAccount()
            u.UserID = user_id
            u.UserName = user_name
            u.UserPicture = 'default.jpg'
            u.EMail = ''
            u.Password = ''
            u.VerificationCode = ''
            u.SignInOrigin = sign_in_origin
            u.CreateDate = now()
            u.ModifyDate = now()
            u.save()

        u = UserAccount.objects.get(UserID=user_id)
        result['userId'] = u.UserID
        result['email'] = u.EMail
        result['userName'] = u.UserName
        result['userPicture'] = 'http://' + request.get_host() + '/images/users/' + u.UserPicture
        result['weight'] = u.Weight
        result['signInOrigin'] = u.SignInOrigin
        result['modifyDate'] = str(u.ModifyDate)
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def signUp(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    email = data['email']
    password = data['password']
    user_name = data['userName']

    # query
    try:
        if UserAccount.objects.filter(EMail=email).count() == 0:
            UserAccount.objects.create(
                UserID=user_id,
                EMail=email,
                Password=password,
                UserName=user_name,
                UserPicture='default.jpg',
                SignInOrigin='testPost',
                CreateDate=now(),
                ModifyDate=now()
            )
            result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def updatePassword(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    old_password = data['oldPassword']
    new_password = data['newPassword']

    # query
    try:
        u = UserAccount.objects.get(
            UserID=user_id,
            Password=old_password
        )
        u.Password = new_password
        u.save()
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def verifyCode(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    verification_code = data['verificationCode']

    # query
    try:
        UserAccount.objects.get(
            UserID=user_id,
            VerificationCode=verification_code
        )
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def forgetPassword(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    email = data['email']

    # query
    try:
        u = UserAccount.objects.get(
            UserID=user_id,
            EMail=email
        )
        u.VerificationCode = getVerificationCode()
        u.save()
        email = EmailMessage(
            'Hello',
            'Your verificationCode is ' + u.VerificationCode,
            to=[email]
        )
        email.send()
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def resetPassword(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    verification_code = data['verificationCode']
    new_password = data['newPassword']

    # query
    try:
        u = UserAccount.objects.get(
            UserID=user_id,
            VerificationCode=verification_code
        )
        u.Password = new_password
        u.VerificationCode = getVerificationCode()
        u.save()
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def createPicture(request):
    # request
    result = {'result': 0}
    file_name = request.POST.get('fileName')
    sub_file_name = request.POST.get('subFileName')
    my_file = request.FILES.get('file')
    my_type = request.POST.get('type')

    if my_file is not None:
        try:
            complete_file_name = file_name + '.' + sub_file_name
            path = getPath(my_type)
            with open(os.path.join(IMAGE_ROOT, path, complete_file_name), 'wb+') as destination:
                for chunk in my_file.chunks():
                    destination.write(chunk)

            result['picturePath'] = complete_file_name
            result['fullPath'] = 'http://' + request.get_host() + '/images/' + path + '/' + complete_file_name
            result['result'] = 1
        except Exception as e:
            result['message'] = str(e)
    return JsonResponse(result)


def updatePicture(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    picture_path = data['picturePath']

    # query
    try:
        u = UserAccount.objects.get(UserID=user_id)
        u.UserPicture = picture_path
        u.save()
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


# helper
def getVerificationCode():
    code = ''
    for i in range(6):
        code += str(randint(1, 9))
    return code


def getPath(x):
    return {
        "0": IMAGE_USER_URL,
    }.get(x, IMAGE_OTHER_URL)


def now():
    return datetime.datetime.now().replace(microsecond=0)
