#!/usr/bin/env python

__author__ = "Pallab Maji"
__copyright__ = "Copyright 2019-2020, codesteller"
__license__ = "MIT"

"""
Created by              :   codesteller 
Date                    :   06/12/19
Description             :   devlogger.py

Add Description Here

"""

import logging
import os


class Logger:
    def __init__(self, logger, filename='application.log'):
        # self.logger = logging.getLogger(__name__)
        self.logger = logger
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.filename = os.path.join(self.log_dir, filename)
        logging.basicConfig(filename=self.filename, filemode='w',
                            format='%(levelname)s : %(name)s : %(message)s',
                            level=logging.INFO)
        self.logger.info("Logger setup successful")

    def log_i(self, message):
        self.logger.info(message)

    def log_w(self, message):
        self.logger.warning(message)

    def log_e(self, message):
        self.logger.error(message)
