import json
import random

import youtube_dl


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


def generateActivitesUrls(base_url, course_id, act_ids):
    urls = []
    for act_id in act_ids:
        # http://class.xjtu.edu.cn/course/13893/learning-activity/full-screen#/184141
        urls.append(base_url + 'course/' + str(course_id) + '/learning-activity/full-screen#/' + str(act_id))
    return urls


def generateVideoInfoUrls(base_url, act_ids):
    urls = []
    for act_id in act_ids:
        # http://class.xjtu.edu.cn/api/activities/184141
        urls.append(base_url + 'api/activities/' + str(act_id))
    return urls


def getActivitiesID(url, session):
    jstext = session.get(url).text
    # print(jstext)
    jsDict = json.loads(jstext)
    actID = []
    try:
        for act in jsDict["activities"]:
            if act["id"]:
                actID.append(act["id"])
    except Exception as e:
        print(e)

    return actID


def getDownloadUrls(url, session):
    jstext = session.get(url).text

    try:
        jsDict = json.loads(jstext)
        # print(jsDict)
    except json.decoder.JSONDecodeError:
        print("cookies 失效")
        return {}

    video_info = {}
    video_info['title'] = jsDict['title'].split()[0]
    video_info['data'] = jsDict['start_time']
    for video in jsDict['video_suite']['videos']:
        if video['camera_type'] == 'encoder':
            video_info['encoder'] = video['file_url']
        elif video['camera_type'] == 'instructor':
            video_info['instructor'] = video['file_url']

    return video_info


def getCookiesFromFile(cookie_dict, cookie_file='cookies.txt'):
    with open(cookie_file, 'r', encoding='utf-8') as frcookie:
        cookies_txt = frcookie.read().strip(';')  # 读取文本内容
        for item in cookies_txt.split(';'):
            name, value = item.strip().split('=', 1)
            cookie_dict[name] = value


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def handleAndSave(vinfo, file_dir, options='all'):
    for vi in vinfo:
        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [my_hook]
        }

        if options == 'instructor':
            outtmpl = file_dir + '/' + vi['data'][:10] + '_' + 'instructor' + '.%(ext)s'
            ydl_opts['outtmpl'] = outtmpl
            print('downloading ', outtmpl)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([vi['instructor']])

        elif options == 'ppt':
            outtmpl = file_dir + '/' + vi['data'][:10] + '_' + 'encoder' + '.%(ext)s'
            ydl_opts['outtmpl'] = outtmpl
            print('downloading ', outtmpl)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([vi['encoder']])

        else:
            outtmpl = file_dir + '/' + vi['data'][:10] + '_' + 'instructor' + '.%(ext)s'
            ydl_opts['outtmpl'] = outtmpl
            print('downloading ', outtmpl)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([vi['instructor']])

            outtmpl = file_dir + '/' + vi['data'][:10] + '_' + 'encoder' + '.%(ext)s'
            ydl_opts['outtmpl'] = outtmpl
            print('downloading ', outtmpl)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([vi['encoder']])


def writeDownloadUrlsToFile(vinfos, save_dir='.'):
    urls_inst = []
    urls_enco = []

    for v in vinfos:
        if 'encoder' in v.keys():
            urls_enco.append(v['encoder'] + '\n')
        else:
            print(v)
        if 'instructor' in v.keys():
            urls_inst.append(v['instructor'] + '\n')
        else:
            print(v)

    try:
        with open(save_dir + '/urls_inst.txt', 'w') as f:
            f.writelines(urls_inst)

        with open(save_dir + '/urls_enco.txt', 'w') as f:
            f.writelines(urls_enco)
    except Exception as e:
        print(e)