import os

# import logging
from create_logger import create_logger
from idm import GeoGems

res_path = '/media/i-files/home/arnold/development/python/vsSM'
logfile = os.path.join(res_path, 'results', 'idm.log')
logger = create_logger.create_log(logfile)

idm = GeoGems(res_path, 'partial-vaccination.config')
idm.run_simple_epidemic()