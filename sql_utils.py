import pymysql


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


def query(sql, *args):
    """
    Encapsulating generic queries
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_c1_data():
    """
    :return: data for div center 1
    """
    # Take the latest set of data of the timestamp
    sql = """
    SELECT total,total-heal-dead,heal,dead from (
    select sum(confirm) total, 
    (SELECT heal from history ORDER BY ds desc LIMIT 1) heal ,
      sum(dead) dead 
    from details where update_time=(
      select update_time from details order by update_time desc limit 1)
    ) d;
    """
    res = query(sql)
    return res[0]


def get_c2_data():
    """
    :return:  data for div center 2
    """
    sql = "select province,sum(confirm_now) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    """
    :return: data for div left 1
    """
    sql = "select ds,confirm_add,heal_add from history"
    res = query(sql)
    return res


def get_l2_data():
    """
    :return: data for div left 2
    """
    sql = "select end_update_time,province,city,county,address,type" \
          " from risk_area " \
          "where end_update_time=(select end_update_time " \
          "from risk_area " \
          "order by end_update_time desc limit 1) "
    res = query(sql)
    return res


def get_r1_data():
    """
    :return:  data for div right 1
    """
    sql = 'SELECT province,confirm FROM ' \
          '(select province ,sum(confirm_now) as confirm from details  ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY confirm DESC LIMIT 5'
    res = query(sql)
    return res


def get_r2_data():
    """
    :return:  data for div right 1
    """
    sql = 'select content from hotsearch order by id desc limit 30'
    res = query(sql)
    return res
