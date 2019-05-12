from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import FileSerializer
from. models import File
from. img_processing import process
import io
import urllib, base64
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
# Create your views here.

def index(request):
  

    Files = File.objects.all().order_by('-id')[:1]
    for a in Files:
      path = a.file.url
      print("=================================!!!!!!!!")
      print(path)
      BnC,imGray,h,s,v,feature,predicted_labels,proba = process(path)
 

    citra=[]
    img=[BnC,imGray]
    for i in img:
      
      plt.imshow(i, interpolation="bilinear", aspect='auto',cmap=plt.cm.gray)
      plt.axis('off')
      fig = plt.gcf()
      buf = io.BytesIO()
      fig.savefig(buf, format='png')
      buf.seek(0)
      string = base64.b64encode(buf.read())
      uri = 'data:image/png;base64,' + urllib.parse.quote(string)
      citra.append(uri)

    img2=[h,s,v]
    for j in img2:
      plt.imshow(j, interpolation="bilinear", aspect='auto')
      plt.axis('off')
      fig = plt.gcf()
      buf = io.BytesIO()
      fig.savefig(buf, format='png')
      buf.seek(0)
      string = base64.b64encode(buf.read())
      uri = 'data:image/png;base64,' + urllib.parse.quote(string)
      citra.append(uri)

    if predicted_labels[0]=='1':
      result='Telinga Kotor'
    else:
      result='Telinga Bersih'
    # Mencari nilai probabilitas
    pro=str(proba)
    split = pro.split(" ")
    prob=[]
    for i in split:
        j=i.replace('[', '')
        m=j.replace(']', '')
        print(m)
        prob.append(m)
    b1=prob[0]
    b2=float(b1)
    bersih=str(round((b2*100),3))
    # print('bersih=',bersih+'%')

    k1=prob[1]
    k2=float(k1)
    kotor=str(round((k2*100),3))
    # print('kotor=',kotor+'%')

    contex = {
        'judul':'About Opang',
        'penulis':'Iya Opang',
        'imge':Files,
        'citra1':citra[0],
        'citra2':citra[1],
        'citra3':citra[2],
        'citra4':citra[3],
        'citra5':citra[4],
        'ciri':feature,
        'hasil':result,
        'probabilitas':[
          ['Bersih',bersih],
          ['Kotor',kotor]
        ]
    }
    return render(request,'deteksi/index.html',contex)


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      print('sukses++++++++++++++++++')
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      print('gagal===================')
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)