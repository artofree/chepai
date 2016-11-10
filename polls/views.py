# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
import os, threading, codecs, time, shutil ,random ,datetime

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.contrib import auth
from django.contrib.auth.models import User
from polls.models import Picture
from django.http import FileResponse

#时间戳，12
timeStamp ,stampDlt=0 ,0
baseH ,baseM ,baseS=11 ,29 ,23
baseTime =baseH *3600 +baseM *60

def makeTimeStamp():
    global timeStamp
    while 1:
        now =datetime.datetime.now()
        theH =int(now.strftime('%H'))
        theM =int(now.strftime('%M'))
        theS =int(now.strftime('%S'))
        theStamp =theH *3600 +theM *60 +theS -baseTime +int(now.strftime('%f')[:2]) /100 -stampDlt
        theStamp =round(theStamp ,2)
        if 0 <theStamp <60:
            timeStamp =theStamp
        else:
            #写入数据库
            pass
        time.sleep(0.1)

t= threading.Thread(target=makeTimeStamp)
t.start()

###########################################################
curVersion =0
expPhotoList = []
#0：打码id
#1：文件路径
#2：第几个码
#3：发码时间（暂无用）
#4：解码时间（暂无用）
#5：code
idDict ={'362229198511230013':['test',0,0,0,0,'0'] ,'0002':['test2',0,0,0,0,'0']}
authDict ={'test':'362229198511230013' ,'test2':'0002'}
hostDict ={'newguo' :['53689363' ,'7570' ,'362229198511230013']}
codeMonth ='2016_11'
lock = threading.Lock()


###初始化测试列表
with codecs.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/exp/answer"), 'r','utf-8') as f:
    theList = f.readlines()
    for line in theList:
        expPhotoList.append(line.strip())


##############################################################################
def login(request):
    return render(request, 'polls/login.html')


def dologin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user:
        # request.session['user_id'] =user.id
        auth.login(request, user)
        return HttpResponseRedirect('mainpage')
        # return HttpResponse("hello")
    else:
        return HttpResponse("用户名或密码错误")


def mainpage(request):
    if request.user.is_authenticated():
        return render(request, 'polls/mainpage.html')
    else:
        return render(request, 'polls/login.html')


###train
def train(request):
    return render(request, 'polls/trainW.html')

def getTrainPhoto(request):
    ret =expPhotoList[random.randint(0 ,49)]
    return HttpResponse(ret)


###fight
def fight(request):
    return render(request, 'polls/fightW.html')


#0:是否已倒计时
#1:时间戳
#2:文件路径
#3:身份证号
def getCodeImg(request):
    global timeStamp
    usr = request.user.username
    theList =idDict[authDict[usr]]
    ret =''
    if theList[1] !=0:
        ret ='1--' +theList[1] +'-' +authDict[usr]
        theList[1] =0
    else:
        if theList[2] ==0:
            if timeStamp >0:
                if 37 -int(timeStamp) >0:
                    ret ='1-' +str(37 -int(timeStamp)) +'-'
                else:
                    ret ='1-' +'0' +'-'
            else:
                ret ='0--'
    return HttpResponse(ret)



def setCode(request):
    idt = request.POST['idt']
    code = request.POST['code']
    lock.acquire()
    try:
        idDict[idt][5] =code
    finally:
        lock.release()

##########################################################################

def uploadPic(request):
    print(datetime.datetime.now())
    if request.method == 'POST':
        idt =request.POST['idt']
        times =request.POST['times']
        pic =request.FILES['file']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        purl ='static/codePic'
        purl =os.path.join(purl ,codeMonth)
        purl =os.path.join(purl ,idt + '_' +times +'.png')
        BASE_DIR =os.path.join(BASE_DIR ,purl)
        with open(BASE_DIR, 'wb+') as destination:
            for chunk in pic.chunks():
                destination.write(chunk)
        lock.acquire()
        try:
            idDict[idt][1] =purl
            if idDict[idt][2] ==0:
                idDict[idt][2] =1
            else:
                idDict[idt][2] =2
        finally:
            lock.release()
    print(datetime.datetime.now())



def getCode(request):
    idt = request.GET['idt']
    return HttpResponse(idDict[idt][5])

def setTimeStamp(request):
    global stampDlt
    now =datetime.datetime.now()
    stampDlt =int(now.strftime('%H')) *3600 +int(now.strftime('%M')) *60 +int(now.strftime('%S')) +int(now.strftime('%f')[:2]) /100 -baseTime -baseS
    stampDlt =round(stampDlt ,2)
    print(stampDlt)

def getTimeStamp(request):
    global timeStamp
    return HttpResponse(timeStamp)

def getVersion(request):
    global curVersion
    return HttpResponse(curVersion)

def getVersionContent(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    purl ='static/verFile'
    BASE_DIR =os.path.join(BASE_DIR ,purl)
    response = FileResponse(open(BASE_DIR, 'rb'))
    return response

def setVersionContent(request):
    global curVersion
    verFile =request.FILES['file']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    purl ='static/verFile'
    BASE_DIR =os.path.join(BASE_DIR ,purl)
    with open(BASE_DIR, 'wb+') as destination:
        for chunk in verFile.chunks():
            destination.write(chunk)
    curVersion +=1
    return HttpResponse('ok!')


def getOrderInfo(request):
    hostname = request.GET['hostname']
    return HttpResponse('-'.join(hostDict[hostname]))

###测试部分
def gettest(request):
    return HttpResponse(1)

def gettesttime(request):
    theT =str(time.time())
    print(theT)
    return HttpResponse(theT)
