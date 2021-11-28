import requests.cookies
from toolbox import *

config=init()

head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

# http://class.xjtu.edu.cn/api/courses/13893/activities
url_act = config["base_url"] + 'api/courses/' + str(config["course_id"]) + '/activities'
session = requests.session()
session.headers = head

cookies_dict=getCookiesDictFromString(config["cookies"])
cookie_jar = requests.cookies.cookiejar_from_dict(cookies_dict)
session.cookies = cookie_jar

act_ids = getActivitiesID(url_act, session)

act_urls = generateActivitesUrls(config["base_url"], config["course_id"], act_ids)
video_info_urls = generateVideoInfoUrls(config["base_url"], act_ids)

vinfos = []
for video_url in video_info_urls:
    v = getDownloadUrls(video_url, session)
    vinfos.append(v)
    print('working on ', video_url)
    print(v['title'] + ' ' + v['date'])

writeDownloadUrlsToFile(vinfos, save_dir=config["save_dir"])

# option='ppt','instructor','all'
# handleAndSave(vinfos, save_dir, 'all')
