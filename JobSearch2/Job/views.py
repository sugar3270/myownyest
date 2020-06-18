from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators import csrf

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main(request):
	return render(request,'index.html')

def POST_crawl(request):

	#if 'title' in request.GET and request.GET['title']:
	#keywords = input('請輸入工作職缺關鍵字:')
	keywords = request.POST["title"]
	
	url = "https://jp.indeed.com/jobs?q=" + keywords + "&l=&from=homepage_relatedQuery"
	print(url)

	options = Options()
	#關閉瀏覽器跳出訊息
	prefs = {
	    'profile.default_content_setting_values' :
	        {
	        'notifications' : 2
	         }
	}
	options.add_experimental_option('prefs',prefs)
	options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           #開啟無痕模式

	driver = webdriver.Chrome(options=options)


	#第一頁內容
	driver.get(url)
	
	with open('result.txt', 'w',encoding='utf-8') as f:
		try:
			for content in driver.find_elements_by_class_name('company'):
				print(content.text)
				target = content.text + "\n"
				f.write(target)
		except:
			pass
		driver.close()
	text = []
	with open ('result.txt','r',encoding='utf-8') as f:
		for line in f:
			text.append(line)
	

	return render(request,'result.html',locals())