import json
from multiprocessing.dummy import Pool as ThreadPool

import requests
from bs4 import BeautifulSoup


class Pachong:
    """main class to get links"""
    status = 0

    def __init__(self, name='', password=''):
        info = {'account': name, 'password': password, 'remember': '1', 'url_back': 'http%3A%2F%2Fwww.zimuzu.tv%2F'}
        self.s = requests.Session()
        tryLogin = self.s.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=info)
        rtn = json.loads(tryLogin.text)
        self.status = rtn['status']

    def login(self, name, password):
        if self.status == 1:
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

    def search(self, keywords):
        """
        :param keywords: 搜索关键字
        :return: 搜索结果对应itemid（用于构建url）
        """
        itemids = []
        for keyword in keywords:

            search = self.s.get('http://www.zimuzu.tv/search/api', params={'keyword': keyword, 'type': ''})
            rtn = json.loads(search.text)
            for list in rtn['data']:
                if list['channel'] == 'tv':
                    itemids.append(list['itemid'])

        return itemids if len(itemids) > 0 else False

    def get_links(self, itemid, season=True, vFormat='HR-HDTV'):
        searchs = []
        for id in itemid:
            url = 'http://www.zimuzu.tv/resource/list/{}'.format(id)
            searchs.append({'url': url, 'season': season, 'vFormat': vFormat})

        print(searchs)
        pool = ThreadPool(4)
        result = pool.map(self.papapa, searchs)
        print(result)

    def papapa(self, search):
        print('url={}'.format(search['url']))
        rtn = self.s.get(search['url'])
        # print(rtn.text)
        content = BeautifulSoup(rtn.text, "html.parser")
        lis = content.find_all('li', attrs={"format": search['vFormat'],
                                            "season": search['season'] if search['season'] else True})
        # print(search['vFormat'], search['season'])
        # print(lis)
        links = {}
        for li in lis:
            title = li.find('a', attrs={"itemid": True})['title']
            href = li.find('a', attrs={"type": "ed2k"})['href']
            links[title] = href
            # print("{0}\n{1}".format(title, href))
        return links
