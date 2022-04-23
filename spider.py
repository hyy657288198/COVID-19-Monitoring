import requests
import json
import pymysql
import time
from bs4 import BeautifulSoup
import hashlib


def get_conn():
    """
    create connection and cursor
    """
    # create connection
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="Hyy657288198!",
                           db="covid_map",
                           charset="utf8")
    # create cursor
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    """
    close connection and cursor
    """
    cursor.close()
    conn.close()


def get_tencent_data():
    """
    get detail data and history data from tencent covid-19 websites.
    """
    url_update = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf'
    url_his = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList," \
              "chinaDayAddList,nowConfirmStatis,provinceCompare "
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.88 Safari/537.36',
    }
    r_update = requests.get(url_update, headers)
    r_his = requests.get(url_his, headers)
    res_update = json.loads(r_update.text)  # json convert to dictionary
    res_his = json.loads(r_his.text)
    data_update = res_update['data']['diseaseh5Shelf']
    data_his = res_his['data']

    history = {}  # history data
    for i in data_his["chinaDayList"]:
        if i["date"] > "04.01":
            ds = i["y"] + "." + i["date"]
            tup = time.strptime(ds, "%Y.%m.%d")
            # change the format of time to correspond to the datetime type in the database
            ds = time.strftime("%Y-%m-%d", tup)
            confirm = i["confirm"]
            if i["nowConfirm"] < 0:
                confirm_now = 0
            else:
                confirm_now = i["nowConfirm"]
            suspect = i["suspect"]
            heal = i["heal"]
            dead = i["dead"]
            history[ds] = {"confirm": confirm, "confirm_now": confirm_now, "suspect": suspect, "heal": heal,
                           "dead": dead}
        else:
            continue
    for i in data_his["chinaDayAddList"]:
        if i["date"] > "04.01":
            ds = i["y"] + "." + i["date"]
            tup = time.strptime(ds, "%Y.%m.%d")
            ds = time.strftime("%Y-%m-%d", tup)
            confirm_add = i["confirm"]
            suspect_add = i["suspect"]
            heal_add = i["heal"]
            dead_add = i["dead"]
            history[ds].update(
                {"confirm_add": confirm_add, "suspect_add": suspect_add, "heal_add": heal_add, "dead_add": dead_add})
        else:
            continue

    details = []  # Detailed data of the day
    update_time = data_update["lastUpdateTime"]
    data_country = data_update["areaTree"]  # Find out the data of China
    data_province = data_country[0]["children"]  # Provinces in China
    for pro_infos in data_province:
        province = pro_infos["name"]  # province
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]  # city
            confirm = city_infos["total"]["confirm"]  # Cumulative diagnosis
            confirm_add = city_infos["today"]["confirm"]  # New diagnosis
            if city_infos["total"]["nowConfirm"] < 0:
                confirm_now = 0
            else:
                confirm_now = city_infos["total"]["nowConfirm"]  # Existing diagnosis
            heal = city_infos["total"]["heal"]  # Cumulative heal
            dead = city_infos["total"]["dead"]  # Cumulative dead
            details.append([update_time, province, city, confirm, confirm_add, confirm_now, heal, dead])
    return history, details


def update_details():
    """
    Insert the detailed data into the database
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  # 0 is history data and 1 is detailed data
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,confirm_now,heal,dead) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s)"
        # Compare the current maximum timestamp
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()} Start updating the latest detailed data")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()} Update latest detailed data completed")
        else:
            print("The current data is the latest data.")
    finally:
        close_conn(conn, cursor)


def update_history():
    """
    Insert the history data into the database
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0 is history data and 1 is detailed data
        print(f"{time.asctime()} Start updating the latest history data")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):  # If the data of the current day does not exist, write data in
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("confirm_now"),
                                     v.get("suspect"), v.get("suspect_add"), v.get("heal"),
                                     v.get("heal_add"), v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()} Update latest history data completed")
    finally:
        close_conn(conn, cursor)


def get_baidu_hot():
    """
    Get hot search from Baidu website
    """
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/100.0.4896.88 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, features="html.parser")
    kw = soup.select("div.c-single-text-ellipsis")
    count = soup.select("div.hot-index_1Bl1a")
    context = []
    for i in range(len(kw)):
        k = kw[i].text.strip()  # Remove spaces
        v = count[i].text.strip()
        context.append(f"{k}{v}".replace('\n', ''))
    return context


def update_hotsearch():
    """
    Insert the hot search into the database
    """
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()} Start updating the latest hot search data")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))  # insert data
        conn.commit()
        print(f"{time.asctime()} Update latest hot search data completed")
    finally:
        close_conn(conn, cursor)


def get_risk_area():
    """
    Get data of medium and high risk areas
    """
    # Current timestamp
    o = '%.3f' % (time.time() / 1e3)
    e = o.replace('.', '')
    i = "23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA"
    a = "123456789abcdefg"
    # sign1
    s1 = hashlib.sha256()
    s1.update(str(e + i + a + e).encode("utf8"))
    s1 = s1.hexdigest().upper()
    # sign2
    s2 = hashlib.sha256()
    s2.update(str(e + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA' + e).encode("utf8"))
    s2 = s2.hexdigest().upper()
    # Post request data
    post_dict = {
        'appId': 'NcApplication',
        'key': '3C502C97ABDA40D0A60FBEE50FAAD1DA',
        'nonceHeader': '123456789abcdefg',
        'paasHeader': 'zdww',
        'signatureHeader': s1,
        'timestampHeader': e
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Referer': 'http://bmfw.www.gov.cn/',
        'Origin': 'http://bmfw.www.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.88 Safari/537.36',
        'x-wif-nonce': 'QkjjtiLM2dCratiA',
        'x-wif-paasid': 'smt-application',
        'x-wif-signature': s2,
        'x-wif-timestamp': e,
    }
    url = "http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson"
    req = requests.post(url=url, data=json.dumps(post_dict), headers=headers)
    resp = req.text
    res = json.loads(resp)
    utime = res['data']['end_update_time']  # updating time
    # 具体数据
    hlist = res['data']['highlist']
    mlist = res['data']['middlelist']

    risk_h = []
    risk_m = []

    for hd in hlist:
        type = "高风险"
        province = hd['province']
        city = hd['city']
        county = hd['county']
        communitys = hd['communitys']
        for x in communitys:
            risk_h.append([utime, province, city, county, x, type])

    for md in mlist:
        type = "中风险"
        province = md['province']
        city = md['city']
        county = md['county']
        communitys = md['communitys']
        for x in communitys:
            risk_m.append([utime, province, city, county, x, type])

    return risk_h, risk_m


def update_risk_area():
    """
    Insert the risk areas data into the database
    """
    cursor = None
    conn = None
    try:
        risk_h, risk_m = get_risk_area()
        conn, cursor = get_conn()
        sql = "insert into risk_area(end_update_time,province,city,county,address,type) values(%s,%s,%s,%s,%s,%s)"
        # Compare the current maximum timestamp
        sql_query = 'select %s=(select end_update_time from risk_area order by id desc limit 1)'
        cursor.execute(sql_query, risk_h[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()} Start updating the latest risk areas data")
            for item in risk_h:
                cursor.execute(sql, item)
            for item in risk_m:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()} Update latest risk areas data completed")
        else:
            print("The current data is the latest data.")
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    update_history()
    update_details()
    update_hotsearch()
    update_risk_area()
