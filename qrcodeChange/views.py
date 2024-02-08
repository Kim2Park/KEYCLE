from django.shortcuts import render

# Create your views here.
# views.py
from django.http import FileResponse,HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from pathlib import Path
import qrcode

from io import BytesIO
import boto3

AWS_ACCESS_KEY_ID ='AKIA6GBMDV7N4SDX5IGP'
AWS_SECRET_ACCESS_KEY = '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'
AWS_DEFAULT_REGION = 'ap-northeast-2'

@csrf_exempt #forbidden csrf cookie not set이 뜬다
def generate_qrcode(request):
    if request.method == 'POST':
        if 'file' not in request.FILES: #파일받아오기!
            return HttpResponse('No file part')
        file = request.FILES['file']
        file_name = file.name
        print(file_name) #이름뽑아오기
        #이미지 임시저장 테스트
        img = Image.open(file)
        current_path = Path(__file__).parent
        img_path = current_path / 'kioskImg' / file_name
        img.save(img_path) 
        #s3클라이언트 생성
        s3 = boto3.client(
                service_name='s3',
                region_name=AWS_DEFAULT_REGION,
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            )
        try: 
            s3.upload_file(img_path,"kioskphotoimage",file_name)
        except Exception as e : print(e)
        imagesUrl = 'https://kioskphotoimage.s3.ap-northeast-2.amazonaws.com/'+file_name
        images = qrcode.make(imagesUrl)
        img_path = current_path / 'kioskImg'/'QR.jpg'
        images.save(img_path)
        #이미지 합성하기 코드 *짜야함*

        byte_io = BytesIO()
        # images.save(byte_io, 'PNG')
        byte_io = byte_io.getvalue()
        #이미지 리턴해주기
        return HttpResponse(byte_io, content_type='image/png')
        # return FileResponse(byte_io, as_attachment=True, filename='qrcode.png')
