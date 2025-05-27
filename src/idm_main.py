import os

# import logging
from create_logger import create_logger
from idm import InfectiousDiseaseModel

res_path = '/media/i-files/home/arnold/development/python/vsSM'
logfile = os.path.join(res_path, 'results', 'idm.log')
logger = create_logger.create_log(logfile)

idm = InfectiousDiseaseModel(res_path, 'partial-vaccination.config')
idm.run_simple_epidemic()