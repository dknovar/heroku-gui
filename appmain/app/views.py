from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    contex={
        'judul':'homepage ne',
        'penulis':'opang',
        'banner':'img/jalan2.jpg',
        'nav':[
            ['/','Home'],
            ['/about','About'],
            ['/login','Login'],
            ['/deteksi','Deteksi']
        ]
    }
    return render(request,'index.html',contex)

def angka (request,input):
    heading = "<h1> Page Angka </h1>"
    str = heading + input
    return HttpResponse(str)

def date(request,tahun,bulan):
    heading = "<h1> Page Angka </h1>"
    strTahun = "Tahun : "+tahun
    strBulan = "Bulan : "+bulan
    str = strTahun + "<br>" +strBulan 
    return HttpResponse(str)