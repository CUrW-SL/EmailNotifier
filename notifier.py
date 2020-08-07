import json
import traceback
from datetime import datetime,timedelta
from db_layer import get_enabled_water_level_stations, get_station_hash_info


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
                print('')






