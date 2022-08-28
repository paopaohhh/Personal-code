#-*- coding : utf-8 -*-
# coding: utf-8
import datetime
import requests
import pandas as pd

def none_func(value, none_str):
    '''空值转换函数'''
    if value == none_str:
        return None
    else:
        return value

cookies = {
    'cowCookie': 'true',
    'qgqp_b_id': '0f4360f70c40d03e31818d460bd070f1',
    'cowminicookie': 'true',
    'xsb_history': '870156%7C%u745C%u6B23%u7535%u5B50',
    'intellpositionL': '902.391px',
    'st_si': '84759847982882',
    'st_asi': 'delete',
    'JSESSIONID': '1F64E95DA6489DE20057FD6E00746CEB',
    'intellpositionT': '1306px',
    'st_pvi': '02992749256523',
    'st_sp': '2022-02-21%2020%3A55%3A58',
    'st_inirUrl': 'https%3A%2F%2Fdata.eastmoney.com%2Fbbsj%2F202112%2Fxjll.html',
    'st_sn': '5',
    'st_psi': '20220222214201257-113300301066-5109735794',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://data.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

params = (
    ('callback', 'jQuery112308824976860570166_1645537321065'),
    ('sortColumns', 'UPDATE_DATE,SECURITY_CODE'),
    ('sortTypes', '-1,-1'),
    ('pageSize', '50'),
    ('pageNumber', '1'),
    ('reportName', 'RPT_LICO_FN_CPD'),
    ('columns', 'ALL'),
    ('filter', '(REPORTDATE=\'2021-12-31\')'),
)

response = requests.get('https://datacenter-web.eastmoney.com/api/data/v1/get', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112308824976860570166_1645537321065&sortColumns=UPDATE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber=1&reportName=RPT_LICO_FN_CPD&columns=ALL&filter=(REPORTDATE%3D%272021-12-31%27)', headers=headers, cookies=cookies)

# 把数据存储在df中
data1 = pd.DataFrame(eval(response.text[42:-2].replace('null', 'None').replace('true', 'True'))['result']['data'])
data1 = data1[data1['TRADE_MARKET'] != '新三板']
# data1

cookies = {
    'cowCookie': 'true',
    'qgqp_b_id': '0f4360f70c40d03e31818d460bd070f1',
    'cowminicookie': 'true',
    'xsb_history': '870156%7C%u745C%u6B23%u7535%u5B50',
    'intellpositionL': '902.391px',
    'st_si': '84759847982882',
    'st_asi': 'delete',
    'JSESSIONID': '1F64E95DA6489DE20057FD6E00746CEB',
    'intellpositionT': '1306px',
    'st_pvi': '02992749256523',
    'st_sp': '2022-02-21%2020%3A55%3A58',
    'st_inirUrl': 'https%3A%2F%2Fdata.eastmoney.com%2Fbbsj%2F202112%2Fxjll.html',
    'st_sn': '5',
    'st_psi': '20220222214201257-113300301066-5109735794',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://data.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

params = (
    ('callback', 'jQuery112308824976860570166_1645537321065'),
    ('sortColumns', 'UPDATE_DATE,SECURITY_CODE'),
    ('sortTypes', '-1,-1'),
    ('pageSize', '50'),
    ('pageNumber', '2'),
    ('reportName', 'RPT_LICO_FN_CPD'),
    ('columns', 'ALL'),
    ('filter', '(REPORTDATE=\'2021-12-31\')'),
)

response = requests.get('https://datacenter-web.eastmoney.com/api/data/v1/get', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112308824976860570166_1645537321065&sortColumns=UPDATE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber=1&reportName=RPT_LICO_FN_CPD&columns=ALL&filter=(REPORTDATE%3D%272021-12-31%27)', headers=headers, cookies=cookies)

# 把数据存储在df中
data2 = pd.DataFrame(eval(response.text[42:-2].replace('null', 'None').replace('true', 'True'))['result']['data'])
data2 = data2[data2['TRADE_MARKET'] != '新三板']
# data2

# 合并两个dataframe
data_yjbb = pd.concat([data1, data2], ignore_index=True)
# data_yjbb

# 获取股价信息
import csv
import urllib.request as r
import threading


# 读取之前获取的个股csv丢入到一个列表中
def getStockList():
    stockList = list(data_yjbb['SECURITY_CODE'])
    #     print(stockList)
    return stockList


def downloadFile(url, filepath):
    try:
        r.urlretrieve(url, filepath)
    except Exception as e:
        print(e)
    print(filepath, "is downloaded")
    pass


# 设置信号量，控制线程并发数
sem = threading.Semaphore(100)


def downloadFileSem(url, filepath):
    with sem:
        downloadFile(url, filepath)


urlStart = 'http://quotes.money.163.com/service/chddata.html?code='
urlEnd = '&end=20220223&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

stockList = getStockList()
for s in stockList:
    # 0：沪市；1：深市
    url = urlStart + ("0" if s.startswith('6') else "1") + s + urlEnd
    filepath = 'D:/股价 小样本/原型网络/data/StocksInfo2021/' + s + '.csv'
    threading.Thread(target=downloadFileSem, args=(url, filepath)).start()


# 这里通过股票代码和披露日期查询股价变动情况
# 并把股价上涨标记为1，下降为0

# 重新设置data_yjbb的索引
data_yjbb = data_yjbb.reset_index(drop=True)
# print(data_yjbb.index)

# 读取对应企业股价信息，并删除列表为空的企业
list_drop = []
for i in range(len(stockList)):
    path_stock = 'D:/股价 小样本/原型网络/data/StocksInfo2021/' + stockList[i] + '.csv'
    df_stock = pd.read_csv(path_stock, encoding='gbk')
    if df_stock.empty:
        list_drop.append(stockList[i])

for x in list_drop:
    stockList.remove(x)

for x in list_drop:
    data_yjbb = data_yjbb.drop(data_yjbb[data_yjbb['SECURITY_CODE'] == x].index)
# 重新设置索引
data_yjbb = data_yjbb.reset_index(drop=True)
# 把更新日期设置为标准格式
data_yjbb['UPDATE_DATE'] = data_yjbb['UPDATE_DATE'].str.replace(' 00:00:00', '')

# 暂时drop前16个企业，因为没有完整的的股价信息
# data_yjbb.drop(index=[x for x in range(16)], inplace=True)

# 获取财务数据的索引
data_index = data_yjbb.index
print(data_yjbb)
for i in data_index:
    path_stock = 'D:/股价 小样本/原型网络/data/StocksInfo2021/' + data_yjbb.loc[i, 'SECURITY_CODE'] + '.csv'
    data_stock = pd.read_csv(path_stock, encoding='gbk')
    #     data_stock['日期'] = data_stock['日期'].str.replace('/', '-')
    print(data_stock['日期'])
    data_stock.set_index('日期', inplace=True)

    str_update_next = data_yjbb.loc[i, 'UPDATE_DATE'][:-2] + str(int(data_yjbb.loc[i, 'UPDATE_DATE'][8:]) + 1)

    try:
        if data_yjbb.loc[i, 'UPDATE_DATE'] == '2022-02-18' or '2022-02-19':
            price_update_next = data_stock.loc['2022-02-21', '收盘价']
        else:
            price_update_next = data_stock.loc[str_update_next, '收盘价']

        if data_yjbb.loc[i, 'UPDATE_DATE'] == '2022-02-19' or '2022-02-20':
            price_update = data_stock.loc['2022-02-18', '收盘价']
        else:
            price_update = data_stock.loc[data_yjbb.loc[i, 'UPDATE_DATE'], '收盘价']

        if price_update_next - price_update > 0:
            data_yjbb.loc[i, 'label'] = 1  # 价格上涨为1
        else:
            data_yjbb.loc[i, 'label'] = 0  # 价格下降为0
    except:
        data_yjbb.drop(index=i, inplace=True)

# 把财务数据筛选出来，这里把股票代码等也都删除了
data_yjbb = data_yjbb.select_dtypes(exclude='object')
# 查找存在空值的列
data_yjbb_null = data_yjbb.isnull().any().to_dict()
data_yjbb_null_list = list(data_yjbb_null.keys())
# 给空值填充为0
data_yjbb[data_yjbb_null_list] = data_yjbb[data_yjbb_null_list].fillna(0)
# 重新设置索引
data_yjbb.reset_index(inplace=True)
# 删除level_0和index列
data_yjbb = data_yjbb.drop(columns=['level_0', 'index'])
# 把label的数据类型转换为int
data_yjbb['label'] = data_yjbb['label'].astype('int64')
# 保存df为csv文件
data_yjbb.to_csv('D:/股价 小样本/原型网络/data/stock2021.csv', index=0)