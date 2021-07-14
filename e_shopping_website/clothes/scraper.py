import os
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests


def file_path():
	file_path = os.path.abspath(os.getcwd())
	return file_path

def tokyo(product_name):
    current_directory = file_path()
    driver = webdriver.Chrome(executable_path=f"{current_directory}/clothes/chromedriver")

    tokyodata = {}
    buy_home = "http://tokichoi.91app.com/"
    option = webdriver.ChromeOptions()
    driver.get(buy_home)

    A = driver.find_element_by_class_name("ns-search-input")
    A.send_keys("\""+"product_name"+"\"")
    A.send_keys("\n")
    sleep(1)


    #把本頁搜尋商品的網址截下來
    clothes = BeautifulSoup(driver.page_source,"html.parser")
    movie = clothes.find_all("li",{"class":"cabinet-li blind-li cabinet-in-pc"})
    finding = [] 
    for goods in movie:
        finding.append(goods.a["href"])

    #新的分頁
    num = 0
    for i in finding:
        num+=1
        new_url = "http://tokichoi.91app.com"+i
        driver.get(new_url)
        sleep(0.5)
        #爬詳細的圖文
        clothes = BeautifulSoup(driver.page_source,"html.parser")
        collect_data = []
        try:
            picture = "http://"+clothes.find("figure",{"class":"large-image-frame"}).div.a.img["ng-src"].strip("//")
        except:
            picture = "Not found"
        picture_name = clothes.find("h1",{"class":"salepage-title"}).text.strip()
        if "】" in picture_name:
            picture_name = picture_name.split("】")[1].split("(")[0]
        else:
            picture_name = picture_name.split("(")[0]
        
        clothes_price = clothes.find("div",{"class":"salepage-price"}).div.span.text.strip()[3:].replace(",","")
        picture_color_size = clothes.find_all("script")
        for a in picture_color_size:
            if "window.ServerRenderData"  in a.text:
                s = a
                break
        clothes_color = s.text.strip().split("DisplayPropertyName")[1][3:].split("}")[0][0:-1]
        try:
            clothes_size = s.text.strip().split("DisplayPropertyName")[2][3:].split("}")[0][0:-1]
        except IndexError:
            clothes_size = "F"
        collect_data.append("東京著衣,"+picture_name)
        collect_data.append(picture)
        collect_data.append(clothes_price)
        collect_data.append(clothes_color)
        collect_data.append(clothes_size)
        collect_data.append(new_url)
        idnumber = "tokyo"+"%03d"%num
        tokyodata[idnumber] = collect_data
        collect_data = ["Tokichoi",idnumber,int(clothes_price)]
        # with open(id_price_file, 'a', newline='') as csvfile:
        #         writer = csv.writer(csvfile)
        #         writer.writerow(collect_data)
        # csvfile.close()
    driver.close()
    return tokyodata

tokyo("clothes")