import traceback
from notifier import notify


if __name__ == '__main__':
    config_path = '/home/hasitha/PycharmProjects/EmailNotifier/config.json'
    try:
        notify(config_path, 'water_level', ['flo2d_250', 'flo2d_150', 'flo2d_150_v2'], 6)
    except Exception as e:
        print('Exception in main:', str(e))
        traceback.print_exc()




