#! usr/bin/python
#coding=utf-8


#这个可以用了！！！！！！！！！！！


import os, threading, requests, math, re, random
#这个OID用的是每个微博用户的相片界面的id

# Configuration Start
OID = 1005051882811994
#COOKIES = "k1aSj6DvSDWv; SINAGLOBAL=7552724259118.417.1447641174437; ULV=1447691774405:2:2:2:6434341784127.688.1447691774390:1447641174455; YF-Page-G0=7f5e11c19f51c6954c5e18e40c0b1444; _s_tentry=-; Apache=6434341784127.688.1447691774390; USRANIME=usrmdinst_29"; # Your cookies.
COOKIES = "SCF=AnhE9Exp4c8SWGkava8wwQUlRMNgjyzSqhlFHE4cKP-quXuW95mDeZB_h-UjpRWD4k2EGnVNp4mG9JBh7ArSX3A.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFW4a5FiGehO.rmsxRU6L8s5JpX5K-hUgL.Fo-feozc1KM4SK.2dJLoI7pNqPS.eKz0Ss809sqt; _T_WM=34fd50ea6ccca30ad4491387afd582a0; H5_INDEX_TITLE=wasd1234asdf; H5_INDEX=3; MLOGIN=0; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26luicode%3D20000173%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011; SUB=_2A252DUnmDeRhGeNL6VAX-SnFzjWIHXVVDleurDV6PUJbkdAKLWfnkW1NSQntNZnQJvrrAwbjOR3ZmCP4oiu475QR; SUHB=0oUoQeEIwdv-hh; SSOLoginState=1527331254"

CRAWL_PHOTOS_NUMBER = 1000
# Configuration END


COOKIES = dict((l.split('=') for l in COOKIES.split('; ')))
#先创建保存图片的目录
SAVE_PATH="image_"+ 'gakki' + "/"
if not os.path.exists(SAVE_PATH):
	os.makedirs(SAVE_PATH)
TEMP_LastMid = ""

def save_image(image_name):
	#if not os.path.isfile(SAVE_PATH + image_name):
	sina_image_url = 'http://ww1.sinaimg.cn/large/' + image_name
	response = requests.get(sina_image_url, stream=True)
	image = response.content
	try:
		print(image_name)
		with open(SAVE_PATH+image_name,"wb") as image_object:
			image_object.write(image)
			return
	except IOError:
		print("IO Error\n")
		return
	finally:
		image_object.close



def get_album_photos_url(page):
	global TEMP_LastMid
	data={
		'ajwvr':6,
		'filter':'wbphoto|||v6',
		'page': page,
		'count':20,
		'module_id':'profile_photo',
		'oid':OID,
		'uid':'',
		'lastMid':TEMP_LastMid,
		'lang':'zh-cn',
		'_t':1,
		'callback':'STK_' + str(random.randint(10000000000000, 900000000000000))
	}
	#print(data)
	#print(COOKIES)
	album_request_result = requests.get('http://photo.weibo.com/page/waterfall',  params = data, cookies = COOKIES).text
	#print(album_request.headers)
	TEMP_LastMid = re.compile(r'"lastMid":"(\d+)"').findall(album_request_result)
	print(TEMP_LastMid)
	return (re.compile(r'(\w+.png|\w+.gif|\w+.jpg)').findall(album_request_result))

if __name__ == '__main__':
	for i in range(1, int(math.ceil(CRAWL_PHOTOS_NUMBER / 20.0))):
		threads = []
		for image_name in get_album_photos_url(i):
			#save_image(image_name);
			threads.append(threading.Thread(target=save_image, args=(image_name,)))
		for t in threads:
			#t.setDaemon(True)
			t.start()
