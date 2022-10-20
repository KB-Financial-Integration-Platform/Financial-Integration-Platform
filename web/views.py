from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import User, Consume, Saving, Card
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login
from web.forms import UserForm

import numpy as np
import pandas as pd
import math


from django.views.decorators.csrf import csrf_exempt

아파트_종류 = pd.read_csv('web/real_estate/아파트_종류_단지명포함.csv',encoding='utf8')
아파트 = pd.read_csv('web/real_estate/아파트_전처리_단지명포함.csv',encoding='utf8')
아파트25 = pd.read_csv('web/real_estate/아파트_2025_단지명포함.csv',encoding='cp949')


def index(request):
    return render(request,'../templates/index.html')

def home(request):
    return render(request,'../templates/Home.html')

def login(request):
    return render(request,'../templates/로그인.html')

def 소비(request):
    user_id = request.user.id
    my_info = Consume.objects.filter(username=user_id)
    return render(request,'../templates/마이_개인소비성향.html', {'my_info':my_info})

def 적금카드(request):
    user_age = request.user.age
    save_info = Saving.objects.filter(age=user_age)
    card_info = Card.objects.filter(age=user_age)
    return render(request,'../templates/적금카드.html', {'save_info':save_info, 'card_info':card_info})

def 주거(request):
    hope_address_s = request.user.hope_address.split(" ")

    #가용자산범위 안에 있는 아파트 추출
    best_process_1 = 아파트_종류[아파트_종류["거래금액(만원)"] <= int(request.user.available_asset)]

    #가용자산범위 안의 희망 동 추출
    best_process_2 = best_process_1[best_process_1["동"] == hope_address_s[2]]
    best_process_2 = best_process_2.rename(columns={'거래금액(만원)':'거래금액'})
    best_process_2 = best_process_2.groupby("단지명").mean().reset_index()
    
    best_process_2['구'] = hope_address_s[1]
    best_process_2['동'] = hope_address_s[2]
    best_process_2['거래금액'] = best_process_2['거래금액'].astype('int')
    best_process_2['억'] = best_process_2['거래금액'] // 10000
    best_process_2['거래금액'] = best_process_2['거래금액'] % 10000
    best_process_2['층'] = best_process_2['층'].astype('int')
    best_process_2['평'] = best_process_2['평'].astype('int')

    if best_process_2.empty :
        best_1 = '이 가격으로는 집을 구매하실수 없습니다'
        best_2 = '이 가격으로는 집을 구매하실수 없습니다'
        best_3 = '이 가격으로는 집을 구매하실수 없습니다'
    elif request.user.child == '있음':
        best_process_2 = best_process_2.sort_values("평", ascending=False)
        best_1 = best_process_2.iloc[0]
        best_2 = best_process_2.iloc[1]
        best_3 = best_process_2.iloc[2]
    else :
        #제일 싼집 순으로
        best_process_2 = best_process_2.sort_values("거래금액")
        best_1 = best_process_2.iloc[0]
        best_2 = best_process_2.iloc[1]
        best_3 = best_process_2.iloc[2]

    return render(request,'../templates/부동산_맞춤주거지역.html', {'best_1':best_1, 'best_2':best_2, 'best_3':best_3})

def ranges_0(list):
    return range(0, len(list)-1)
    
def pick_data_1(list, i, j):
    return list[i+1][j]

# csrf token을 확인하지 않는 장식자
@csrf_exempt
def 실거래가(request):    

    if request.method == 'POST':
        apt = request.POST['keyword']
        apt_list = 아파트[아파트['단지명']==str(apt)][-10:]
        apt_list = apt_list.rename(columns={'거래금액(만원)':'거래금액'})

        apt25 = 아파트25[아파트25['단지명']==str(apt)]['0'].mean().astype('int')
        apt25억 = apt25// 10000
        apt25가격 = apt25 % 10000
        
        
        return render(request, '../templates/부동산_실거래가조회.html', {"apt":apt,"apt_list": apt_list, "apt25억":apt25억,"apt25가격":apt25가격})
    else:
        return render(request, '../templates/부동산_실거래가조회.html')


def 부동산(request):
    return render(request,'../templates/부동산.html')
def 설명회(request):
    return render(request,'../templates/설명회정보.html')
def 주식(request):
    return render(request,'../templates/주식.html')


# 로그인
@csrf_exempt
def login(request):
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)
        
        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, '../templates/로그인.html', {'error' : '아이디 또는 비밀번호가 일치하지 않습니다.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, '../templates/로그인.html')

# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, '../templates/로그인.html')


def 회원가입(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, '../templates/회원가입.html', {'form': form})