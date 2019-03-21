'''
This is a py file for functions may frequently used

'''
import time
import json

TIME_WINDOW = 900

def try_until_success(func, *args, **kwargs):
    while True:
        try:
            ret = func(*args, **kwargs)
            break
        except Exception as e:
            print(e)
            time.sleep(TIME_WINDOW)
    return ret


def load_config():
    with open('../meta.json', 'r') as metafile:
        content = metafile.read()
        config = json.loads(content)
    return config

