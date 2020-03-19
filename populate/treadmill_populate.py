import time
from populate import default_settings
from treadmill_pipeline import treadmill


limit = 60 * 55  # 55 minutes in seconds


def main():
    start = time.time()
    while time.time() - start < limit:
        print('==== TreadmillTracking.populate() ====')
        treadmill.TreadmillTracking.populate(**default_settings)
        print('---- sleep ----')
        time.sleep(60)


if __name__ == '__main__':
    main()
