# Python self executing directory
import sys
import os
CURRENT_PATH = sys.path[0]
sys.path.append(os.path.join(CURRENT_PATH, 'lib'))

from devices import GpsDevice
from devices import read_gpx

def demo():
    print("volpy demo run.")
    sample_data = os.path.join(
        CURRENT_PATH,
        'datasets',
        'survey_ibema_faxinal.gpx')
    df = read_gpx(sample_data, GpsDevice.GARMIN_MONTANA_680)
    print(df)

if __name__ == '__main__':
    demo()
