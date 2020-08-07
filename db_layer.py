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


def get_enabled_water_level_stations(db_config, model):
    stations = []
    db_con = get_dss_db_connection(db_config)
    if db_con is not None:
        cursor = db_con.cursor(buffered=True)
        sql_query='select {}, station_name, alert_level from dss.station_alert where enable=1;'.format(model)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for row in results:
            model_info = dict(station_id=row[0], station_name=row[1], alert_level=row[2])
            stations.append(model_info)
    close_connection(db_con)
    return stations


def get_station_hash_info(db_config, station_id, source_id, variable_id, unit_id, init_time):
    hash_info = {}
    db_con = get_dss_db_connection(db_config)
    if db_con is not None:
        cursor = db_con.cursor(buffered=True)
        sql_query = 'select id,end_date from curw_fcst.run where station={} and source={} and ' \
                    'variable={} and unit={} and end_date>\'{}\';'.format(
            station_id, source_id, variable_id, unit_id, init_time)
        print('get_station_hash_info|sql_query : ', sql_query)
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result:
            hash_info['hash_id'] = result[0]
            hash_info['latest_fgt'] = result[1]
    close_connection(db_con)
    return hash_info


def get_station_status(db_config, start_limit, end_limit, fgt, alert_level, hash_id):
    alert_info = {}
    db_con = get_dss_db_connection(db_config)
    if db_con is not None:
        cursor = db_con.cursor(buffered=True)
        sql_query = 'select time,fgt,value from curw_fcst.data where time>\'{}\' and time < \'{}\' and fgt = \'{}\' ' \
                    'and value > {} and id = \'{}\' order by value desc limit 1;'.format(start_limit, end_limit, fgt,
                                                                                          alert_level, hash_id)
        print('get_station_hash_info|sql_query : ', sql_query)
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result:
            alert_info['time'] = result[0]
            alert_info['fgt'] = result[1]
            alert_info['value'] = result[2]
    close_connection(db_con)
    return alert_info


