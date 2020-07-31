import mysql.connector
from datetime import datetime, timedelta
import pandas as pd


def get_db_connection(mysql_user, mysql_password, mysql_host, mysql_db):
    try:
        connection = mysql.connector.connect(user=mysql_user,
                                             password=mysql_password,
                                             host=mysql_host,
                                             database=mysql_db)
        print('new db connection has created.')
        return connection
    except ConnectionError as ex:
        print('ConnectionError|ex: ', ex)
        return None


def get_fcst_db_connection(db_config):
    return get_db_connection(db_config['user'], db_config['password'], db_config['host'],'curw_fcst')


def get_dss_db_connection(db_config):
    return get_db_connection(db_config['user'], db_config['password'], db_config['host'], 'dss')


def close_connection(connection):
    if connection is not None:
        connection.close()
        print('db connection has closed.')
    else:
        print('db connection has already closed.')


def get_enabled_stations(db_config):
    stations = []
    db_con = get_dss_db_connection(db_config)
    if db_con is not None:
        cursor = db_con.cursor(buffered=True)
        sql_query='select flo2d_250,flo2d_150,flo2d_150_v2,mike,station_name,alert_level from dss.station_alert where enable=1;'
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for row in results:
            model_info = dict(flo2d_250=row[0], flo2d_150=row[1], flo2d_150_v2=row[2], mike=row[3],
                              station_name=row[4], alert_level=row[5])
            stations.append(model_info)
    close_connection(db_con)
    return stations


