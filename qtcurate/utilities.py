from time import sleep
from qtcurate.dataprocess import DataProcess


def wait_for_completion(dp_id: str, dp: DataProcess):
    percentage = 0
    while percentage < 100:
        result = dp.progress(dp_id)
        percentage = result['progress']
        print(f"Search progress {percentage}%")
        if percentage < 100:
            sleep(1)
    sleep(3)
