# 読み込み -> 変換 -> 加工(削落 -> 時間) -> js書出 -> 評価(時間 -> 並替(リスト)) -> 加工(HTML) -> document -> yey
### タイトル、セクション分け
## セクションごとのサブ作業
# コメント&コメントアウト

import json
import xmltodict
from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup
import re
import itertools

class Notifinfo:
    def __init__(self, args):
        self.channel = args['channel']
        self.title = args['title']
        self.link = args['link']
        self._untidiedDate = args['date']
        self.tidiedDate = None
        self.strfDate = None
        self.unixDate = None
        self.category = args['category']

    def _setUnixTime(self):
        if type(self.tidiedDate) is datetime:
            self.unixDate = self.tidiedDate.timestamp()
        else:
            raise ValueError('date untidied')

    def _setStrDate(self):
        if type(self.tidiedDate) is datetime:
            # self.strfDate = self.tidiedDate.strftime('%-m/%-d %H:%M')
            self.strfDate = self.tidiedDate.strftime('%Y/%m/%d %H:%M')
        else:
            raise ValueError('date untidied')

    def tidyTimeWDMYTZ(self):
        # Www DD Mmm YYYY TT:TT:TT +TTTT
        self.tidiedDate = datetime.strptime(self._untidiedDate, '%a, %d %b %Y %H:%M:%S %z')
        self._setUnixTime()
        self._setStrDate()

    def tidyTimeYMDC(self):
        # Yyyy年M月D日　コメント
        red = re.match('^(\S+)', self._untidiedDate).group(1)
        self.tidiedDate = datetime.strptime(red, '%Y年%m月%d日')
        self._setUnixTime()
        self._setStrDate()

    def tidyTimeYMDTHMSZ(self):
        # 2020-04-03T16:13:45+00:00
        self.tidiedDate = datetime.strptime(self._untidiedDate, '%Y-%m-%dT%H:%M:%S+00:00')
        self._setUnixTime()
        self._setStrDate()

    def tidyTimeYMDHMS(self):
        # 2020-04-23 21:25
        self.tidiedDate = datetime.strptime(self._untidiedDate, '%Y-%m-%d %H:%M')
        self._setUnixTime()
        self._setStrDate()

    def getAsDict(self):
        dicta = {}
        dicta['channel'] = self.channel
        dicta['title'] = self.title
        dicta['link'] = self.link
        # dicta['tidiedDate'] = self.tidiedDate
        dicta['strfDate'] = self.strfDate
        dicta['category'] = self.category
        return dicta



### IO(読込 --> js書出)
def get(fileName):
    with open(fileName) as f:
        return f.read()

def letOut(fileName, text):
    with open(fileName, mode='a') as f:
        f.write('\n' + text + '\n')

### classのproperty checker
def check(classInstance):
    for k,v in bunInfoList[2].__dict__.items():
        print(k,':',v)

### bridgeJSの中身の消去
def clearFile(fileName):
    with open(fileName, mode='w') as f:
        f.write('\n')

### 日付を送る
def letOutExecuteTime():
    dateNow = datetime.now().strftime('%Y/%m/%d %H:%M')
    fileNameWrite = 'bridge.js'
    tidiedText = f'var executeTime = "{dateNow}";'
    letOut(fileNameWrite, tidiedText)

### はじめの呼び出し
clearFile('bridge.js')
letOutExecuteTime()



### rss: 処理
def rssConverter(channelName):
    ## オブジェクトにする
    fileNameRead = f'{channelName}.xml'
    rssXml = get(fileNameRead)
    rssDict = xmltodict.parse(rssXml)

    rssItemsList = rssDict['rss']['channel']['item']

    rssInfoList = []
    for item in rssItemsList:
        args = {}
        args['channel'] = str(channelName+'News')
        args['title'] = item['title']
        args['link'] = item['link']
        args['date'] = item['pubDate']
        args['category'] = item['category']
        notifinfo = Notifinfo(args)
        rssInfoList.append(notifinfo)

    for item in rssInfoList: item.tidyTimeWDMYTZ()

    ## 日付判定して、より新しいものがリストの先頭に来るように
    rssInfoList.sort(key=lambda s: s.unixDate, reverse=True)
    rssDictList = [info.getAsDict() for info in rssInfoList]

    fileNameWrite = 'bridge.js'
    tidiedText = f'var {channelName}FromBridge = {rssDictList};'

    letOut(fileNameWrite, tidiedText)

    ## check
    # check(bunInfoList[2])
    # print(bunInfoList[2].getUnixTime())
    # for item in bunInfoList: print(item.tidiedDate)

### rss処理呼び出し
# top, clife, bun, とsocinfo
rssConverter('top')
rssConverter('clife')
rssConverter('bun')
rssConverter('socinfo')



### infocial: 処理
def htmlInfocialConverter(channelName):
    fileNameRead = f'{channelName}.html'
    html = get(fileNameRead)
    soup = BeautifulSoup(html, 'html.parser')


    ## column-content-center
    mainTitle = soup.select('.column-content h1')[1:]
    mainDate = soup.select('.column-content p[style="text-align:right"]')
    mainLink = 'http://sil.tamacc.chuo-u.ac.jp/wp/'
    mainInfoList = []
    for t,d in zip(mainTitle, mainDate):
        args = {}
        args['channel'] = 'infocial'
        args['title'] = t.string
        args['link'] = mainLink
        args['date'] = d.string
        args['category'] = 'null'
        notifinfo = Notifinfo(args)
        mainInfoList.append(notifinfo)

    for item in mainInfoList: item.tidyTimeYMDC()

    ## column-narrow-right
    subLi = soup.select('.column-narrow .academica-featured-posts-gallery li')
    subInfoList = []
    for l in subLi:
        title = l.find('h3').string
        link = l.find('h3').find('a').get('href')
        date = l.find('span', class_='datetime').find('time').get('datetime')
        args = {}
        args['channel'] = 'infocial'
        args['title'] = title
        args['link'] = link
        args['date'] = date
        args['category'] = 'null'
        notifinfo = Notifinfo(args)
        subInfoList.append(notifinfo)

    for item in subInfoList: item.tidyTimeYMDTHMSZ()

    ## unify
    infoList = mainInfoList + subInfoList

    infoList.sort(key=lambda s: s.unixDate, reverse=True)
    dictList = [info.getAsDict() for info in infoList]

    fileNameWrite = 'bridge.js'
    tidiedText = f'var {channelName}FromBridge = {dictList};'

    letOut(fileNameWrite, tidiedText)



### corona: 処理
def htmlCoronaConverter(channelName):
    fileNameRead = f'{channelName}.html'
    html = get(fileNameRead)
    soup = BeautifulSoup(html, 'html.parser')

    ## mod content
    modContList = soup.select('#post_detail .mod_cont')[1:]
    wList = [modCont.select('li a') for modCont in modContList]
    aList = [a for a in itertools.chain.from_iterable(wList) if re.match(r'^【2.*', str(a.text))]
    aTitleList = [re.match(r'.*?】(\S*)\s?.*?',str(a.text)).group(1) for a in aList]
    aLinkList = [a.get('href') for a in aList]
    aDateList = [re.match(r'^【(\S*?)】',str(a.text)).group(1) for a in aList]
    infoList = []
    for t,l,d in zip(aTitleList, aLinkList, aDateList):
        args = {}
        args['channel'] = 'corona'
        args['title'] = t
        args['link'] = l
        args['date'] = d
        args['category'] = 'null'
        notifinfo = Notifinfo(args)
        infoList.append(notifinfo)

    for item in infoList: item.tidyTimeYMDC()

    infoList.sort(key=lambda s: s.unixDate, reverse=True)
    dictList = [info.getAsDict() for info in infoList]

    fileNameWrite = 'bridge.js'
    tidiedText = f'var {channelName}FromBridge = {dictList};'

    letOut(fileNameWrite, tidiedText)



### html処理呼び出し
htmlCoronaConverter('corona')
htmlInfocialConverter('infocial')



### cplus: 処理
def htmlCplusConverter(channelName):
    fileNameRead = f'{channelName}.html'
    html = get(fileNameRead)
    soup = BeautifulSoup(html, 'html.parser')

    ## table new_massage
    aList = soup.select('table.new_message tr td.bb a')
    aTitleList = [a.text for a in aList]
    aLinkList = [a.get('href') for a in aList]
    fssList = soup.select('table.new_message tr td.fss')
    fssDateList = [re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})',str(f.text)).group(1) for f in fssList]
    infoList = []
    for t,l,d in zip(aTitleList, aLinkList, fssDateList):
        args = {}
        args['channel'] = 'cplus'
        args['title'] = t
        args['link'] = l
        args['date'] = d
        args['category'] = 'null'
        notifinfo = Notifinfo(args)
        infoList.append(notifinfo)

    for item in infoList: item.tidyTimeYMDHMS()

    infoList.sort(key=lambda s: s.unixDate, reverse=True)
    dictList = [info.getAsDict() for info in infoList]

    fileNameWrite = 'bridge.js'
    tidiedText = f'var {channelName}FromBridge = {dictList};'

    letOut(fileNameWrite, tidiedText)



### cplusの呼び出し
htmlCplusConverter('cplus')




















