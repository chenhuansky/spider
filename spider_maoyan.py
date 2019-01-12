import requests
import json
#pool线程池，多线程处理很快
from multiprocessing import Pool
from requests.exceptions import RequestException
#re是正则表达式解析库
import re
def get_one_page(url):
		try:
			response=requests.get(url)
			#判断是否正确返回了 即200
			if response.status_code==200:
				return response.text
			return None
		except RequestException:
			return None
def parse_one_page(html):
	pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
	items=re.findall(pattern,html)
	#print(items)
	for item in items:
		yield{
			'index':item[0],
			'image':item[1],
			'title':item[2],
			#strip()[3:]的意思是切掉前三个 此处指切掉“主演：”
			'actor':item[3].strip()[3:],
			'time':item[4].strip()[5:],
			'score':item[5]+item[6]
		}

def write_to_file(content):
#此处encoding=‘utf-8’和ensure_ascii=False是为了保证输出的中文不被以别的方式编码
	with open('result.txt','a',encoding='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()

#经过观察 得知offset的值是用来网页翻页的，因此为了一次性处理多个网页（毕竟一页只有10个电影我们要的是前100）
#因此将offset作为参数传入,具体写法是作为字符串str形式接在url后面
def main(offset):
	url='https://maoyan.com/board/4?offset='+str(offset)
	html=get_one_page(url)
	#第一次测试整个页面的html内容返回
	#print(html)
	#parse_one_page(html)
	for item in parse_one_page(html):
		print(item)
		write_to_file(item)

if __name__=='__main__':
	for i in range(10):
		main(i*10) 
	pool=Pool()
	pool.map(main,[i*10 for i in range(10)])