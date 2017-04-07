# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
import os, sys ,threading, codecs, time, shutil ,random ,datetime
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib import auth
from django.contrib.auth.models import User
from polls.models import Picture
from django.http import FileResponse
from django.conf import settings

logFile =open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log") ,'w')


#时间戳，12
#状态1标志位：
status1Flag =1
timeStamp ,stampDlt=0 ,0
baseH ,baseM ,baseS1 ,baseS2=11 ,29 ,12 ,23
baseTime =baseH *3600 +baseM *60

def makeTimeStamp():
    global timeStamp ,stampDlt ,status1Flag ,idDict
    while 1:
        now =datetime.datetime.now()
        theH =int(now.strftime('%H'))
        theM =int(now.strftime('%M'))
        theS =int(now.strftime('%S'))
        theStamp =theH *3600 +theM *60 +theS -baseTime +int(now.strftime('%f')[:2]) /100 -stampDlt
        theStamp =round(theStamp ,2)
        if 0 <theStamp <60:
            timeStamp =theStamp
            if status1Flag:
                for key in idDict:
                    idDict[key][3] =1
                status1Flag =0
        if timeStamp >59:
            #写入数据库
            pass
        time.sleep(0.1)

t= threading.Thread(target=makeTimeStamp)
t.start()

###########################################################
priceStage=['37-43.0-500',                    #0
            '46-54.0-800',                    #1
            '46-54.5-800',                    #2
            '46-54.5-900',                    #3
            '46-55.0-800',                    #4
            '46-55.0-900',                    #5
            '46-55.5-800',                    #6
            '46-55.5-900',                    #7
            '46-56.0-900',                    #8
            '46-56.0-1000',                   #9
            '46-54.5-400']                    #10

curVersion =0
expPhotoList = []
drillList =[]
#当前打码状态：0，未开始 1，开始倒计时 2，预览码 3第一码 4第二码
idDict ={}#{id:[[预览图url],(第一码)[url,{user:[码，时间]}],(第二码)[url,{user:[码，时间]}]],当前打码状态}
authDict ={}#{'test':'362229198511230013' ,'test2':'0002'}
hostDict ={}#{'chepaiguo1' :['522101196702217638', '53833982', '4058', '39-45-500', '48-55.5-700']}

codeMonth ='2017_04'
lock = threading.Lock()

def init():
    print('--------------------------------------------init----------------------------------')
    ###初始化测试列表
    with codecs.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/exp/answer"), 'r','utf-8') as f:
        theList = f.readlines()
        for line in theList:
            expPhotoList.append(line.strip())

    ###初始化drill列表
    with codecs.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/exp/drillInfo"), 'r','utf-8') as f:
        theList = f.readlines()
        for line in theList:
            drillList.append(line.strip())

    ###初始化info相关dict
    theUrl =os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/info/" +codeMonth)
    with codecs.open(theUrl, 'r','utf-8') as f:
        theList = f.readlines()
        for line in theList:
            subList =line.strip().split(',')
            hostDict[subList[4]] =[subList[0] ,subList[1] ,subList[2] ,priceStage[0] ,priceStage[int(subList[5])] ,subList[6]]
            purl ='static/codePic'
            purl =os.path.join(purl ,codeMonth)
            url0 =os.path.join(purl ,subList[0] + '_' +'0.png')
            url1 =os.path.join(purl ,subList[0] + '_' +'1.png')
            url2 =os.path.join(purl ,subList[0] + '_' +'2.png')
            idDict[subList[0]] =[[url0] ,[url1 ,{}], [url2 ,{}] ,0 ,37]
            #authDict
            authList =subList[3].split('-')
            for user in authList:
                authDict[user] =subList[0]
            #idDict
                idDict[subList[0]][1][1][user] =['0' ,'0']
                idDict[subList[0]][2][1][user] =['0' ,'0']

    i =0

init()

##############################################################################
#@ensure_csrf_cookie
def login(request):
    return render(request, 'polls/login.html')


#@csrf_protect
def dologin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user:
        # request.session['user_id'] =user.id
        auth.login(request, user)
        logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +username +'---' +'login' +'\n')
        logFile.flush()
        return HttpResponseRedirect('mainpage')
        # return HttpResponse("hello")
    else:
        return HttpResponse("用户名或密码错误")

@login_required(login_url='login')
def getusrname(request):
    usr = request.user.username
    if timeStamp >59:
        usr ='刷新过，已失效'
    return HttpResponse(usr)

@login_required(login_url='login')
def getrsptime(request):
    usr = request.user.username
    times = request.GET['times']
    logFile.write(usr +'---' +'rsptime : ' + times +'ms\n')
    logFile.flush()
    return HttpResponse('ok')


@login_required(login_url='login')
def mainpage(request):
    return render(request, 'polls/mainpage.html')
    # if request.user.is_authenticated():
    #     return render(request, 'polls/mainpage.html')
    # else:
    #     return render(request, 'polls/login.html')


###train
@login_required(login_url='login')
def train(request):
    return render(request, 'polls/trainW.html')

@login_required(login_url='login')
def getTrainPhoto(request):
    ret =expPhotoList[random.randint(0 ,69)]
    return HttpResponse(ret)

@login_required(login_url='login')
def finjob(request):
    usr = request.user.username
    total = request.POST['total']
    logFile.write(str(datetime.datetime.now()) +'---' +usr +'---finjob' +'---' +'total:' +total+'\n')
    logFile.flush()

#drill
@login_required(login_url='login')
def drill(request):
    return render(request, 'polls/drill.html')

@login_required(login_url='login')
def getDrillInfo(request):
    ret =drillList[random.randint(0 ,8)]
    return HttpResponse(ret)

###fight
@login_required(login_url='login')
def fight(request):
    return render(request, 'polls/fightW.html')


def stream_generator(usr):
    global timeStamp
    theStatus =0
    sleepTime =3
    ###预览码结束时间数,小于最早第一出价时间即可
    expCodeEnd =35
    while True:
        theList =idDict[authDict[usr]]
        ret =''
        # if timeStamp >59:
        #     if theStatus ==5:
        #         continue
        #1:倒计时数
        if theList[3] ==1:
            if theStatus !=1:
                theStatus =1
                sleepTime =0.5
            if timeStamp >0:
                if theList[4] -int(timeStamp) >0:
                    ret ='1-' +str(theList[4] -int(timeStamp))
        #1:倒计时数,2:文件路径
        if theList[3] ==2:
            if theStatus !=2:
                theStatus =2
            if timeStamp >0:
                if theList[4] -int(timeStamp) >0:
                    ret ='2-' +str(theList[4] -int(timeStamp)) +'-' +theList[0][0]
                    if timeStamp >expCodeEnd:
                        ret ='2-' +str(theList[4] -int(timeStamp))
                        sleepTime =0.1
        #1:文件路径
        if theList[3] ==3:
            if theStatus !=3:
                theStatus =3
                ret ='3-' +theList[1][0]
        if theList[3] ==4:
            if theStatus !=4:
                theStatus =4
                ret ='4-' +theList[2][0]
        if timeStamp >59:
            if theStatus ==4:
                theStatus =5
                sleepTime =100000
                print('end')
                ret ='5'
        if ret !='':
            yield u'data: %s\n\n' % ret
        time.sleep(sleepTime)

@login_required(login_url='login')
def getStatus(request):
    usr = request.user.username
    if usr in authDict:
        response = StreamingHttpResponse(stream_generator(usr), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response
    else:
        return HttpResponse('wrong!')


#根据状态码决定是哪个码
@login_required(login_url='login')
def setCode(request):
    print(datetime.datetime.now())
    usr = request.user.username
    if usr not in authDict:
        return HttpResponse('wrong!')
    lock.acquire()
    try:
        theList =idDict[authDict[usr]]
        whichCode =theList[theList[3] -2][1]
        code = request.POST['code']
        times = request.POST['times']
        whichCode[usr][0] =code
        whichCode[usr][1] =times
    finally:
        lock.release()
    logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +usr +'---setCode:' +code +'---to:' +authDict[usr] +'---times:' +times +'\n')
    logFile.flush()

##########################################################################

def uploadPic(request):
    # print(datetime.datetime.now())
    if request.method == 'POST':
        idt =request.POST['idt']
        times =int(request.POST['times'])
        pic =request.FILES['file']
        purl =idDict[idt][times][0]
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BASE_DIR =os.path.join(BASE_DIR ,purl)
        lock.acquire()
        try:
            with open(BASE_DIR, 'wb+') as destination:
                for chunk in pic.chunks():
                    destination.write(chunk)
            idDict[idt][3] =times +2
            logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---uploadpic' +'---' +idDict[idt][times][0]+'\n')
            logFile.flush()
        finally:
            lock.release()


#根据本端状态码决定是哪个码
def getTrueCode(request):
    idt = request.GET['idt']
    theList =idDict[idt]
    theDict =theList[theList[3] -2][1]
    codeDict ={}
    codesStr ='('
    for k in theDict:
        theCode =theDict[k][0]
        codesStr +=theCode
        codesStr +=','
        ###写死部分，设定验证码长度为4
        # if theCode !='0' and len(theCode) ==4:
        if theCode !='0':
            if theCode in codeDict:
                codeDict[theCode] +=1
            else:
                codeDict[theCode] =1
    codesStr +=')'
    if len(codeDict) >0:
        codeDict = sorted(codeDict.items(), key=lambda dic: dic[1])
        logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---id:' +idt +'---codes:' +codesStr +'---finalcode:' +codeDict[-1][0]+'\n')
        logFile.flush()
        return HttpResponse(codeDict[-1][0])
    else:
        logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---id:' +idt +'---getnothing'+'\n')
        return HttpResponse('')

def setTimeStamp(request):
    global stampDlt
    times = request.GET['times']
    now =datetime.datetime.now()
    if times =='1':
        stampDlt =int(now.strftime('%H')) *3600 +int(now.strftime('%M')) *60 +int(now.strftime('%S')) +int(now.strftime('%f')[:2]) /100 -baseTime -baseS1
        stampDlt =round(stampDlt ,2)
    if times =='2':
        stampDlt =int(now.strftime('%H')) *3600 +int(now.strftime('%M')) *60 +int(now.strftime('%S')) +int(now.strftime('%f')[:2]) /100 -baseTime -baseS2
        stampDlt =round(stampDlt ,2)
    print(stampDlt)

# def time_generator():
#     global timeStamp
#     theStamp =0
#     while True:
#         if timeStamp !=theStamp:
#             theStamp =timeStamp
#             yield u'data: %s\n\n' % str(timeStamp)
#         time.sleep(0.1)
#
# def getTimeStamp(request):
#     response = StreamingHttpResponse(time_generator(), content_type="text/event-stream")
#     response['Cache-Control'] = 'no-cache'
#     return response

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
    logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'------changeversion to:' +str(curVersion)+'\n')
    logFile.flush()
    return HttpResponse('ok!')


def getOrderInfo(request):
    hostname = request.GET['hostname']
    return HttpResponse('~'.join(hostDict[hostname]))



###测试部分
def gettest(request):
    return HttpResponse(1)

def gettesttime(request):
    theT =str(time.time())
    print(theT)
    return HttpResponse(theT)
