import traceback
from notifier import notify


if __name__ == '__main__':
    config_path = '/home/hasitha/PycharmProjects/EmailNotifier/config.json'
    parameter_type = 'water_level'
    models = ['flo2d_250']
    try:
        notify(config_path, parameter_type, models)
    except Exception as e:
        print('Exception in main:', str(e))
        traceback.print_exc()




