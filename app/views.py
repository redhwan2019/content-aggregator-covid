from app.models import *
from django.shortcuts import render,redirect
from django.http  import HttpResponse
import requests
from readability import Document
from bs4 import BeautifulSoup
import re
import uuid

from urllib.parse import urlparse, urljoin


regex = re.compile('<header>(.+)</header>')



def clearArticles(request):
    CovidContent.objects.all().delete()
    return redirect('/')
def clearLinks(request):
    CovidContentLink.objects.all().delete()
    return redirect('/')


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Create your views here.
def updatecovid(request):
    #-------python----------------
    links=CovidContentLink.objects.all()
    for link in links:
        reqs = requests.get(link.url)
        content = reqs.text
        headers = re.findall('<header(.*?)>(.*?)</header>',content,re.DOTALL)
        # print(headers[0])
        # return redirect("/")
        for header in headers:
            if header:
                content = content.replace(str(header),"")
        soup = BeautifulSoup(content, 'html.parser')
        for href in soup.find_all('a'):
            href=href['href']
            if(not str(href).startswith(urlparse(link.url).scheme) and "?" not in str(href) ):
                print("href",href)
                base= urlparse(link.url).scheme+"://"+urlparse(link.url).hostname
                fullpath = base+href
                # print("test ",fullpath)
                article = requests.get(fullpath).text
                articleparsed= Document(article)
                soup = BeautifulSoup(str(article), 'html.parser')
                img = str(soup.find_all('img')[0]['src'])
                if img and not img.startswith("http"):
                    img = base+img
                dateIndex =article.find("datePublished")
                if dateIndex is not -1:
                    commaIndex =article.find(",",dateIndex+14,len(article))
                    date = article[dateIndex+16:commaIndex-1]    
                    isCreated = CovidContent.objects.get_or_create(img=img,date=date,headline=articleparsed.title(), url=fullpath)
    return redirect('/')


def addcovidsource(request):
    if request.method == 'GET':
        covidContentLinks = CovidContentLink.objects.all()
        context = {  'links': covidContentLinks,}
        return render(request,'addsource.html',context)
    elif request.method == 'POST':
        id =str(uuid.uuid4())
        isCreated = CovidContentLink.objects.get_or_create(id=id,url= request.POST.get('weblink'))
        return redirect('/addcovidsource')
    else:
        return redirect('/')    
    
def deletecovidsource(request):
    CovidContentLink.objects.filter(id=request.GET.get('id')).delete()
    return redirect('/addcovidsource')  

def home(request):
    covidcontent = CovidContent.objects.all()
    context = { 
        'covidcontent': covidcontent,
    }
    return render(request,'home.html',context)