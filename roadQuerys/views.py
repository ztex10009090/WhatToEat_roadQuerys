# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from roadQuerys.models import *
from users.models import UserAccount
from django.db.models import Q
from django.db.models import Avg
import datetime
import json


# Create your views here.
def createRoadQuery(request):
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['userId']
    road_query_name = data['roadQueryName']
    road_query_address = data['address']
    road_query_picture = data['roadQueryPicture']
    classify = data['classify']
    introduction = data['introduction']
    star = data['star']
    open_time = data['openTime']
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])
    try:
        u = UserAccount.objects.get(UserID=user_id)
        rq = RoadQuery.objects.create(
            RoadQueryName=road_query_name,
            RoadQueryAddress=road_query_address,
            RoadQueryPicture=road_query_picture,
            Introduction=introduction,
            Star=star,
            OpenTime=open_time,
            Latitude=latitude,
            Longitude=longitude,
            CreateUser=u,
            CreateDate=now(),
            ModifyDate=now()
        )
        for c in classify:
            classification = Classify.objects.get(ClassifyName=c['classifyName'])
            rq.Classify.add(classification)
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getRoadQuery(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    road_query_name = data['name']

    # query
    try:
        r = RoadQuery.objects.get(RoadQueryName=road_query_name)
        result['name'] = r.RoadQueryName
        result['classify'] = r.Classify
        result['address'] = r.RoadQueryAddress
        result['picture'] = 'http://' + request.get_host() + '/images/roadQuerys/' + r.RoadQueryPicture
        result['introduction'] = r.Introduction
        result['openTime'] = r.OpenTime
        result['lat'] = r.Latitude
        result['long'] = r.Longitude
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getClassify(request):
    result = {'result': 0}

    # query
    try:
        classifications = []
        for c in Classify.objects.all():
            classification = {'classifyName': c.ClassifyName}
            classifications.append(classification)
        result['classifications'] = classifications
        result['result'] = 1 if len(classifications) > 0 else 0
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getTag(request):
    result = {'result': 0}

    # query
    try:
        tags = []
        for c in Classify.objects.all():
            classification = {'classifyName': c.ClassifyName,
                              'tagColor': c.TagColor}
            tags.append(classification)
        result['classifications'] = tags
        result['result'] = 1 if len(tags) > 0 else 0
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getRoadQueryList(request):
    result = {'result': 0}

    # query
    try:
        road_querys = []
        for rq in RoadQuery.objects.all():
            classifications = []
            for c in rq.Classify.all():
                classification = {'classifyName': c.ClassifyName}
                classifications.append(classification)
            road_query = {'roadQueryName': rq.RoadQueryName,
                          'address': rq.RoadQueryAddress,
                          'roadQueryPicture': 'http://' + request.get_host() +
                                              '/images/roadQuerys/' + rq.RoadQueryPicture,
                          'classify': classifications,
                          'userId': rq.CreateUser.UserID,
                          'introduction': rq.Introduction,
                          'openTime': rq.OpenTime,
                          'latitude': float(rq.Latitude),
                          'longitude': float(rq.Longitude),
                          'userName': rq.CreateUser.UserName,
                          'userPicture': 'http://' + request.get_host() + '/images/users/' + rq.CreateUser.UserPicture,
                          'createDate': str(rq.CreateDate)}
            road_querys.append(road_query)
        result['roadQuerys'] = road_querys
        result['result'] = 1 if len(road_querys) > 0 else 0
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getSearch(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    kind = data['kind']
    keywords = data['keywords']

    # query
    try:
        road_querys = []
        if kind == "tag":
            for rq in RoadQuery.objects.all():
                classifications = []
                key_num = 0
                key_count = len(keywords)
                for c in rq.Classify.all():
                    for key in keywords:
                        if key['classifyName'] == c.ClassifyName:
                            key_num = key_num + 1
                if key_num >= key_count:
                    for c in rq.Classify.all():
                        classification = {'classifyName': c.ClassifyName}
                        classifications.append(classification)
                    road_query = {'roadQueryName': rq.RoadQueryName,
                                  'address': rq.RoadQueryAddress,
                                  'roadQueryPicture': 'http://' + request.get_host() +
                                                      '/images/roadQuerys/' + rq.RoadQueryPicture,
                                  'classify': classifications,
                                  'userId': rq.CreateUser.UserID,
                                  'introduction': rq.Introduction,
                                  'openTime': rq.OpenTime,
                                  'latitude': float(rq.Latitude),
                                  'longitude': float(rq.Longitude),
                                  'userName': rq.CreateUser.UserName,
                                  'userPicture': 'http://' + request.get_host() + '/images/users/' +
                                                 rq.CreateUser.UserPicture,
                                  'createDate': str(rq.CreateDate)}
                    road_querys.append(road_query)
        elif kind == "word":
            for rq in RoadQuery.objects.filter(Q(RoadQueryName__icontains=keywords) |
                                               Q(RoadQueryAddress__icontains=keywords)):
                classifications = []
                for c in rq.Classify.all():
                    classification = {'classifyName': c.ClassifyName}
                    classifications.append(classification)
                road_query = {'roadQueryName': rq.RoadQueryName,
                              'address': rq.RoadQueryAddress,
                              'roadQueryPicture': 'http://' + request.get_host() +
                                                  '/images/roadQuerys/' + rq.RoadQueryPicture,
                              'classify': classifications,
                              'userId': rq.CreateUser.UserID,
                              'introduction': rq.Introduction,
                              'openTime': rq.OpenTime,
                              'latitude': float(rq.Latitude),
                              'longitude': float(rq.Longitude),
                              'userName': rq.CreateUser.UserName,
                              'userPicture': 'http://' + request.get_host() + '/images/users/' +
                                             rq.CreateUser.UserPicture,
                              'createDate': str(rq.CreateDate)}
                road_querys.append(road_query)
        else:
            pass

        result['roadQuerys'] = road_querys
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getAdvancedSearch(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    keywords = data['keywords']
    abandon = data['abandon']
    star = data['star']

    # query
    try:
        road_querys = []
        for rq in RoadQuery.objects.all():
            classifications = []
            key_num = 0
            key_count = len(keywords)
            ban_num = 0
            for classify in rq.Classify.all():
                for key in keywords:
                    if key['classifyName'] == classify.ClassifyName:
                        key_num = key_num + 1
                for ban in abandon:
                    if ban['classifyName'] == classify.ClassifyName:
                        ban_num = ban_num + 1
            if (key_num >= key_count) and (ban_num == 0) and \
                    (rq.Star >= int(star)):
                for c in rq.Classify.all():
                    classification = {'classifyName': c.ClassifyName}
                    classifications.append(classification)
                road_query = {'roadQueryName': rq.RoadQueryName,
                              'address': rq.RoadQueryAddress,
                              'roadQueryPicture': 'http://' + request.get_host() +
                                                  '/images/roadQuerys/' + rq.RoadQueryPicture,
                              'classify': classifications,
                              'userId': rq.CreateUser.UserID,
                              'introduction': rq.Introduction,
                              'openTime': rq.OpenTime,
                              'latitude': float(rq.Latitude),
                              'longitude': float(rq.Longitude),
                              'userName': rq.CreateUser.UserName,
                              'userPicture': 'http://' + request.get_host() + '/images/users/' +
                                             rq.CreateUser.UserPicture,
                              'createDate': str(rq.CreateDate)}
                road_querys.append(road_query)
        result['roadQuerys'] = road_querys
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def createComment(request):
    # request
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    road_query = data['roadQuery']
    user_id = data['userId']
    comment = data['comment']
    star = data['star']

    # query
    try:
        u = UserAccount.objects.get(UserID=user_id)
        r = RoadQuery.objects.get(RoadQueryName=road_query)
        Comment.objects.create(
            RoadQuery=r,
            User=u,
            StarAmount=star,
            CommentContent=comment,
            CreateDate=now()
        )
        r.Star = Comment.objects.filter(RoadQuery=road_query).aggregate(Avg('StarAmount'))
        r.save()
        result['result'] = 1
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


def getComment(request):
    result = {'result': 0}
    data = json.loads(request.body.decode("utf-8"))
    road_query = data['roadQueryName']

    # query
    try:
        comments = []
        for c in Comment.objects.filter(RoadQuery=road_query):
            comment = {
                'roadQuery': c.RoadQuery,
                'user': c.User,
                'commentContent': c.CommentContent,
                'star': c.StarAmount
            }
            comments.append(comment)
        result['comments'] = comments
        result['result'] = 1 if len(comments) > 0 else 0
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)


# helper
def now():
    return datetime.datetime.now().replace(microsecond=0)
