from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import json
#import numpy as np
#import pandas as pd
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
#THIS IS FOR AMAZON WEBSITE#
#driver=webdriver.Edge(r'C:\WorkSoftwares\WebDriver\msedgedriverr.exe')
#records1=[]
#dicta={}
#dictf={}
app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_url(search_term):
    template="https://www.amazon.in/s?k={}&ref=nb_sb_noss_2"
    search_term=search_term.replace(' ','+')
    return template.format(search_term)
def extract_record(item):
    """Extractng and returning data from a single item"""
    #description and url
    atag=item.h2.a
    description=atag.text.strip()
    url='https://www.amazon.in'+atag.get('href') 
    
    #price
    try:
        price_parent=item.find('span','a-price')
        price=price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
    
    #try:
    #rating=item.i.text
    #review_count=item.find('span',{'class':'a-size-base','dir':'auto'}).text
#     except AttributeError:
#         rating=''
#         review_count=''
        
    #result=(description,price,url)
    result=list((description,price,url))
    return result
def main(search_term,driver):
    records1=[]
    url=get_url(search_term)
    driver.get(url)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    results=soup.find_all('div',{'data-component-type':'s-search-result'})

    for item in results:
        record=extract_record(item)
        if record:
            records1.append(record)
#     dicta={"PRODUCT":records1[0][:6],"PRICE":records1[1][:6],"URL":records1[2][:6]}
#     print(dicta)
    producta=[]
    prica=[]
    urla=[]
    for i in range(0,6):
        producta.append(str(records1[i][0]))
        prica.append(str(records1[i][1]))
        urla.append(str(records1[i][2]))
#     print(producta)
    dicta={"PRODUCT":producta,"PRICE":prica,"URL":urla}
    #print(dicta)
    return dicta

#THIS IS FOR FLIPKART#
def get_url2(search_term2):
    template2="https://www.flipkart.com/search?q={}"
    search_term2=search_term2.replace(' ','%20')
    return template2.format(search_term2)
def main2(search_term2):
    url2=get_url2(search_term2)
    res2=requests.get(url2)
    soup2=bs4.BeautifulSoup(res2.text,'lxml')
    if(len(list(soup2.select(".s1Q9rs")))!=0):
        #print("hi")
        class1=".s1Q9rs"
        class2="._30jeq3"
        class3="._3LWZlK"
    else:
        class2="._30jeq3._1_WHN1"
        class1="._4rR01T"
        class3="._3LWZlK"
    name2=soup2.select(class1)
    price2=soup2.select(class2)#._1_WHN1")
    #urlobj=get_url(name[0].text)
    ratings2=soup2.select(class3)
#     print(name[0].text)
#     print(price[0].text)
#     print(urlobj)
#     print(ratings[0].text)
    namef=[]
    pricef=[]
    urlobj=[]
    ratingsf=[]
    for i in range(0,6):
        namef.append(str(name2[i].text))
        pricef.append(str(price2[i].text))
        ratingsf.append(str(ratings2[i].text))
        #namef.append(str(name[i].text))
        urlobj.append(str(get_url(name2[i].text)))
    dictf={"PRODUCT":namef,"PRICE":pricef,"URL":urlobj,"RATINGS":ratingsf} #dictionary of flipkart
    #print(dictf)
    #data=pd.DataFrame(dictf)
#     print(len(namef))
#     print(len(pricef))
#     print(len(ratingsf))
#     print(len(urlobj))
    #print(data)
    return dictf


@app.route("/",methods=["POST"])
@cross_origin()
def home():
    dicta={}
    data=request.json
    #product=data['productName']
    product="skullcandy"
    driver=webdriver.Edge(r'C:\WorkSoftwares\WebDriver\msedgedriverr.exe')
    dicta=main(product,driver)
    dictf=main2(product) 
    print(dicta)
    print(dictf)
    d={"Amazon":dicta,
       "Flipkart":dictf
       }
    
    return json.dumps(d)
if __name__=='__main__':
    app.run()