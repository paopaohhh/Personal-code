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

data_yjbb = pd.DataFrame()
for i in range(236):
    cookies = {
        'qgqp_b_id': '0f4360f70c40d03e31818d460bd070f1',
        'intellpositionL': '902.391px',
        'em_hq_fls': 'js',
        'emshistory': '%5B%22002402%22%2C%22002759%22%2C%22301110%22%2C%22002947%22%5D',
        'em-quote-version': 'topspeed',
        'xsb_history': '834406%7C%u8FEA%u5A01%u666E%2C871484%7C%u805A%u5408%u7535%u529B%2C830880%7C%u706B%u51E4%u51F0%2C873332%7C%u7F8E%u8FB0%u73AF%u4FDD%2C870156%7C%u745C%u6B23%u7535%u5B50%2C834045%7C%u6E05%u4F17%u79D1%u6280',
        'HAList': 'a-sh-603132-%u91D1%u5FBD%u80A1%u4EFD%2Ca-sz-002947-%u6052%u94ED%u8FBE%2Ca-sz-000509-*ST%u534E%u5851%2Ca-sh-603209-%u5174%u901A%u80A1%u4EFD%2Ca-sh-600272-%u5F00%u5F00%u5B9E%u4E1A%2Ca-sh-603169-%u5170%u77F3%u91CD%u88C5%2Ca-sz-301110-%u9752%u6728%u80A1%u4EFD%2Ca-sz-002759-%u5929%u9645%u80A1%u4EFD%2Ca-sz-002402-%u548C%u800C%u6CF0%2Ca-sh-603070-%u4E07%u63A7%u667A%u9020',
        'cowCookie': 'true',
        'st_si': '65676307439872',
        'cowminicookie': 'true',
        'st_asi': 'delete',
        'st_pvi': '02992749256523',
        'st_sp': '2022-02-21%2020%3A55%3A58',
        'st_inirUrl': 'https%3A%2F%2Fdata.eastmoney.com%2Fbbsj%2F202112%2Fxjll.html',
        'st_sn': '3',
        'st_psi': '20220314154704954-113300301066-6505683837',
        'JSESSIONID': '8F260E4939E453B20026DD45234954ED',
        'intellpositionT': '455px',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    params = (
        ('callback', 'jQuery112309516673853071009_1647244067327'),
        ('sortColumns', 'UPDATE_DATE,SECURITY_CODE'),
        ('sortTypes', '-1,-1'),
        ('pageSize', '50'),
        ('pageNumber', f'{i+1}'),
        ('reportName', 'RPT_LICO_FN_CPD'),
        ('columns', 'ALL'),
        ('filter', '(REPORTDATE=\'2020-12-31\')'),
    )

    response = requests.get('https://datacenter-web.eastmoney.com/api/data/v1/get', headers=headers, params=params,
                            cookies=cookies)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112309516673853071009_1647244067327&sortColumns=UPDATE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber=1&reportName=RPT_LICO_FN_CPD&columns=ALL&filter=(REPORTDATE%3D%272020-12-31%27)', headers=headers, cookies=cookies)

    # 把数据存储在df中
    data = pd.DataFrame(eval(response.text[42:-2].replace('null', 'None').replace('true', 'True'))['result']['data'])
    data = data[data['TRADE_MARKET'] != '新三板']
    data = data[data['SECURITY_TYPE'] != 'B股']
    # 合并两个dataframe
    if i == 0:
        data_yjbb = data
    else:
        data_yjbb = pd.concat([data_yjbb, data], ignore_index=True)
    # data_ybjj


# print(data_yjbb)

# 删除日期太过接近的数据
list_drop = []
list_drop = list_drop + data_yjbb[data_yjbb['UPDATE_DATE'] == '2022-03-25 00:00:00'].index.to_list()
list_drop = list_drop + data_yjbb[data_yjbb['UPDATE_DATE'] == '2022-03-24 00:00:00'].index.to_list()
# list_drop

data_yjbb = data_yjbb.drop(index = list_drop)
data_yjbb = data_yjbb.reset_index(drop=True)
# data_yjbb

########### 获取股价信息 ############
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

# 保存data_ybjj中股票的价格信息，从网易财经下载股票信息，有4900个股票信息
urlStart = 'http://quotes.money.163.com/service/chddata.html?code='
urlEnd = '&end=20220324&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

stockList = getStockList()
for s in stockList:
    # 0：沪市；1：深市
    url = urlStart + ("0" if s.startswith('6') else "1") + s + urlEnd
    filepath = 'D:/股价 小样本/原型网络/data/StocksInfo2020/' + s + '.csv'
    threading.Thread(target=downloadFileSem, args=(url, filepath)).start()

# 这里通过股票代码和披露日期查询股价变动情况
# 并把股价上涨标记为1，下降为0

# 读取对应企业股价信息，并删除列表为空的企业
stockList = getStockList()
list_drop = []
for i in range(len(stockList)):
    path_stock = 'D:/股价 小样本/原型网络/data/StocksInfo2020/' + stockList[i] + '.csv'
    df_stock = pd.read_csv(path_stock, encoding='gbk')
    if df_stock.empty:
        list_drop.append(stockList[i])

for x in list_drop:
    stockList.remove(x)

for x in list_drop:
    data_yjbb = data_yjbb.drop(index=data_yjbb[data_yjbb['SECURITY_CODE'] == x].index)
# 重新设置索引
data_yjbb = data_yjbb.reset_index(drop=True)
# 把更新日期设置为标准格式
data_yjbb['UPDATE_DATE'] = data_yjbb['UPDATE_DATE'].str.replace(' 00:00:00', '')

# 可以看一下还剩多少只股票
data_index_list = data_yjbb.index.to_list()
# data_yjbb

# 缺某些日期的股价信息，需要使用前后时间的股价信息
df_environment = pd.read_csv('D:/股价 小样本/原型网络/data/沪深300.csv', encoding='gbk')

for i in data_index_list:
    path_stock = 'D:/股价 小样本/原型网络/data/StocksInfo2020/' + data_yjbb.loc[i, 'SECURITY_CODE'] + '.csv'
    data_stock = pd.read_csv(path_stock, encoding='gbk')
    #     data_stock['日期'] = data_stock['日期'].str.replace('/', '-')
    #     print(data_stock['日期'])
    data_stock.set_index('日期', inplace=True)
    # 获得公告日的标准日期
    str_update_before = data_yjbb.loc[i, 'UPDATE_DATE'][:-2] + str(int(data_yjbb.loc[i, 'UPDATE_DATE'][8:]) - 1)
    str_update = data_yjbb.loc[i, 'UPDATE_DATE']
    str_update_next = data_yjbb.loc[i, 'UPDATE_DATE'][:-2] + str(int(data_yjbb.loc[i, 'UPDATE_DATE'][8:]) + 1)

    z = 0
    try:
        price_update = data_stock.loc[str_update, '收盘价']
        price_update_next = data_stock.loc[str_update_next, '收盘价']
        # 减去大盘涨幅
        price_update -= df_environment.loc[str_update, '涨跌幅'] / 100 * data_stock.loc[str_update_before, '收盘价']
        price_update_next -= df_environment.loc[str_update_next, '涨跌幅'] / 100 * data_stock.loc[str_update, '收盘价']
    except:
        while True:
            z += 1
            if not (str_update_before in df_environment['日期']):
                str_update_before = str_update
            str_update = str_update_next
            str_update_next = data_yjbb.loc[i, 'UPDATE_DATE'][:-2] + str(
                int(data_yjbb.loc[i, 'UPDATE_DATE'][8:]) + z + 1)
            if str_update in data_stock.index and str_update_next in data_stock.index:
                price_update = data_stock.loc[str_update, '收盘价']
                price_update_next = data_stock.loc[str_update_next, '收盘价']
                # 减去大盘涨幅
                price_update -= df_environment.loc[str_update, '涨跌幅'] / 100 * data_stock.loc[str_update_before, '收盘价']
                price_update_next -= df_environment.loc[str_update_next, '涨跌幅'] / 100 * data_stock.loc[
                    str_update, '收盘价']
                break
            if z >= 20:
                data_yjbb = data_yjbb.drop(index=i)
                break
    if price_update_next - price_update > 0:
        data_yjbb.loc[i, 'label'] = 1  # 价格上涨为1
    else:
        data_yjbb.loc[i, 'label'] = 0  # 价格下降为0
# data_yjbb

# 把财务数据筛选出来，这里把股票代码等也都删除了
data_yjbb = data_yjbb.select_dtypes(exclude='object')
# 查找存在空值的列
data_yjbb_null = data_yjbb.isnull().any().to_dict()
data_yjbb_null_list = list(data_yjbb_null.keys())
# 给空值填充为0
data_yjbb[data_yjbb_null_list] = data_yjbb[data_yjbb_null_list].fillna(0)
# 重新设置索引
data_yjbb.reset_index(inplace=True)
# data_yjbb

# 删除level_0和index列
data_yjbb = data_yjbb.drop(columns=['index'])
# 把label的数据类型转换为int
data_yjbb['label'] = data_yjbb['label'].astype('int64')
# 保存df为csv文件
data_yjbb.to_csv('D:/股价 小样本/原型网络/data/stock2020.csv', index=0)

