# import logging
from telnetlib import GA
from create_logger import create_logger
logger = create_logger.create_log('grid-vehicles.log')

import random
import pandas as pd

from idm import InfectiousDiseaseModel

# Initialize Pandas  display options such that the whole DataFrame is printed
pd.options.display.max_rows = 999999
pd.options.display.max_columns = 999999

# Constants

if __name__ == "__main__":
    random.seed(42)

    res_path = '/media/i-files/home/arnold/development/python/vsSM'

    idm = InfectiousDiseaseModel(res_path)
    idm.run_simple_epidemic()