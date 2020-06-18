import requests
import re
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from django.shortcuts import render
from . import models

BASE_CRAIGSLIST_URL ='https://www.melltoo.com/en/ae?search={}'
#BASE_IMAGE_URL = 'https://d1armgzt214jrp.cloudfront.net/{}_200x200.jpg'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features='html.parser')

    divs = soup.find('div',{'class':'items-container'})
    listings = divs.findAll('a')
    final = []
    for post in listings:
        title = post.find(class_='item-name').text
        if post.find(class_='item-price'):
            price = post.find(class_='item-price').text
        else:
            price = 'NA'

        url = post.find('img')['src']

        #if post.find(class_='').get()
        final.append((title, price, url))
        #print(final)
    stuff_for_frontend= {'search':search,
                    'final_postings':final}
    return render(request, 'my_app/new_search.html',stuff_for_frontend)