from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Stat

import json
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

from django.http import FileResponse
import io

@api_view(['POST'])
def correctRateUpdate(request):
    if request.method == 'POST':
        lastNumber = 6
        data = json.loads(request.body.decode('utf-8'))
        list = data.get('userAnswers', [])
        # 각 문제의 정답수 업데이트
        for id, isCorrect in enumerate(list):
            stat = Stat.objects.get(id = id + 1)
            stat.total += isCorrect
            stat.save()
        # 전체 문제 수
        stat = Stat.objects.get(id=lastNumber)
        stat.total += 1
        stat.save()
        return JsonResponse({"message" : "success"}, status=200)
    return JsonResponse({"message" : "success"}, status=403)

# 원형 그래프
@api_view(['GET'])
def pieGraph(request):
    if request.method == 'GET':
        lastNumber = 6
        input = Stat.objects.get(id=request.data['id'])
        total = Stat.objects.get(id = lastNumber)
        percentage = round((input.total / total.total * 100))
        dataSet = [total.total - input.total, input.total]
        # dataLabels = ['wrong','correct']
        dataColor = ['white', 'palegreen']
        dataExplodes = (0, 0)

        # 글꼴 설정
        font_path = './Stat/SDSamliphopangcheBasic.otf'
        custom_font = FontProperties(fname=font_path, size=10)
        
        plt.switch_backend('Agg')
        # plt.pie(dataSet, labels=dataLabels, colors=dataColor, autopct='%1.0f%%', startangle=90, explode=dataExplodes)
        plt.pie(dataSet, colors=dataColor,  startangle=0, explode=dataExplodes)
        plt.text(0, -1.2, str(percentage) + '%가 이 문제를 맞췄어요!', ha='center', va='center', fontproperties=custom_font, fontsize = 20)

        centerCircle = plt.Circle((0,0),0.45,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centerCircle)

        # 가로세로 비율 동일
        plt.axis('equal')

        flag = 1
        if flag == 1:
            # 이미지 스트림으로 전송
            imgStream = io.BytesIO()
            plt.savefig(imgStream, format='png')
            plt.close()
            # # 이미지 스트림의 시작으로 이동
            imgStream.seek(0)
            return FileResponse(imgStream, content_type='image/png')
        else :
            # 이미지 로컬에 저장
            image_path = './statistics-1.png'
            plt.savefig(image_path)
            plt.close()
            return JsonResponse({"message" : "success"}, status=200)
    return JsonResponse({"message" : "fail"}, status=403)

# 문제별 정답률
@api_view(['GET'])
def correctRate(request):
    if request.method == 'GET':
        dominator = Stat.objects.get(id=6).total
        lastNumber = 6
        list = []
        for i in range(1, lastNumber):
            if (dominator == 0):
                list.append(0)
                continue
            molecule = Stat.objects.get(id = i)
            list.append(round((molecule.total / dominator * 100)))
        return  JsonResponse({"list" : list}, status=200)
    return JsonResponse({"message" : "fail"}, status=403)