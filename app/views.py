from app.models import *
from django.shortcuts import render,redirect
from django.http  import HttpResponse
import feedparser
def clearArticles(request):
    CovidContent.objects.all().delete()
    return redirect('/')
def clearLinks(request):
    CovidContentLink.objects.all().delete()
    return redirect('/')


# Create your views here.
def updatecovid(request):
    #-------python----------------
    links=CovidContentLink.objects.all()
    for link in links:
        url = feedparser.parse(
               str(link.url)
            )
        for i in range(len(url.entries)):
            info = url.entries[i]
            content= CovidContent()
            content.headline= info.title
            desc = info.description
            start=desc.find("img src=")
            end=desc.find("width")
            desc=desc[start+9:end-2:]
    
            #---------------
            content.img = desc
            content.url  = info.link
            isCreated = CovidContent.objects.get_or_create(img=content.img,headline=content.headline, url=content.url)
            # content.save()
    return redirect('/')

def covidContentLinks(request):
    covidContentLinks = CovidContentLink.objects.all()
    context = { 
        'links': covidContentLinks,
    }
    return render(request,'addsource.html',context)

def addcovidsource(request):
    print("request",request.POST.get('weblink'))
    isCreated = CovidContentLink.objects.get_or_create(url= request.POST.get('weblink'))
    return redirect('/covidContentLinks')

def home(request):
    covidcontent = CovidContent.objects.all()
    context = { 
        'covidcontent': covidcontent,
    }
    return render(request,'home.html',context)