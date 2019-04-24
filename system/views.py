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

    return render(request, 'newgn.html')

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
    return render(request, 'gn.html', {"name": name})

# //add
@login_required
def recommendation(request, name):
    friend = []
    sim_people = []
    # name = "MmeMagloire"
    dict = {}
    # 生成数据集
    dict["MmeMagloire"] = ['摄影师','狗狗','睡觉','电影','90后','旅游']
    dict["Geborand"] = ['健身','美食','武汉大学']
    dict["MlleBaptistine"] = ['剁手','美食','快乐','活力']
    dict["Napoleon"] = ['唱歌','宅','时尚','美食','音乐','电影','活力','希望','信念','快乐']
    dict["Champtercier"] = ['剁手','美食','快乐','活力']
    dict["CountessDeLo"] = ['健康','90后']
    dict["Cravatte"] = ['体育']
    dict["Count"] = ['名人明星','旅游','IT数码','美女']
    dict["Myriel"] = ['旅游','活力','信念','健身']
    dict["OldMan"] = ['美食']
    dict["Labarre"] = ['健身','抽奖','转发狂魔']
    dict["Anzelma"] = ['生活','睡觉','90后']
    dict["Gillenormand"] = ['转发狂魔']
    dict["Fauchelevent"] = ['摄影师','狗狗','睡觉','电影','90后','旅游']
    dict["Montparnasse"] = ['健身','美食','武汉大学']
    dict["MotherInnocent"] = ['剁手','美食','快乐','活力']
    dict["Javert"] = ['唱歌','宅','时尚','美食','音乐','电影','活力','希望','信念','快乐']
    dict["Woman2"] = ['剁手','美食','快乐','活力']
    dict["MmeThenardier"] = ['健康','90后']
    dict["Simplice"] = ['体育']
    dict["Woman1"] = ['名人明星','旅游','IT数码','美女']
    dict["Thenardier"] = ['旅游','活力','信念','健身']
    dict["MlleGillenormand"] = ['旅游','活力','信念','健身']
    dict["Eponine"] = ['美食']
    dict["Gueulemer"] = ['健身','抽奖','转发狂魔']
    dict["Babet"] = ['生活','睡觉','90后']
    dict["Claquesous"] = ['转发狂魔']
    dict["Brujon"] = ['摄影师','狗狗','睡觉','电影','90后','旅游']
    dict["Marius"] = ['健身','美食','武汉大学']
    dict["Cosette"] = ['剁手','美食','快乐','活力']
    dict["Valjean"] = ['剁手','美食','快乐','活力']
    dict["Zephine"] = ['体育']
    dict["Fantine"] = ['健康','90后']
    dict["Tholomyes"] = ['生活','睡觉','90后']
    dict["Dahlia"] = ['美食']
    dict["Fameuil"] = ['体育']
    dict["Listolier"] = ['生活','睡觉','90后']
    dict["Blacheville"] = ['美食']
    dict["Marguerite"] = ['转发狂魔']
    dict["Favourite"] = ['健康','90后']
    dict["MmeDeR"] = ['生活']
    dict["Isabeau"] = ['转发狂魔']
    dict["Gervais"] = ['健康','90后']
    dict["Chenildieu"] = ['生活']
    dict["Brevet"] = ['美食']
    dict["Cochepaille"] = ['转发狂魔']
    dict["Bamatabois"] = ['生活','睡觉','90后']
    dict["Champmathieu"] = ['剁手','美食','快乐','活力']
    dict["Judge"] = ['转发狂魔']
    dict["Perpetue"] = ['生活']
    dict["Scaufflaire"] = ['健康','90后']
    dict["MmePontmercy"] = ['转发狂魔']
    dict["Pontmercy"] = ['生活']
    dict["Boulatruelle"] = ['健康','90后']
    dict["Gribier"] = ['生活']
    dict["Jondrette"] = ['转发狂魔']
    dict["Mabeuf"] = ['健康','90后']
    dict["MmeBurgon"] = ['美食']
    dict["Combeferre"] = ['快乐','活力']
    dict["Prouvaire"] = ['生活']
    dict["Joly"] = ['健康','90后']
    dict["Grantaire"] = ['美食']
    dict["Feuilly"] = ['健康','90后']
    dict["Bahorel"] = "woman"
    dict["Courfeyrac"] = ['美食']
    dict["Gavroche"] = ['健康','90后']
    dict["Bossuet"] = "man"
    dict["MotherPlutarch"] = ['剁手','活力']
    dict["Child1"] = ['美食']
    dict["MmeHucheloup"] = ['健身','武汉大学']
    dict["Child2"] = ['健身']
    dict["Enjolras"] = ['美食']
    dict["Magnon"] = ['健身','美食','武汉大学']
    dict["MlleVaubois"] = ['健身']
    dict["LtGillenormand"] = ['武汉大学']
    dict["BaronessT"] = ['美食']
    dict["Toussaint"] = ['美食']

    label = []
    # sim_people_label = []

    for key in dict:
        if key == name:
            label = dict[key]
            break

    for key in dict:
        temp = dict[key]
        if key != name:
            for t in temp:
                if t in label:
                    sim_people.append([key,t])
                    # sim_people_label.append(t)

    print(sim_people)


    return render(request, 'recommendation.html', {"name": name,"sim_people": sim_people})


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

def gn_part(request, name):
    # name = "MmeMagloire"
    communites = []
    communites.append(['MmeMagloire', 'Geborand', 'MlleBaptistine', 'Napoleon', 'Champtercier', 'CountessDeLo', 'Cravatte', 'Count', 'Myriel', 'OldMan'])
    communites.append(['Labarre'])
    communites.append(['Anzelma', 'Gillenormand', 'Fauchelevent', 'Montparnasse', 'MotherInnocent', 'Javert', 'Woman2', 'MmeThenardier', 'Simplice', 'Woman1', 'Thenardier', 'MlleGillenormand', 'Eponine', 'Gueulemer', 'Babet', 'Claquesous', 'Brujon', 'Marius', 'Cosette', 'Valjean'])
    communites.append(['Zephine', 'Fantine', 'Tholomyes', 'Dahlia', 'Fameuil', 'Listolier', 'Blacheville', 'Marguerite', 'Favourite'])
    communites.append(['MmeDeR'])
    communites.append(['Isabeau'])
    communites.append(['Gervais'])
    communites.append(['Chenildieu', 'Brevet', 'Cochepaille', 'Bamatabois', 'Champmathieu', 'Judge'])
    communites.append(['Perpetue'])
    communites.append(['Scaufflaire'])
    communites.append(['MmePontmercy', 'Pontmercy'])
    communites.append(['Boulatruelle'])
    communites.append(['Gribier'])
    communites.append(['Jondrette'])
    communites.append(['Mabeuf', 'MmeBurgon', 'Combeferre', 'Prouvaire', 'Joly', 'Grantaire', 'Feuilly', 'Bahorel', 'Courfeyrac', 'Gavroche', 'Bossuet', 'MotherPlutarch', 'Child1', 'MmeHucheloup', 'Child2', 'Enjolras'])
    communites.append(['Magnon'])
    communites.append(['MlleVaubois'])
    communites.append(['LtGillenormand'])
    communites.append(['BaronessT'])
    communites.append(['Toussaint'])

    friends = []
    for communite in communites:
        if name in communite:
            friends = communite
            break
    print(friends)

    edges = []
    edges.append(["Napoleon","Myriel"])
    edges.append(["MlleBaptistine","Myriel"])
    edges.append(["MmeMagloire","Myriel"])
    edges.append(["MmeMagloire","MlleBaptistine"])
    edges.append(["CountessDeLo","Myriel"])
    edges.append(["Geborand","Myriel"])
    edges.append(["Champtercier","Myriel"])
    edges.append(["Cravatte","Myriel"])
    edges.append(["Count","Myriel"])
    edges.append(["OldMan","Myriel"])
    edges.append(["Valjean","Labarre"])
    edges.append(["Valjean","MmeMagloire"])
    edges.append(["Valjean","MlleBaptistine"])
    edges.append(["Valjean","Myriel"])
    edges.append(["Marguerite","Valjean"])
    edges.append(["MmeDeR","Valjean"])
    edges.append(["Isabeau","Valjean"])
    edges.append(["Gervais","Valjean"])
    edges.append(["Listolier","Tholomyes"])
    edges.append(["Fameuil","Tholomyes"])
    edges.append(["Fameuil","Listolier"])
    edges.append(["Blacheville","Tholomyes"])
    edges.append(["Blacheville","Listolier"])
    edges.append(["Blacheville","Fameuil"])
    edges.append(["Favourite","Tholomyes"])
    edges.append(["Favourite","Listolier"])
    edges.append(["Favourite","Fameuil"])
    edges.append(["Favourite","Blacheville"])
    edges.append(["Dahlia","Tholomyes"])
    edges.append(["Dahlia","Listolier"])
    edges.append(["Dahlia","Fameuil"])
    edges.append(["Dahlia","Blacheville"])
    edges.append(["Dahlia","Favourite"])
    edges.append(["Zephine","Tholomyes"])
    edges.append(["Zephine","Listolier"])
    edges.append(["Zephine","Fameuil"])
    edges.append(["Zephine","Blacheville"])
    edges.append(["Zephine","Favourite"])
    edges.append(["Zephine","Dahlia"])
    edges.append(["Fantine","Tholomyes"])
    edges.append(["Fantine","Listolier"])
    edges.append(["Fantine","Fameuil"])
    edges.append(["Fantine","Blacheville"])
    edges.append(["Fantine","Favourite"])
    edges.append(["Fantine","Dahlia"])
    edges.append(["Fantine","Zephine"])
    edges.append(["Fantine","Marguerite"])
    edges.append(["Fantine","Valjean"])
    edges.append(["MmeThenardier","Fantine"])
    edges.append(["MmeThenardier","Valjean"])
    edges.append(["Thenardier","MmeThenardier"])
    edges.append(["Thenardier","Fantine"])
    edges.append(["Thenardier","Valjean"])
    edges.append(["Cosette","MmeThenardier"])
    edges.append(["Cosette","Valjean"])
    edges.append(["Cosette","Tholomyes"])
    edges.append(["Cosette","Thenardier"])
    edges.append(["Javert","Valjean"])
    edges.append(["Javert","Fantine"])
    edges.append(["Javert","Thenardier"])
    edges.append(["Javert","MmeThenardier"])
    edges.append(["Javert","Cosette"])
    edges.append(["Fauchelevent","Valjean"])
    edges.append(["Fauchelevent","Javert"])
    edges.append(["Bamatabois","Fantine"])
    edges.append(["Bamatabois","Javert"])
    edges.append(["Bamatabois","Valjean"])
    edges.append(["Perpetue","Fantine"])
    edges.append(["Simplice","Perpetue"])
    edges.append(["Simplice","Valjean"])
    edges.append(["Simplice","Fantine"])
    edges.append(["Simplice","Javert"])
    edges.append(["Scaufflaire","Valjean"])
    edges.append(["Woman1","Valjean"])
    edges.append(["Woman1","Javert"])
    edges.append(["Judge","Valjean"])
    edges.append(["Judge","Bamatabois"])
    edges.append(["Champmathieu","Valjean"])
    edges.append(["Champmathieu","Judge"])
    edges.append(["Champmathieu","Bamatabois"])
    edges.append(["Brevet","Judge"])
    edges.append(["Brevet","Champmathieu"])
    edges.append(["Brevet","Valjean"])
    edges.append(["Brevet","Bamatabois"])
    edges.append(["Chenildieu","Judge"])
    edges.append(["Chenildieu","Champmathieu"])
    edges.append(["Chenildieu","Brevet"])
    edges.append(["Chenildieu","Valjean"])
    edges.append(["Chenildieu","Bamatabois"])
    edges.append(["Cochepaille","Judge"])
    edges.append(["Cochepaille","Champmathieu"])
    edges.append(["Cochepaille","Brevet"])
    edges.append(["Cochepaille","Chenildieu"])
    edges.append(["Cochepaille","Valjean"])
    edges.append(["Cochepaille","Bamatabois"])
    edges.append(["Pontmercy","Thenardier"])
    edges.append(["Boulatruelle","Thenardier"])
    edges.append(["Eponine","MmeThenardier"])
    edges.append(["Eponine","Thenardier"])
    edges.append(["Anzelma","Eponine"])
    edges.append(["Anzelma","Thenardier"])
    edges.append(["Anzelma","MmeThenardier"])
    edges.append(["Woman2","Valjean"])
    edges.append(["Woman2","Cosette"])
    edges.append(["Woman2","Javert"])
    edges.append(["MotherInnocent","Fauchelevent"])
    edges.append(["MotherInnocent","Valjean"])
    edges.append(["Gribier","Fauchelevent"])
    edges.append(["MmeBurgon","Jondrette"])
    edges.append(["Gavroche","MmeBurgon"])
    edges.append(["Gavroche","Thenardier"])
    edges.append(["Gavroche","Javert"])
    edges.append(["Gavroche","Valjean"])
    edges.append(["Gillenormand","Cosette"])
    edges.append(["Gillenormand","Valjean"])
    edges.append(["Magnon","Gillenormand"])
    edges.append(["Magnon","MmeThenardier"])
    edges.append(["MlleGillenormand","Gillenormand"])
    edges.append(["MlleGillenormand","Cosette"])
    edges.append(["MlleGillenormand","Valjean"])
    edges.append(["MmePontmercy","MlleGillenormand"])
    edges.append(["MmePontmercy","Pontmercy"])
    edges.append(["MlleVaubois","MlleGillenormand"])
    edges.append(["LtGillenormand","MlleGillenormand"])
    edges.append(["LtGillenormand","Gillenormand"])
    edges.append(["LtGillenormand","Cosette"])
    edges.append(["Marius","MlleGillenormand"])
    edges.append(["Marius","Gillenormand"])
    edges.append(["Marius","Pontmercy"])
    edges.append(["Marius","LtGillenormand"])
    edges.append(["Marius","Cosette"])
    edges.append(["Marius","Valjean"])
    edges.append(["Marius","Tholomyes"])
    edges.append(["Marius","Thenardier"])
    edges.append(["Marius","Eponine"])
    edges.append(["Marius","Gavroche"])
    edges.append(["BaronessT","Gillenormand"])
    edges.append(["BaronessT","Marius"])
    edges.append(["Mabeuf","Marius"])
    edges.append(["Mabeuf","Eponine"])
    edges.append(["Mabeuf","Gavroche"])
    edges.append(["Enjolras","Marius"])
    edges.append(["Enjolras","Gavroche"])
    edges.append(["Enjolras","Javert"])
    edges.append(["Enjolras","Mabeuf"])
    edges.append(["Enjolras","Valjean"])
    edges.append(["Combeferre","Enjolras"])
    edges.append(["Combeferre","Marius"])
    edges.append(["Combeferre","Gavroche"])
    edges.append(["Combeferre","Mabeuf"])
    edges.append(["Prouvaire","Gavroche"])
    edges.append(["Prouvaire","Enjolras"])
    edges.append(["Prouvaire","Combeferre"])
    edges.append(["Feuilly","Gavroche"])
    edges.append(["Feuilly","Enjolras"])
    edges.append(["Feuilly","Prouvaire"])
    edges.append(["Feuilly","Combeferre"])
    edges.append(["Feuilly","Mabeuf"])
    edges.append(["Feuilly","Marius"])
    edges.append(["Courfeyrac","Marius"])
    edges.append(["Courfeyrac","Enjolras"])
    edges.append(["Courfeyrac","Combeferre"])
    edges.append(["Courfeyrac","Gavroche"])
    edges.append(["Courfeyrac","Mabeuf"])
    edges.append(["Courfeyrac","Eponine"])
    edges.append(["Courfeyrac","Feuilly"])
    edges.append(["Courfeyrac","Prouvaire"])
    edges.append(["Bahorel","Combeferre"])
    edges.append(["Bahorel","Gavroche"])
    edges.append(["Bahorel","Courfeyrac"])
    edges.append(["Bahorel","Mabeuf"])
    edges.append(["Bahorel","Enjolras"])
    edges.append(["Bahorel","Feuilly"])
    edges.append(["Bahorel","Prouvaire"])
    edges.append(["Bahorel","Marius"])
    edges.append(["Bossuet","Marius"])
    edges.append(["Bossuet","Courfeyrac"])
    edges.append(["Bossuet","Gavroche"])
    edges.append(["Bossuet","Bahorel"])
    edges.append(["Bossuet","Enjolras"])
    edges.append(["Bossuet","Feuilly"])
    edges.append(["Bossuet","Prouvaire"])
    edges.append(["Bossuet","Combeferre"])
    edges.append(["Bossuet","Mabeuf"])
    edges.append(["Bossuet","Valjean"])
    edges.append(["Joly","Bahorel"])
    edges.append(["Joly","Bossuet"])
    edges.append(["Joly","Gavroche"])
    edges.append(["Joly","Courfeyrac"])
    edges.append(["Joly","Enjolras"])
    edges.append(["Joly","Feuilly"])
    edges.append(["Joly","Prouvaire"])
    edges.append(["Joly","Combeferre"])
    edges.append(["Joly","Mabeuf"])
    edges.append(["Joly","Marius"])
    edges.append(["Grantaire","Bossuet"])
    edges.append(["Grantaire","Enjolras"])
    edges.append(["Grantaire","Combeferre"])
    edges.append(["Grantaire","Courfeyrac"])
    edges.append(["Grantaire","Joly"])
    edges.append(["Grantaire","Gavroche"])
    edges.append(["Grantaire","Bahorel"])
    edges.append(["Grantaire","Feuilly"])
    edges.append(["Grantaire","Prouvaire"])
    edges.append(["MotherPlutarch","Mabeuf"])
    edges.append(["Gueulemer","Thenardier"])
    edges.append(["Gueulemer","Valjean"])
    edges.append(["Gueulemer","MmeThenardier"])
    edges.append(["Gueulemer","Javert"])
    edges.append(["Gueulemer","Gavroche"])
    edges.append(["Gueulemer","Eponine"])
    edges.append(["Babet","Thenardier"])
    edges.append(["Babet","Gueulemer"])
    edges.append(["Babet","Valjean"])
    edges.append(["Babet","MmeThenardier"])
    edges.append(["Babet","Javert"])
    edges.append(["Babet","Gavroche"])
    edges.append(["Babet","Eponine"])
    edges.append(["Claquesous","Thenardier"])
    edges.append(["Claquesous","Babet"])
    edges.append(["Claquesous","Gueulemer"])
    edges.append(["Claquesous","Valjean"])
    edges.append(["Claquesous","MmeThenardier"])
    edges.append(["Claquesous","Javert"])
    edges.append(["Claquesous","Eponine"])
    edges.append(["Claquesous","Enjolras"])
    edges.append(["Montparnasse","Javert"])
    edges.append(["Montparnasse","Babet"])
    edges.append(["Montparnasse","Gueulemer"])
    edges.append(["Montparnasse","Claquesous"])
    edges.append(["Montparnasse","Valjean"])
    edges.append(["Montparnasse","Gavroche"])
    edges.append(["Montparnasse","Eponine"])
    edges.append(["Montparnasse","Thenardier"])
    edges.append(["Toussaint","Cosette"])
    edges.append(["Toussaint","Javert"])
    edges.append(["Toussaint","Valjean"])
    edges.append(["Child1","Gavroche"])
    edges.append(["Child2","Gavroche"])
    edges.append(["Child2","Child1"])
    edges.append(["Brujon","Babet"])
    edges.append(["Brujon","Gueulemer"])
    edges.append(["Brujon","Thenardier"])
    edges.append(["Brujon","Gavroche"])
    edges.append(["Brujon","Eponine"])
    edges.append(["Brujon","Claquesous"])
    edges.append(["Brujon","Montparnasse"])
    edges.append(["MmeHucheloup","Bossuet"])
    edges.append(["MmeHucheloup","Joly"])
    edges.append(["MmeHucheloup","Grantaire"])
    edges.append(["MmeHucheloup","Bahorel"])
    edges.append(["MmeHucheloup","Courfeyrac"])
    edges.append(["MmeHucheloup","Gavroche"])
    edges.append(["MmeHucheloup","Enjolras"])

    rejson = []
    rejson.append({"name":name})
    dict = {}
    i = 0
    for edge in edges:
        if edge[0] in friends and edge[1] in friends:
            rejson.append({"source" + str(i): edge[0]})
            rejson.append({"target" + str(i): edge[1]})
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

    rejson.append({"maxspread": maxspread, "maxcount": round(maxcount/totalcount, 2)})
    # for friend in friends:
    #     rejson.append({"name": friend.to_name})
    rejson.append({"friends": friends})


    print(rejson)
    return HttpResponse(json.dumps(rejson))

@login_required
def param_gender(request,name):
    # name = "MmeMagloire"
    select = request.GET.get("select", "gender")
    dict = {}

    if select == "gender":
        #生成数据集
        dict["MmeMagloire"] = "man"
        dict["Geborand"] = "woman"
        dict["MlleBaptistine"] = "man"
        dict["Napoleon"] = "woman"
        dict["Champtercier"] = "man"
        dict["CountessDeLo"] = "woman"
        dict["Cravatte"] = "man"
        dict["Count"] = "woman"
        dict["Myriel"] = "man"
        dict["OldMan"] = "woman"
        dict["Labarre"] = "man"
        dict["Anzelma"] = "woman"
        dict["Gillenormand"] = "man"
        dict["Fauchelevent"] = "woman"
        dict["Montparnasse"] = "man"
        dict["MotherInnocent"] = "woman"
        dict["Javert"] = "man"
        dict["Woman2"] = "woman"
        dict["MmeThenardier"] = "man"
        dict["Simplice"] = "woman"
        dict["Woman1"] = "man"
        dict["Thenardier"] = "woman"
        dict["MlleGillenormand"] = "man"
        dict["Eponine"] = "woman"
        dict["Gueulemer"] = "man"
        dict["Babet"] = "woman"
        dict["Claquesous"] = "man"
        dict["Brujon"] = "woman"
        dict["Marius"] = "man"
        dict["Cosette"] = "woman"
        dict["Valjean"] = "man"
        dict["Zephine"] = "woman"
        dict["Fantine"] = "man"
        dict["Tholomyes"] = "woman"
        dict["Dahlia"] = "man"
        dict["Fameuil"] = "woman"
        dict["Listolier"] = "man"
        dict["Blacheville"] = "woman"
        dict["Marguerite"] = "man"
        dict["Favourite"] = "woman"
        dict["MmeDeR"] = "man"
        dict["Isabeau"] = "woman"
        dict["Gervais"] = "man"
        dict["Chenildieu"] = "woman"
        dict["Brevet"] = "man"
        dict["Cochepaille"] = "woman"
        dict["Bamatabois"] = "man"
        dict["Champmathieu"] = "woman"
        dict["Judge"] = "man"
        dict["Perpetue"] = "woman"
        dict["Scaufflaire"] = "man"
        dict["MmePontmercy"] = "woman"
        dict["Pontmercy"] = "man"
        dict["Boulatruelle"] = "woman"
        dict["Gribier"] = "man"
        dict["Jondrette"] = "woman"
        dict["Mabeuf"] = "man"
        dict["MmeBurgon"] = "woman"
        dict["Combeferre"] = "man"
        dict["Prouvaire"] = "woman"
        dict["Joly"] = "man"
        dict["Grantaire"] = "woman"
        dict["Feuilly"] = "man"
        dict["Bahorel"] = "woman"
        dict["Courfeyrac"] = "man"
        dict["Gavroche"] = "woman"
        dict["Bossuet"] = "man"
        dict["MotherPlutarch"] = "woman"
        dict["Child1"] = "man"
        dict["MmeHucheloup"] = "woman"
        dict["Child2"] = "man"
        dict["Enjolras"] = "woman"
        dict["Magnon"] = "man"
        dict["MlleVaubois"] = "woman"
        dict["LtGillenormand"] = "man"
        dict["BaronessT"] = "woman"
        dict["Toussaint"] = "man"
    else:
        # 生成数据集
        dict["MmeMagloire"] = "jiangsu"
        dict["Geborand"] = "beijing"
        dict["MlleBaptistine"] = "jiangxi"
        dict["Napoleon"] = "chengdu"
        dict["Champtercier"] = "sichuan"
        dict["CountessDeLo"] = "shanxi"
        dict["Cravatte"] = "beijing"
        dict["Count"] = "shandong"
        dict["Myriel"] = "hunan"
        dict["OldMan"] = "sichuan"
        dict["Labarre"] = "chongqing"
        dict["Anzelma"] = "shanxi"
        dict["Gillenormand"] = "jiangsu"
        dict["Fauchelevent"] = "beijing"
        dict["Montparnasse"] = "jiangxi"
        dict["MotherInnocent"] = "chengdu"
        dict["Javert"] = "sichuan"
        dict["Woman2"] = "shanxi"
        dict["MmeThenardier"] = "beijing"
        dict["Simplice"] = "shandong"
        dict["Woman1"] = "hunan"
        dict["Thenardier"] = "sichuan"
        dict["MlleGillenormand"] = "chongqing"
        dict["Eponine"] = "shanxi"
        dict["Gueulemer"] = "jiangsu"
        dict["Babet"] = "beijing"
        dict["Claquesous"] = "jiangxi"
        dict["Brujon"] = "chengdu"
        dict["Marius"] = "sichuan"
        dict["Cosette"] = "shanxi"
        dict["Valjean"] = "beijing"
        dict["Zephine"] = "shandong"
        dict["Fantine"] = "hunan"
        dict["Tholomyes"] = "sichuan"
        dict["Dahlia"] = "chongqing"
        dict["Fameuil"] = "shanxi"
        dict["Listolier"] = "jiangsu"
        dict["Blacheville"] = "beijing"
        dict["Marguerite"] = "jiangxi"
        dict["Favourite"] = "chengdu"
        dict["MmeDeR"] = "sichuan"
        dict["Isabeau"] = "shanxi"
        dict["Gervais"] = "beijing"
        dict["Chenildieu"] = "shandong"
        dict["Brevet"] = "hunan"
        dict["Cochepaille"] = "sichuan"
        dict["Bamatabois"] = "chongqing"
        dict["Champmathieu"] = "shanxi"
        dict["Judge"] = "jiangsu"
        dict["Perpetue"] = "beijing"
        dict["Scaufflaire"] = "jiangxi"
        dict["MmePontmercy"] = "chengdu"
        dict["Pontmercy"] = "sichuan"
        dict["Boulatruelle"] = "shanxi"
        dict["Gribier"] = "beijing"
        dict["Jondrette"] = "shandong"
        dict["Mabeuf"] = "hunan"
        dict["MmeBurgon"] = "sichuan"
        dict["Combeferre"] = "chongqing"
        dict["Prouvaire"] = "shanxi"
        dict["Joly"] = "jiangsu"
        dict["Grantaire"] = "beijing"
        dict["Feuilly"] = "jiangxi"
        dict["Bahorel"] = "chengdu"
        dict["Courfeyrac"] = "sichuan"
        dict["Gavroche"] = "beijing"
        dict["Bossuet"] = "shandong"
        dict["MotherPlutarch"] = "hunan"
        dict["Child1"] = "sichuan"
        dict["MmeHucheloup"] = "chongqing"
        dict["Child2"] = "shanxi"
        dict["Enjolras"] = "jiangsu"
        dict["Magnon"] = "beijing"
        dict["MlleVaubois"] = "jiangxi"
        dict["LtGillenormand"] = "chengdu"
        dict["BaronessT"] = "shandong"
        dict["Toussaint"] = "hunan"


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
    edges.append(["Napoleon", "Myriel"])
    edges.append(["MlleBaptistine", "Myriel"])
    edges.append(["MmeMagloire", "Myriel"])
    edges.append(["MmeMagloire", "MlleBaptistine"])
    edges.append(["CountessDeLo", "Myriel"])
    edges.append(["Geborand", "Myriel"])
    edges.append(["Champtercier", "Myriel"])
    edges.append(["Cravatte", "Myriel"])
    edges.append(["Count", "Myriel"])
    edges.append(["OldMan", "Myriel"])
    edges.append(["Valjean", "Labarre"])
    edges.append(["Valjean", "MmeMagloire"])
    edges.append(["Valjean", "MlleBaptistine"])
    edges.append(["Valjean", "Myriel"])
    edges.append(["Marguerite", "Valjean"])
    edges.append(["MmeDeR", "Valjean"])
    edges.append(["Isabeau", "Valjean"])
    edges.append(["Gervais", "Valjean"])
    edges.append(["Listolier", "Tholomyes"])
    edges.append(["Fameuil", "Tholomyes"])
    edges.append(["Fameuil", "Listolier"])
    edges.append(["Blacheville", "Tholomyes"])
    edges.append(["Blacheville", "Listolier"])
    edges.append(["Blacheville", "Fameuil"])
    edges.append(["Favourite", "Tholomyes"])
    edges.append(["Favourite", "Listolier"])
    edges.append(["Favourite", "Fameuil"])
    edges.append(["Favourite", "Blacheville"])
    edges.append(["Dahlia", "Tholomyes"])
    edges.append(["Dahlia", "Listolier"])
    edges.append(["Dahlia", "Fameuil"])
    edges.append(["Dahlia", "Blacheville"])
    edges.append(["Dahlia", "Favourite"])
    edges.append(["Zephine", "Tholomyes"])
    edges.append(["Zephine", "Listolier"])
    edges.append(["Zephine", "Fameuil"])
    edges.append(["Zephine", "Blacheville"])
    edges.append(["Zephine", "Favourite"])
    edges.append(["Zephine", "Dahlia"])
    edges.append(["Fantine", "Tholomyes"])
    edges.append(["Fantine", "Listolier"])
    edges.append(["Fantine", "Fameuil"])
    edges.append(["Fantine", "Blacheville"])
    edges.append(["Fantine", "Favourite"])
    edges.append(["Fantine", "Dahlia"])
    edges.append(["Fantine", "Zephine"])
    edges.append(["Fantine", "Marguerite"])
    edges.append(["Fantine", "Valjean"])
    edges.append(["MmeThenardier", "Fantine"])
    edges.append(["MmeThenardier", "Valjean"])
    edges.append(["Thenardier", "MmeThenardier"])
    edges.append(["Thenardier", "Fantine"])
    edges.append(["Thenardier", "Valjean"])
    edges.append(["Cosette", "MmeThenardier"])
    edges.append(["Cosette", "Valjean"])
    edges.append(["Cosette", "Tholomyes"])
    edges.append(["Cosette", "Thenardier"])
    edges.append(["Javert", "Valjean"])
    edges.append(["Javert", "Fantine"])
    edges.append(["Javert", "Thenardier"])
    edges.append(["Javert", "MmeThenardier"])
    edges.append(["Javert", "Cosette"])
    edges.append(["Fauchelevent", "Valjean"])
    edges.append(["Fauchelevent", "Javert"])
    edges.append(["Bamatabois", "Fantine"])
    edges.append(["Bamatabois", "Javert"])
    edges.append(["Bamatabois", "Valjean"])
    edges.append(["Perpetue", "Fantine"])
    edges.append(["Simplice", "Perpetue"])
    edges.append(["Simplice", "Valjean"])
    edges.append(["Simplice", "Fantine"])
    edges.append(["Simplice", "Javert"])
    edges.append(["Scaufflaire", "Valjean"])
    edges.append(["Woman1", "Valjean"])
    edges.append(["Woman1", "Javert"])
    edges.append(["Judge", "Valjean"])
    edges.append(["Judge", "Bamatabois"])
    edges.append(["Champmathieu", "Valjean"])
    edges.append(["Champmathieu", "Judge"])
    edges.append(["Champmathieu", "Bamatabois"])
    edges.append(["Brevet", "Judge"])
    edges.append(["Brevet", "Champmathieu"])
    edges.append(["Brevet", "Valjean"])
    edges.append(["Brevet", "Bamatabois"])
    edges.append(["Chenildieu", "Judge"])
    edges.append(["Chenildieu", "Champmathieu"])
    edges.append(["Chenildieu", "Brevet"])
    edges.append(["Chenildieu", "Valjean"])
    edges.append(["Chenildieu", "Bamatabois"])
    edges.append(["Cochepaille", "Judge"])
    edges.append(["Cochepaille", "Champmathieu"])
    edges.append(["Cochepaille", "Brevet"])
    edges.append(["Cochepaille", "Chenildieu"])
    edges.append(["Cochepaille", "Valjean"])
    edges.append(["Cochepaille", "Bamatabois"])
    edges.append(["Pontmercy", "Thenardier"])
    edges.append(["Boulatruelle", "Thenardier"])
    edges.append(["Eponine", "MmeThenardier"])
    edges.append(["Eponine", "Thenardier"])
    edges.append(["Anzelma", "Eponine"])
    edges.append(["Anzelma", "Thenardier"])
    edges.append(["Anzelma", "MmeThenardier"])
    edges.append(["Woman2", "Valjean"])
    edges.append(["Woman2", "Cosette"])
    edges.append(["Woman2", "Javert"])
    edges.append(["MotherInnocent", "Fauchelevent"])
    edges.append(["MotherInnocent", "Valjean"])
    edges.append(["Gribier", "Fauchelevent"])
    edges.append(["MmeBurgon", "Jondrette"])
    edges.append(["Gavroche", "MmeBurgon"])
    edges.append(["Gavroche", "Thenardier"])
    edges.append(["Gavroche", "Javert"])
    edges.append(["Gavroche", "Valjean"])
    edges.append(["Gillenormand", "Cosette"])
    edges.append(["Gillenormand", "Valjean"])
    edges.append(["Magnon", "Gillenormand"])
    edges.append(["Magnon", "MmeThenardier"])
    edges.append(["MlleGillenormand", "Gillenormand"])
    edges.append(["MlleGillenormand", "Cosette"])
    edges.append(["MlleGillenormand", "Valjean"])
    edges.append(["MmePontmercy", "MlleGillenormand"])
    edges.append(["MmePontmercy", "Pontmercy"])
    edges.append(["MlleVaubois", "MlleGillenormand"])
    edges.append(["LtGillenormand", "MlleGillenormand"])
    edges.append(["LtGillenormand", "Gillenormand"])
    edges.append(["LtGillenormand", "Cosette"])
    edges.append(["Marius", "MlleGillenormand"])
    edges.append(["Marius", "Gillenormand"])
    edges.append(["Marius", "Pontmercy"])
    edges.append(["Marius", "LtGillenormand"])
    edges.append(["Marius", "Cosette"])
    edges.append(["Marius", "Valjean"])
    edges.append(["Marius", "Tholomyes"])
    edges.append(["Marius", "Thenardier"])
    edges.append(["Marius", "Eponine"])
    edges.append(["Marius", "Gavroche"])
    edges.append(["BaronessT", "Gillenormand"])
    edges.append(["BaronessT", "Marius"])
    edges.append(["Mabeuf", "Marius"])
    edges.append(["Mabeuf", "Eponine"])
    edges.append(["Mabeuf", "Gavroche"])
    edges.append(["Enjolras", "Marius"])
    edges.append(["Enjolras", "Gavroche"])
    edges.append(["Enjolras", "Javert"])
    edges.append(["Enjolras", "Mabeuf"])
    edges.append(["Enjolras", "Valjean"])
    edges.append(["Combeferre", "Enjolras"])
    edges.append(["Combeferre", "Marius"])
    edges.append(["Combeferre", "Gavroche"])
    edges.append(["Combeferre", "Mabeuf"])
    edges.append(["Prouvaire", "Gavroche"])
    edges.append(["Prouvaire", "Enjolras"])
    edges.append(["Prouvaire", "Combeferre"])
    edges.append(["Feuilly", "Gavroche"])
    edges.append(["Feuilly", "Enjolras"])
    edges.append(["Feuilly", "Prouvaire"])
    edges.append(["Feuilly", "Combeferre"])
    edges.append(["Feuilly", "Mabeuf"])
    edges.append(["Feuilly", "Marius"])
    edges.append(["Courfeyrac", "Marius"])
    edges.append(["Courfeyrac", "Enjolras"])
    edges.append(["Courfeyrac", "Combeferre"])
    edges.append(["Courfeyrac", "Gavroche"])
    edges.append(["Courfeyrac", "Mabeuf"])
    edges.append(["Courfeyrac", "Eponine"])
    edges.append(["Courfeyrac", "Feuilly"])
    edges.append(["Courfeyrac", "Prouvaire"])
    edges.append(["Bahorel", "Combeferre"])
    edges.append(["Bahorel", "Gavroche"])
    edges.append(["Bahorel", "Courfeyrac"])
    edges.append(["Bahorel", "Mabeuf"])
    edges.append(["Bahorel", "Enjolras"])
    edges.append(["Bahorel", "Feuilly"])
    edges.append(["Bahorel", "Prouvaire"])
    edges.append(["Bahorel", "Marius"])
    edges.append(["Bossuet", "Marius"])
    edges.append(["Bossuet", "Courfeyrac"])
    edges.append(["Bossuet", "Gavroche"])
    edges.append(["Bossuet", "Bahorel"])
    edges.append(["Bossuet", "Enjolras"])
    edges.append(["Bossuet", "Feuilly"])
    edges.append(["Bossuet", "Prouvaire"])
    edges.append(["Bossuet", "Combeferre"])
    edges.append(["Bossuet", "Mabeuf"])
    edges.append(["Bossuet", "Valjean"])
    edges.append(["Joly", "Bahorel"])
    edges.append(["Joly", "Bossuet"])
    edges.append(["Joly", "Gavroche"])
    edges.append(["Joly", "Courfeyrac"])
    edges.append(["Joly", "Enjolras"])
    edges.append(["Joly", "Feuilly"])
    edges.append(["Joly", "Prouvaire"])
    edges.append(["Joly", "Combeferre"])
    edges.append(["Joly", "Mabeuf"])
    edges.append(["Joly", "Marius"])
    edges.append(["Grantaire", "Bossuet"])
    edges.append(["Grantaire", "Enjolras"])
    edges.append(["Grantaire", "Combeferre"])
    edges.append(["Grantaire", "Courfeyrac"])
    edges.append(["Grantaire", "Joly"])
    edges.append(["Grantaire", "Gavroche"])
    edges.append(["Grantaire", "Bahorel"])
    edges.append(["Grantaire", "Feuilly"])
    edges.append(["Grantaire", "Prouvaire"])
    edges.append(["MotherPlutarch", "Mabeuf"])
    edges.append(["Gueulemer", "Thenardier"])
    edges.append(["Gueulemer", "Valjean"])
    edges.append(["Gueulemer", "MmeThenardier"])
    edges.append(["Gueulemer", "Javert"])
    edges.append(["Gueulemer", "Gavroche"])
    edges.append(["Gueulemer", "Eponine"])
    edges.append(["Babet", "Thenardier"])
    edges.append(["Babet", "Gueulemer"])
    edges.append(["Babet", "Valjean"])
    edges.append(["Babet", "MmeThenardier"])
    edges.append(["Babet", "Javert"])
    edges.append(["Babet", "Gavroche"])
    edges.append(["Babet", "Eponine"])
    edges.append(["Claquesous", "Thenardier"])
    edges.append(["Claquesous", "Babet"])
    edges.append(["Claquesous", "Gueulemer"])
    edges.append(["Claquesous", "Valjean"])
    edges.append(["Claquesous", "MmeThenardier"])
    edges.append(["Claquesous", "Javert"])
    edges.append(["Claquesous", "Eponine"])
    edges.append(["Claquesous", "Enjolras"])
    edges.append(["Montparnasse", "Javert"])
    edges.append(["Montparnasse", "Babet"])
    edges.append(["Montparnasse", "Gueulemer"])
    edges.append(["Montparnasse", "Claquesous"])
    edges.append(["Montparnasse", "Valjean"])
    edges.append(["Montparnasse", "Gavroche"])
    edges.append(["Montparnasse", "Eponine"])
    edges.append(["Montparnasse", "Thenardier"])
    edges.append(["Toussaint", "Cosette"])
    edges.append(["Toussaint", "Javert"])
    edges.append(["Toussaint", "Valjean"])
    edges.append(["Child1", "Gavroche"])
    edges.append(["Child2", "Gavroche"])
    edges.append(["Child2", "Child1"])
    edges.append(["Brujon", "Babet"])
    edges.append(["Brujon", "Gueulemer"])
    edges.append(["Brujon", "Thenardier"])
    edges.append(["Brujon", "Gavroche"])
    edges.append(["Brujon", "Eponine"])
    edges.append(["Brujon", "Claquesous"])
    edges.append(["Brujon", "Montparnasse"])
    edges.append(["MmeHucheloup", "Bossuet"])
    edges.append(["MmeHucheloup", "Joly"])
    edges.append(["MmeHucheloup", "Grantaire"])
    edges.append(["MmeHucheloup", "Bahorel"])
    edges.append(["MmeHucheloup", "Courfeyrac"])
    edges.append(["MmeHucheloup", "Gavroche"])
    edges.append(["MmeHucheloup", "Enjolras"])

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
    rejson.append({"communication": communication})
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