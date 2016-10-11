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
        time.sleep(0.1)

t= threading.Thread(target=makeTimeStamp)
t.start()

###########################################################

expPhotoList = []
#0：id
#1：文件路径
#2：时间戳
#3：发码时间
#4：解码时间
#5：code
idDict ={'0001':['test1',0,0,0,0,'0'] ,'0002':['test2',0,0,0,0,'0']}
authDict ={'test1':'0001' ,'test2':'0002'}
codeMonth ='2016_09'
lock = threading.Lock()


###初始化测试列表
with codecs.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/exp/answer"), 'r','utf-8') as f:
    theList = f.readlines()
    for line in theList:
        expPhotoList.append(line.strip())



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


def train(request):
    return render(request, 'polls/trainW.html')


def fight(request):
    return render(request, 'polls/fightW.html')


def getTrainPhoto(request):
    ret =expPhotoList[random.randint(0 ,49)]
    return HttpResponse(ret)

def uploadPic(request):
    print(datetime.datetime.now())
    if request.method == 'POST':
        idt =request.POST['idt']
        pic =request.FILES['file']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        purl ='static/codePic'
        purl =os.path.join(purl ,codeMonth)
        purl =os.path.join(purl ,idt +'.png')
        BASE_DIR =os.path.join(BASE_DIR ,purl)
        with open(BASE_DIR, 'wb+') as destination:
            for chunk in pic.chunks():
                destination.write(chunk)
        lock.acquire()
        try:
            idDict[idt][1] =purl
        finally:
            lock.release()
    print(datetime.datetime.now())

#0:是否已倒计时
#1:时间戳
#2:文件路径
#3:身份证号
def getCodeImg(request):
    usr = request.user.username
    theList =idDict[authDict[usr]]
    ret =''
    if theList[1] !=0:
        ret ='1--' +theList[1] +'-' +authDict[usr]
        print(datetime.datetime.now())
    else:
        if int(theList[2]) >0:
            ret ='1-' +str(theList[2]) +'-'
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

def gettest(request):
    return HttpResponse(1)

def gettesttime(request):
    theT =str(time.time())
    print(theT)
    return HttpResponse(theT)
