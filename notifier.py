import json
import traceback
from datetime import datetime,timedelta
from db_layer import get_enabled_water_level_stations, \
    get_station_hash_info, get_station_status


def _get_config(config_path):
    config = None
    try:
        config = json.loads(open(config_path).read())
    except FileNotFoundError as nofile:
        print('get_config|FileNotFoundError : ', str(nofile))
        traceback.print_exc()
    finally:
        return config


def notify(config_path, parameter_type, models, lead_time_hours=6):
    print('notify|[config_path, parameter_type, models] : ', [config_path, parameter_type, models])
    config = _get_config(config_path)
    if config is not None:
        print('notify|config : ', config['model_config'])
        if parameter_type == 'water_level':
            print('notify|water_level')
            notify_water_level(config, models, lead_time_hours)
        elif parameter_type == 'discharge':
            print('notify|discharge')
        elif parameter_type == 'precipitation':
            print('notify|discharge')
    else:
        print('notify|no required config')


def _get_time_limits(lead_time_hours):
    print('get_time_limits|lead_time_hours : ', lead_time_hours)
    current_time = datetime.now()
    init_time = current_time.strftime('%Y-%m-%d 00:00:00')
    start_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time = (current_time + timedelta(hours=lead_time_hours)).strftime('%Y-%m-%d %H:%M:%S')
    print('get_time_limits|[init_time, start_time, end_time] : ', [init_time, start_time, end_time])
    return [init_time, start_time, end_time]


def notify_water_level(config, models, lead_time_hours):
    [init_time, start_time, end_time] = _get_time_limits(lead_time_hours)
    notify_water_level_info = []
    for model in models:
        print('notify_water_level|model : ', model)
        model_config = config['model_config']['water_level'][model]
        print('notify_water_level|model_config : ', model_config)
        stations = get_enabled_water_level_stations(config['db_config'], model)
        print('notify_water_level|stations : ', stations)
        alerted_stations = []
        for station in stations:
            hash_info = get_station_hash_info(config['db_config'], station['station_id'],
                                              model_config['source'], model_config['variable'],
                                              model_config['unit'], init_time)
            print('notify_water_level|hash_info : ', hash_info)
            if hash_info:
                if hash_info['latest_fgt'] > datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S'):
                    alert_info = get_station_status(config['db_config'], start_time, end_time,
                                                    hash_info['latest_fgt'].strftime('%Y-%m-%d %H:%M:%S'),
                                                    station['alert_level'], hash_info['hash_id'])
                    if alert_info:
                        station['hash_id'] = hash_info['hash_id']
                        station['latest_fgt'] = hash_info['latest_fgt']
                        station['time'] = alert_info['time']
                        station['fgt'] = alert_info['fgt']
                        station['value'] = alert_info['value']
                        alerted_stations.append(station)
                    else:
                        print('notify_water_level|no alert info found.')
                else:
                    print('notify_water_level|no runs for today|model:', model)
            else:
                print('notify_water_level|no hash info|station : ', station)
        notify_water_level_info.append({model: alerted_stations})





