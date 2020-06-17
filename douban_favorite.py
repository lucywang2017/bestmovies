#-*- coding:utf-8-*-

import expanddouban
import bs4
from bs4 import BeautifulSoup
import csv

"""
获取每个地区，每个类型页面的URL
"""

def getMovieUrl(category,location):
	url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}'.format(category,location)
	return url

#print(getMovieUrl('剧情','美国'))

"""
获取电影页面的HTML
"""
def getMovieHTML(url,loadmore='true'):
	html = expanddouban.getHtml(url)
	return html

#print(getMovieHTML('https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国'))

"""
定义电影类
"""
class Movie:
	def __init__(self,name,rate,location,category,info_link,cover_link):
		self.name = name 
		self.rate = rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link


	def print_data(self):
		return "{},{},{},{},{},{}".format(self.name,self.rate,self.location,self.category,self.info_link,self.cover_link)


		"""
		获取豆瓣电影的信息
		"""
def getMovies(category,location):
	url = getMovieUrl(category,location) #获取连接
	html = expanddouban.getHtml(url) #获取DOM结构
	soup = bs4.BeautifulSoup(html,'html.parser') #解析DOM结构
	#print(soup)
	html_content = soup.find_all('a','item')
	#print(html_content)

#getMovies("剧情","美国")
	moviesList = []

	for item in html_content:
		name = item.find('span','title').string
		rate = item.find('span','rate').string
		info_link = item['href']
		cover_link = item.find('img')['src']

		moviesList.append(Movie(name,rate,location,category,info_link,cover_link).print_data())
	return moviesList

#print(getMovies('剧情','美国'))

"""
构造电影数据表
"""

category_list = ['动作','犯罪','战争']
location_list = ['大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','丹麦','巴西']

movieDataList = []
movieDataListTemp = []

for location in location_list:
	for category in category_list:
		temp = getMovies(category,location)
		movieDataListTemp.append(temp)
		movieDataList += temp

with open('movies.csv','w',encoding = 'utf-8-sig', newline = '') as csvfile:
	movies_writer = csv.writer(csvfile,delimiter = ',',quotechar = '|',quoting = csv.QUOTE_MINIMAL)
	for item in movieDataList:
		result = item.split(',',-1)
		movies_writer.writerows([result])
csvfile.close()


"""统计电影数据
"""
movies_content = []
with open('movies.csv','r',encoding = 'UTF-8-sig') as csvfile:
	moviereader = csv.reader(csvfile)

	for row in moviereader:
		movies_content.append(row)


cate_dict = {}

for item in movies_content:
	if item[3] in cate_dict:
		cate_dict.update({item[3]:(cate_dict[item[3]] + 1)})
	else:
		cate_dict.update({item[3]:1})


movie_dict = {}

for item in movies_content:
	if item[3] in movie_dict:
		if item[2] in movie_dict[item[3]]:
			movie_dict[item[3]].update({item[2]:(movie_dict[item[3]][item[2]] +1)})
		else:
			movie_dict[item[3]].update({item[2]:1})
	else:
		movie_dict.update({item[3]:{item[2]:1}})

def List_Output(list,num,max):
	cnt = 0 
	list_loca = []
	list_val = []
	list_out = []

	for i in range(len(list)):
		cnt +=1
		if cnt>max:
			break
		loca = list[i][0]

		val = float('%.2f' %(100*(list[i][1]/num)))

		list_loca.append(loca)
		list_val.append(str(val)+'%')

	list_out.append(list_loca)
	list_out.append(list_val)


	return list_out

def w_txt(category,list):
	with open('output.txt','a',encoding = 'UTF-8-sig') as output:

		category_number = "{}类型电影中，数量排名前三的地区包括:".format(category)
		output.write(category_number)
		output.write(",".join(str(loca) for loca in list[0]) + "。")
		output.write('分别占此类别电影总数的百分比为:')
		output.write(",".join(str(per) for per in list[1]) + "。")
		output.write("\n" * 2)
    #return 

for cate in movie_dict:
	list = []
	category = []

	num = int(cate_dict[cate])

	category = sorted(movie_dict[cate].items(),key = lambda item:item[1],reverse = True)
	list = List_Output(category,num,3)

	w_txt(cate,list)


