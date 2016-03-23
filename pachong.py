import json,sys,requests,MySQLdb,urllib
from multiprocessing.dummy import Pool as ThreadPool
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

        self.db = MySQLdb.connect('localhost', 'root', '', 'test', use_unicode=True, charset="utf8")
        self.cursor = self.db.cursor()

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
            searchs.append({'url': url, 'seriesid': id, 'season': season, 'vFormat': vFormat})

        print(searchs)
        pool = ThreadPool(4)
        result = pool.map(self.papapa, searchs)
        self.db.commit()
        self.db.close()
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
            seriesid = search['seriesid']
            season = li['season']
            episode = li['episode']
            itemid = li.find('a', attrs={"itemid": True})['itemid']
            title = li.find('a', attrs={"itemid": True})['title']
            href = li.find('a', attrs={"type": "ed2k"})['href']
            links[title] = href
            # print("insert into zimuzu(item_id,series_id,episode,season,ed2k) VALUES({0},{1},{2},{3},'{4}')".format(itemid, seriesid, episode, season, urllib.parse.quote(href)))
            self.cursor.execute("insert into zimuzu(item_id,series_id,episode,season,ed2k) VALUES({0},{1},{2},{3},'{4}')".format(itemid, seriesid, episode, season, href))

        return links

    # def store(self, resu):