import os
# import sys
# sys.path.append('D:/pycharm/workspace/socialNetworkCode/system')


from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
import json

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
# 导入的login 和 logout 用来实现保持session
from django.contrib.auth import authenticate, login, logout

import networkx as nx
# import sys
# from sys import path
# path.append(0,sys.path[0]+'..\\algorithm')

# from system.algorithm import gn-weighted
# from .gn-weighted import *
from . import models
from . import weighted

def login_site(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)   # 使用 Django 的 authenticate 方法来验证
        if user:
            login(request, user)    # <==
            return HttpResponseRedirect(reverse('socialNetworkCode:demo', args=(int(1), int(1),)))
        else:
            return render(request, 'login.html', {
                'login_err': 'Please recheck your username or password !'
            })
    return render(request, 'login.html')


def logout_site(request):
    logout(request)     # <==
    return HttpResponseRedirect('/socialNetworkCode/login/')


@login_required
def demo(request, eventpage, peoplepage):
    limit = 4
    events = models.Sensitiveevent.objects.all().order_by("-warning")
    print(events)
    eventpaginatior = Paginator(events, limit)
    # page = request.GET.get('page', 1)
    eventpagenum = eventpaginatior.num_pages+1
    eventfootnum = {}
    for i in range(1, eventpagenum):
        eventfootnum[i] = i
    event = eventpaginatior.page(eventpage)

    peoples = models.Supversiedpersonlist.objects.all().order_by("-hot")
    peoplepaginator = Paginator(peoples, limit)
    peoplepagenum = peoplepaginator.num_pages + 1
    peoplefootnum = {}
    for i in range(1, peoplepagenum):
        peoplefootnum[i] = i
    people = peoplepaginator.page(peoplepage)

    name = request.GET.get('name')
    if name:
        user_message = models.Supversiedpersonlist()
        user_message.name = name
        n = 1
        for message in peoples:
            n = n+1
        user_message.idperson = n
        user_message.save()
    return render(request, 'demo.html', {"events": event, "people": people, "eventpagenums": eventfootnum, "eventpage": eventpage, "peoplepage": peoplepage, "peoplepagenums": peoplefootnum, })


def search(request):
    name = request.GET.get('name')
    usernames = models.Supversiedpersonlist.objects.all().filter(name__contains=name)
    # 此地很重要，由于要返回json类型到模板，但是json.dumps()只能够把python内置数据类型转化为json，所以以下把上面
    # 从数据库中取出来的queryset型数据转化为数组类型，再用json.dumps()
    # 方可成功。
    # print(usernames)
    rejson = []       #queryset是什么
    for username in usernames:
        rejson.append(username.name)
    print(rejson)
    return HttpResponse(json.dumps(rejson),  content_type='application/json')


@login_required
def relationextraction(request):
    # test2.test()
    return render(request, 'relationextraction.html')

@login_required
def newgn(request):
    users = []

    class User:
        name = "0"
        nickname = "o"
        province = ""
        slogan = ""
        tag = ""

        def __init__(self,name,nickname,province,slogan,tag):
            self.name = name
            self.nickname = nickname
            self.province = province
            self.slogan = slogan
            self.tag = tag

    with open('./system/data/user.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            user = User(line.split("$")[0],line.split("$")[1],line.split("$")[2],line.split("$")[3],line.split("$")[4].strip("\n"))
            users.append(user)

    return render(request, 'newgn.html',{"users":users})

def allgn(request):
    return render(request,'allgn.html')

@login_required
def fileUpload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myFile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("上传失败")
        destination = open(os.path.join("D:\\pycharm\\workspace\\socialNetworkCode\\system\\fileUpload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("上传成功")


@login_required
def peoplenews(request, name):
    username = request.POST.get('name')
    # print(username)
    if username:
        username = username
    else:
        username = name
    user = models.Supversiedpersonlist.objects.all().get(name=username)
    labels = models.Personlabel.objects.all().filter(id_person=user.idperson)
    # users = models.Accountsinformation.objects.all().filter(idperson=user.idperson)
    lives = models.Lifetimelist.objects.all().filter(personnumber=user.idperson)
    print(lives)
    words = models.Wordstopic.objects.all().filter(idperson=user.idperson)
    return render(request, 'peoplenews.html', {"name": user.name, "user": user, "labels": labels, "lives": lives,
                                               "words": words})


@login_required
def all_analysis(request, name):
    media = request.GET.get("media", "facebook")
    relation = request.GET.get("relation", "整体")
    if relation == "整体":
        friends = models.Friendcircle.objects.all().filter(media=media, name=name)
    else:
        friends = models.Friendcircle.objects.all().filter(media=media, name=name, relation=relation)
    friend = []
    # link = []
    for message in friends:
        friend.append({"name": message.to_name})
    friend.append({"name": name})
    user = models.Supversiedpersonlist.objects.all().get(name=name)
    labels = models.Personlabel.objects.all().filter(id_person=user.idperson)
    accounts = models.Accountsinformation.objects.all().filter(idperson=user.idperson)
    return render(request, 'all_analysis.html', {"name": name, "friend": friend, "user": user, "labels": labels,
                                                 "accounts": accounts})

# //add
@login_required
def gn(request,name):
    media = request.GET.get("media", "facebook")
    relation = request.GET.get("relation", "整体")
    nickname = {}
    with open('./system/data/nickname.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            nickname[line.split(",")[0]] = line.split(",")[1].strip("\n")
    return render(request, 'gn.html', {"name": name,"nickname":nickname[name]})

# //add
@login_required
def recommendation(request, name):
    sim_people = []
    dict = {}
    name_type = "0"

    nickname = {}
    with open('./system/data/nickname.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            nickname[line.split(",")[0]] = line.split(",")[1].strip("\n")

    with open('./system/result/doc_topic.txt') as f:
        for line in f:
            s_key = line.split(":")[0]
            s_value = line.split(":")[1].strip('\n')

            dict[s_key] = s_value
            if s_key == name:
                name_type = s_value

    for key in dict:
        if key != name:
            if dict[key] == name_type:
                sim_people.append(nickname[key])

    # print(sim_people)

    # 生成name_type对应的word
    topic_word = ""
    with open('./system/result/topic_word.txt','r', encoding='UTF-8') as f:
        for line in f:
            s_key = line.split(":")[0]
            s_value = line.split(":")[1].strip('\n')
            if s_key == ("Topic #" + str(name_type)):
                topic_word = s_value


    # 生成aprior算法数据

    dictrory = {}
    with open('./system/result/aprior.txt','r', encoding='UTF-8') as f:
        for line in f:
            s1 = line.split(",")[0].split("'")[1]
            s2 = line.split(",")[1]
            s3 = line.split(",")[2].strip('\n')

            if s1 == name:
                for i in range(len(s2.split("'"))):
                    if i%2 ==1:
                        # print(s2.split("'")[i])
                        dictrory[nickname[s2.split("'")[i]]] = s3

    print(dictrory)
    return render(request, 'recommendation.html', {"name": name,"nickname":nickname[name],"sim_people": sim_people,"type": name_type,"topic_word":topic_word,"aprior": json.dumps(dictrory)})


@login_required
def media_focus(request, media, account):
    name = request.GET.get("name")
    account = models.Accountsinformation.objects.all().get(username=account, media=media)
    tweet = models.Twieetslists.objects.all().filter(useraccounts=account, mediasource=media)
    return render(request, 'MediaFocus.html', {"account": account, "tweet": tweet, "name": name})


def friend_circle(request, name):
    media = request.GET.get("media", "facebook")
    relation = request.GET.get("relation", "整体")
    if relation == "整体":
        friends = models.Friendcircle.objects.all().filter(media=media, name=name)
    else:
        friends = models.Friendcircle.objects.all().filter(media=media, name=name, relation=relation)
    rejson = []
    for friend in friends:
        rejson.append({"name": friend.to_name})
    rejson.append({"name": name})
    print(rejson)
    return HttpResponse(json.dumps(rejson))

# //add
def all_gn(request):
    nickname = {}
    with open('./system/data/nickname.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            nickname[line.split(",")[0]] = line.split(",")[1].strip("\n")

    communites = []
    with open('./system/data/communites.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            communite = []
            for num in line.split(","):
                communite.append(nickname[num.strip('\n')]+":"+num.strip('\n'))
            communites.append(communite)

    edges = []
    with open('./system/data/edges.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            edge = []
            for num in line.split(","):
                edge.append(num.strip('\n'))
            edges.append(edge)



    rejson = []
    i = 0
    for edge in edges:
        rejson.append({"source" + str(i): nickname[edge[0]]})
        rejson.append({"target" + str(i): nickname[edge[1]]})
        i = i+1

    rejson.append({"communites": communites})

    print(rejson)
    return HttpResponse(json.dumps(rejson))



def gn_part(request, name):
    # name = "MmeMagloire"
    communites = []

    with open('./system/data/communites.txt','r',encoding='UTF-8') as f:
        for line in f:
            communite = []
            for num in line.split(","):
                communite.append(num.strip('\n'))
            communites.append(communite)

    friends = []
    for communite in communites:
        if name in communite:
            friends = communite
            break
    print(friends)

    edges = []
    with open('./system/data/edges.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            edge = []
            for num in line.split(","):
                edge.append(num.strip('\n'))
            edges.append(edge)


    nickname = {}
    with open('./system/data/nickname.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            nickname[line.split(",")[0]] = line.split(",")[1].strip("\n")

    rejson = []
    rejson.append({"name":nickname[name]})
    dict = {}
    i = 0
    for edge in edges:
        if edge[0] in friends and edge[1] in friends:
            rejson.append({"source" + str(i): nickname[edge[0]]})
            rejson.append({"target" + str(i): nickname[edge[1]]})
            i = i+1

            if edge[0] in dict:
                dict[edge[0]] = dict.get(edge[0]) + 1
            else:
                dict[edge[0]] = 1

            if edge[1] in dict:
                dict[edge[1]] = dict.get(edge[1]) + 1
            else:
                dict[edge[1]] = 1

    maxspread = ""
    maxcount = 0
    totalcount = 0
    for key in dict:
        totalcount += dict[key]
        if dict[key] > maxcount:
            maxspread = key
            maxcount = dict[key]

    rejson.append({"maxspread": nickname[maxspread], "maxcount": round(maxcount/totalcount, 2)})
    # for friend in friends:
    #     rejson.append({"name": friend.to_name})
    print(dict)
    for i in range(len(friends)):
        friends[i] = nickname[friends[i]] + ":" + friends[i]
    rejson.append({"friends": friends})

    d_dict = sorted(dict.items(), key=lambda item: item[1], reverse=True)
    # print(d_dict)
    dict_relation = {}
    for id,count in d_dict:
        if count in dict_relation:
            dict_relation[count] = dict_relation.get(count) + ',' + nickname[id]
        else:
            dict_relation[count] = nickname[id]

    # print(dict_relation)

    rejson.append({"level_num":len(dict_relation),"level":dict_relation})
    print(rejson)
    return HttpResponse(json.dumps(rejson))



@login_required
def param_gender(request,name):
    # name = "MmeMagloire"
    nickname = {}
    with open('./system/data/nickname.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            nickname[line.split(",")[0]] = line.split(",")[1].strip("\n")


    select = request.GET.get("select", "gender")
    dict = {}

    if select == "gender":
        #生成数据集
        with open('./system/data/gender.txt', 'r', encoding='UTF-8') as f:
            for line in f:
                dict[line.split(",")[0]] = line.split(",")[1].strip("\n")

    else:
        # 生成数据集
        with open('./system/data/place.txt', 'r', encoding='UTF-8') as f:
            for line in f:
                dict[line.split(",")[0]] = line.split(",")[1].strip("\n")

    gender = ""
    for key in dict:
        if key == name:
            gender = dict[key]
            break
    node = []
    for key in dict:
        if dict[key] == gender:
            node.append(key)

    print(node)

    edges = []
    with open('./system/data/edges.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            edge = []
            for num in line.split(","):
                edge.append(num.strip('\n'))
            edges.append(edge)


    useedge = []
    for edge in edges:
        if edge[0] in node and edge[1] in node:
            useedge.append([edge[0],edge[1]])

    weighted.make_file(node,useedge)

    G = nx.read_gml('output.gml')

    algorithm = weighted.GN_w(G)

    communication, allq, maxq = algorithm.run()

    print(communication , allq , maxq)

    rejson = []
    for i in range(len(communication)):
        for j in range(len(communication[i])):
            communication[i][j] = nickname[communication[i][j]]
    rejson.append({"communication": communication})

    for i in range(len(useedge)):
        for j in range(len(useedge[i])):
            useedge[i][j] = nickname[useedge[i][j]]
    rejson.append({"edge":useedge})

    rejson.append({"maxQ":maxq})

    print(rejson)
    return HttpResponse(json.dumps(rejson))

@login_required
def sin_analysis(request, name):
    user = models.Supversiedpersonlist.objects.all().get(name=name)
    labels = models.Personlabel.objects.all().filter(id_person=user.idperson)
    accounts = models.Accountsinformation.objects.all().filter(idperson=user.idperson)
    label = request.GET.get('name')
    print(label)
    if label:
        sim_people = models.Similarpeople.objects.all().filter(label=label, id_person=user.idperson).order_by("-similarity")
        events = models.Sensitiveevent.objects.all().filter(label=label).order_by("-hot")
        tweets = models.Twieetslists.objects.all().filter(idperson=user.idperson, label=label).order_by("-warning")
    else:
        sim_people = models.Similarpeople.objects.all().filter(id_person=user.idperson).order_by("-similarity")
        events = models.Sensitiveevent.objects.all().filter().order_by("-hot")
        tweets = models.Twieetslists.objects.all().filter(idperson=user.idperson).order_by("-warning")
    print(sim_people)
    return render(request, 'sin_analysis.html', {"name": name, "labels": labels, "user": user, "accounts": accounts, "sim_people": sim_people, "events": events, "tweets": tweets, "label": label})


@login_required
def person_contrast(request, name, contrast):
    person = models.Supversiedpersonlist.objects.all().get(name=name)
    contrast = models.Supversiedpersonlist.objects.all().get(name=contrast)
    person_labels = models.Personlabel.objects.all().filter(id_person=person.idperson)
    contrast_labels = models.Personlabel.objects.all().filter(id_person=contrast.idperson)
    person_events = models.Personevent.objects.all().filter(person=name)
    contrast_events = models.Personevent.objects.all().filter(person=contrast)

    peoples = models.Supversiedpersonlist.objects.all()
    add_name = request.GET.get('name')
    if add_name:
        usernames = models.Supversiedpersonlist.objects.all().filter(name__contains=add_name)
        if (usernames):
            pass
        else:
            user_message = models.Supversiedpersonlist()
            user_message.name = add_name
            n = 1
            for message in peoples:
                n = n + 1
            user_message.idperson = n
            user_message.save()
    return render(request, 'person_contrast.html', {"name": name, "person": person, "contrast": contrast, "person_labels": person_labels, "contrast_labels": contrast_labels,
                                                    "person_events": person_events, "contrast_events": contrast_events})


@login_required
def person_tweet(request, id_tweet, name):
    tweet = models.Twieetslists.objects.all().get(idtweets=id_tweet)
    tweets = models.Twieetslists.objects.all()
    return render(request, 'person_tweet.html', {"name": name, "tweet": tweet, "tweets": tweets})


@login_required
def person_event(request, event, name):
    eventwords = models.Usersensitivewords.objects.all().filter(sensitivevent=event)
    event_info = models.Sensitiveevent.objects.all().get(sensitivevent=event)
    tweets = models.Twieetslists.objects.all().filter(idsensitivevent=event_info.idsensitivevent)
    return render(request, 'person_event.html', {"name": name, "eventwords": eventwords, "event": event, "event_info": event_info, "tweets": tweets})


@login_required
def sensitiveinfo(request, event):
    page = request.GET.get('page', 1)
    limit = 4
    eventwords = models.Usersensitivewords.objects.all().filter(sensitivevent=event)
    event_infos = models.Sensitiveevent.objects.all().get(sensitivevent=event)
    event_info = event_infos.content
    eventwordspaginatior = Paginator(eventwords, limit)
    eventwordspagenum = eventwordspaginatior.num_pages + 1
    eventwordsfootnum = {}
    for i in range(1, eventwordspagenum):
        eventwordsfootnum[i] = i
    eventwords = eventwordspaginatior.page(page)
    return render(request, 'SensitiveInfo.html', {"eventwords": eventwords, "eventwordspagenums": eventwordsfootnum,
                                                  "eventwordspage": page, "event": event, "event_info": event_info})


@login_required
def sensitive_develop(request, event):
    page = request.GET.get('page', 1)
    limit = 4
    event = models.Sensitiveevent.objects.all().get(sensitivevent=event)
    tweets = models.Twieetslists.objects.all().filter(idsensitivevent=event.idsensitivevent)
    tweetspaginatior = Paginator(tweets, limit)
    tweetspagenum = tweetspaginatior.num_pages + 1
    tweetsfootnum = {}
    for i in range(1, tweetspagenum):
        tweetsfootnum[i] = i
    tweets = tweetspaginatior.page(page)
    return render(request, 'SensitiveDevelop.html', {"tweets": tweets, "tweetspagenums": tweetsfootnum, "tweetspage": page,
                                                     "event": event})


@login_required
def tweet_detail(request, id_tweet):
    tweet = models.Twieetslists.objects.all().get(idtweets=id_tweet)
    tweets = models.Twieetslists.objects.all()
    return render(request, 'TweetDetail.html', {"tweet": tweet, "tweets": tweets})


@login_required
def tweet_analysis(request, id_tweet):

    return render(request, 'TweetAnalysis.html', {})