import requests
from lxml import etree
import pandas as pd
import json
import os
import difflib

银行 = input('输入银行名称:')
报告名称 = input('输入报告名称(例如:2021年半年度报告):')
网址 = 'http://www.cninfo.com.cn/new/information/topSearch/detailOfQuery'
ua = {
'Referer': 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=%E5%8D%97%E4%BA%AC%E9%93%B6%E8%A1%8C',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
# 'Cookie': 'JSESSIONID=B2EDF048CEEC9654B855149A23E330C3; routeId=.uc2; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1628931283,1628944634,1628944670; _sp_ses.2141=*; _sp_id.2141=5eb72c37-2568-4011-9c7e-da96208087c2.1628931282.3.1628983927.1628950943.b1c1f3bc-4d24-447b-a953-cf2c983b0b52; SID=1688d2b5-e94f-4dcd-a52a-e30b4e7e73fa; cninfo_user_browse=002142,9900003281,宁波银行|601009,9900003284,南京银行; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1628983928'
}
data = {
'keyWord': 银行,
'maxSecNum': 10,
'maxListNum': 5
}

响应数据 = requests.post(url=网址,headers=ua,data = data).text
# 响应数据.encoding = 'gbk'
字典 = json.loads(响应数据)
# print(字典)

股市代码 = 字典['keyBoardList'][0]['orgId']
股票代码 = 字典['keyBoardList'][0]['code']

if not os.path.exists('./银行年报'):
    os.makedirs('./银行年报')

网址1 = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
UA伪装 = {
'Cookie': 'JSESSIONID=A6E77E2691E39C8C51E1FF75DFAD1CBD; _sp_ses.2141=*; routeId=.uc2; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1628931283; SID=0ca14ca4-138f-464c-8711-18ee65182bfe; cninfo_user_browse=002142,9900003281,%E5%AE%81%E6%B3%A2%E9%93%B6%E8%A1%8C|601009,9900003284,%E5%8D%97%E4%BA%AC%E9%93%B6%E8%A1%8C; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1628932386; _sp_id.2141=5eb72c37-2568-4011-9c7e-da96208087c2.1628931282.1.1628932956.1628931282.98980760-993f-47bc-bf19-0bd2f3d14db8',
'Referer': 'http://www.cninfo.com.cn/new/disclosure/stock?stockCode=002142&orgId=9900003281',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}
data1 = {
'stock': 股票代码+','+股市代码,
'pageSize': 30,
'pageNum': 1,
'category': 'category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;',
'column': 'szse',
'tabName': 'fulltext'

}
响应数据1 = requests.post(url = 网址1,headers=UA伪装,data=data)

字典1 = json.loads(响应数据1.text)
总页数 = 字典1['totalRecordNum']
try:
    for i in range(1,总页数+1):

        data2 = {
            'stock': 股票代码 + ',' + 股市代码,
            'pageSize': 30,
            'pageNum': i,
            'category': 'category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;',
            'column': 'szse',
            'tabName': 'fulltext'
        }
        响应数据2 = requests.post(url=网址1, headers=UA伪装, data=data2)
        字典2 = json.loads(响应数据2.text)


        for i in 字典2['announcements']:
            # if (difflib.SequenceMatcher(None,i['announcementTitle'],报告名称).ratio()>0.9) and (i['secName'] == 银行):
            print(i['announcementTitle'])
            if (i['announcementTitle'] == 报告名称) and (i['secName'] == 银行):
                url = 'http://static.cninfo.com.cn/' + i['adjunctUrl']
                下载 = requests.get(url=url,headers=UA伪装,params=data)
                名称 = i['announcementTitle']
                with open(f'./银行年报/{银行}{名称}.pdf','wb') as f:
                    f.write(下载.content)
#             elif (difflib.SequenceMatcher(None,i['announcementTitle'],报告名称).ratio()>0.8) and (i['secName'] == 银行):
#
#                 url = 'http://static.cninfo.com.cn/' + i['adjunctUrl']
#                 下载 = requests.get(url=url,headers=UA伪装,params=data)
#                 名称 = i['announcementTitle']
#                 with open(f'./银行年报/{银行}{名称}.pdf','wb') as f:
#                     f.write(下载.content)
except:
    pass
# print(type(字典['announcements']))
#     print(响应数据2)


