# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
import os, sys ,threading, codecs, time, shutil ,random ,datetime ,time
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

# logFile =open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log") ,'w')


#时间戳，12
#状态1标志位：
status1Flag =1
timeStamp ,stampDlt=0 ,0
baseH ,baseM ,baseS1 ,baseS2=11 ,29 ,12 ,23
baseTime =baseH *3600 +baseM *60

###第一出价时间，即为pricestage里的#0 begin时间
expCodeEnd =33
###预览码结束时间数,小于最早第一出价时间即可
expEndTime =31
###是否实战，实战或实战模拟当天设为1，平时为0
isFight =1

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

#8,10,16,26,28

###########################################################
###此处的开始时间已经不再重要，只是判断对应的第一还是第二次出价
priceStage=['33-40.0-400',                     #0
            '45-55.5-900',                     #1----(16-0)
            '45-56.0-1000',                    #2----(24-0)
            '45-56.2-700',                     #3----
            '45-56.5-700',                     #4----(18-0)
            '45-56.0-800',                     #5!---(5-0)(19-0)
            '45-56.5-800',                     #6!---(2-0)(11-0)
            '45-56.0-900',                     #7----(28-0)(10-0)
            '45-56.5-900',                     #8!---(4-0)(13-0)(30-0)
            '48-56.2-600',                     #9!---(29-0)(23-2-2:3)
            '48-56.6-600',                     #10---(7-0)
            '48-56.2-700',                     #11---(8-0)
            '48-56.6-700',                     #12!!-(9-0)(12-0)(15-0)
            '49-56.5-500',                     #13---(26-0)(25-2-2:1)
            '50-56.5-500',                     #14---(14-0)(22-1-2:1)
            '49-56.2-600',                     #15!--(6-0)(3-2-2:0)
            '49-56.6-600',                     #16---(27-0)
            '49-56.2-700',                     #17---(21-0)
            '49-56.5-700',                     #18!!-(1-0)(20-0)
            '49-56.5-400']                     #(31-0)(17-0)

curVersion =0
expPhotoList = []
drillList =[]
#当前打码状态：0，未开始 1，开始倒计时 2，预览码 3第一码 4第二码
idDict ={}#{id:[[预览图url],(第一码)[url,{user:[码，时间]}],(第二码)[url,{user:[码，时间]}]],当前打码状态,第一码起始时间,4状态附加码}
authDict ={}#{'qc01':'362229198511230013' ,'qc02':'362229198511230013'}
chepaiDict ={}#{'qc01':'chepaiguo1' ,'qc02':'chepaiguo2'}
hostDict ={}#{'chepaiguo1' :['522101196702217638', '53833982', '4058', '39-45-500', '48-55.5-700']}

codeMonth ='2018_08'
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
            line =line.replace(' ' ,'')
            subList =line.strip().split(',')
            hostDict[subList[4]] =[subList[0] ,subList[1] ,subList[2] ,priceStage[0] ,priceStage[int(subList[5])] ,priceStage[int(subList[6])] ,subList[7] ,subList[8]]
            purl ='static/codePic'
            purl =os.path.join(purl ,codeMonth)
            url0 =os.path.join(purl ,subList[0] + '_' +'0.png')
            url1 =os.path.join(purl ,subList[0] + '_' +'1.png')
            # url2 =os.path.join(purl ,subList[0] + '_' +'2.png')
            url2 =os.path.join(purl ,subList[0] + '_2_0.png')
            idDict[subList[0]] =[[url0] ,[url1 ,{}], [url2 ,{}] ,0 ,expCodeEnd ,0]
            #authDict
            authList =subList[3].split('-')
            for user in authList:
                authDict[user] =subList[0]
            #chepaiDict
            for user in authList:
                chepaiDict[user] =subList[4]
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
        if username in authDict:
            print(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +chepaiDict[username] +'---' +username +'---' +'login')
        # logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +chepaiDict[username] +'---' +username +'---' +'login' +'\n')
        # logFile.flush()
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
def getClock(request):
    ret ='-'
    if isFight:
        ret =str(int(time.time()))
    return HttpResponse(ret)

@login_required(login_url='login')
def getrsptime(request):
    usr = request.user.username
    times = request.GET['times']
    print(usr +'---' +'rsptime : ' + times +'ms')
    # logFile.write(usr +'---' +'rsptime : ' + times +'ms\n')
    # logFile.flush()
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
    ret =expPhotoList[random.randint(0 ,99)]
    return HttpResponse(ret)

@login_required(login_url='login')
def finjob(request):
    usr = request.user.username
    total = request.POST['total']
    print(str(datetime.datetime.now()) +'---' +usr +'---finjob' +'---' +'total:' +total)
    # logFile.write(str(datetime.datetime.now()) +'---' +usr +'---finjob' +'---' +'total:' +total+'\n')
    # logFile.flush()

#drill
@login_required(login_url='login')
def drill(request):
    return render(request, 'polls/drill.html')

@login_required(login_url='login')
def getDrillInfo(request):
    ret =drillList[random.randint(0 ,10)]
    return HttpResponse(ret)

###fight
@login_required(login_url='login')
def fight(request):
    return render(request, 'polls/fightW.html')


def stream_generator(usr):
    global timeStamp
    theStatus =0
    #因为第二码第一次来即设置为1了,所以此处初始值为1
    secondStatus =1
    sleepTime =2
    oldTime =time.time()
    #新建连接，发送成功通知
    print('new channel.')
    yield u'data: 0-ok\n\n'
    while True:
        newTime =time.time()
        if newTime -oldTime >2:
            yield u'data: 0-heartbeat\n\n'
            oldTime =newTime
        theList =idDict[authDict[usr]]
        ret =''
        #1:倒计时数
        if theList[3] ==1:
            if theStatus !=1:
                theStatus =1
                sleepTime =0.3
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
                    if timeStamp >expEndTime:
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
            else:
                if secondStatus !=theList[5]:
                    secondStatus =theList[5]
                    ret ='4-' +theList[2][0]
                    print('status change---' +str(secondStatus) +'---' +theList[2][0])
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
    # print(datetime.datetime.now())
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
    if usr in authDict:
        print(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +chepaiDict[usr] +'---' +usr +'---setCode:' +code +'---to:' +authDict[usr] +'---times:' +times)
    # logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +chepaiDict[usr] +'---' +usr +'---setCode:' +code +'---to:' +authDict[usr] +'---times:' +times +'\n')
    # logFile.flush()

##########################################################################

def uploadPic(request):
    # print(datetime.datetime.now())
    if request.method == 'POST':
        lock.acquire()
        try:
            idt =request.POST['idt']
            times =int(request.POST['times'])
            pic =request.FILES['file']
            purl =idDict[idt][times][0]
            if times ==2:
                #初始为0，第一次过来即设置为1,即2_1.png
                idDict[idt][5] +=1
                purl =purl[:-5] +str(idDict[idt][5]) +'.png'
                idDict[idt][times][0] =purl
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            BASE_DIR =os.path.join(BASE_DIR ,purl)
            with open(BASE_DIR, 'wb+') as destination:
                for chunk in pic.chunks():
                    destination.write(chunk)
            idDict[idt][3] =times +2
            print(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +request.POST['hostName'] +'---uploadpic' +'---to:' +idDict[idt][times][0])
            # logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +request.POST['hostName'] +'---uploadpic' +'---to:' +idDict[idt][times][0]+'\n')
            # logFile.flush()
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
        print(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +request.GET['hostName'] +'---id:' +idt +'---getcodes:' +codesStr +'---finalcode:' +codeDict[-1][0])
        # logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +request.GET['hostName'] +'---id:' +idt +'---getcodes:' +codesStr +'---finalcode:' +codeDict[-1][0]+'\n')
        # logFile.flush()
        return HttpResponse(codeDict[-1][0])
    else:
        print(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +request.GET['hostName'] +'---id:' +idt +'---getnothing')
        # logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'---' +request.GET['hostName'] +'---id:' +idt +'---getnothing'+'\n')
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
    #print(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'------changeversion to:' +str(curVersion))
    # logFile.write(str(datetime.datetime.now()) +'---' +'timeStame:' +str(timeStamp) +'------changeversion to:' +str(curVersion)+'\n')
    # logFile.flush()
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
