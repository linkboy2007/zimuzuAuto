import json
import requests
from bs4 import BeautifulSoup

class  Pachong:
    """main class to get links"""
    status = 0

    def __init__(self, name='', password=''):
        info = {'account': name, 'password': password, 'remember': '1', 'url_back': 'http%3A%2F%2Fwww.zimuzu.tv%2F'}
        self.s = requests.Session()
        tryLogin = self.s.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=info)
        rtn = json.loads(tryLogin.text)
        self.status = rtn['status']

    def login(self, name, password):
        if(self.status == 1):
            return True
        info = {'account': name, 'password': password, 'remember': '1', 'url_back': 'http%3A%2F%2Fwww.zimuzu.tv%2F'}
        tryLogin = self.s.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=info)
        rtn = json.loads(tryLogin.text)
        self.status = rtn['status']
        return json.dumps(rtn, ensure_ascii=False)

    def getUserInfo(self):
        getCurUserTopInfo = self.s.get('http://www.zimuzu.tv/User/Login/getCurUserTopInfo')
        userInfo = json.loads(getCurUserTopInfo.text)
        return json.dumps(userInfo, ensure_ascii=False)

    def search(self, keyword):
        search = self.s.get('http://www.zimuzu.tv/search/api', params={'keyword': keyword, 'type': ''})
        rtn = json.loads(search.text)
        for list in rtn['data']:
            if(list['channel'] == 'tv'):
                return list['itemid']
        return False

    def get_links(self, itemid, season=True, vFormat='HR-HDTV'):
        rtn = self.s.get('http://www.zimuzu.tv/resource/list/{}'.format(itemid))
        content = BeautifulSoup(rtn.text, "html.parser")
        lis = content.find_all('li', attrs={"format": vFormat, "season": season})
        links = {}
        for li in lis:
            title = li.find('a', attrs={"itemid": True})['title']
            href = li.find('a', attrs={"type": "ed2k"})['href']
            links[title] = href
            #print("{0}\n{1}".format(title, href))
        return links