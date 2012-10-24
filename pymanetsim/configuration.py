import ConfigParser

config = ConfigParser.ConfigParser()

if not config.read('config.cfg'):
    # This is for when building the manual
    alternative = config.read('../pymanetsim/config.cfg')

    if not alternative:
        print "Could not find the configuration file"

DATA_RAW_PATH = config.get('PyManetSimConfig', 'data_raw_path')
DATA_PROCESSED_PATH = config.get('PyManetSimConfig', 'data_processed_path')
IMAGES_PATH = config.get('PyManetSimConfig', 'images_path')

DEBUG = config.getboolean('PyManetSimConfig', 'debug')

#If you want to be less correct but do speedier simulations
FAST = config.getboolean('PyManetSimConfig', 'fast')


DRAW_MAPS = config.getboolean('PyManetSimConfig', 'draw_maps')
