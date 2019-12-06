#!/usr/bin/env python

__author__ = "Pallab Maji"
__copyright__ = "Copyright 2019-2020, codesteller"
__license__ = "MIT"

"""
Created by              :   codesteller 
Date                    :   06/12/19
Description             :   get_stats.py

Add Description Here

"""

from devlogger import devlogger
import logging
import pandas as pd


class DBStats:
    """
    @brief: This class takes the database object and generates statistics of the dataset
            Statistics includes
            1. No. of Instances per class per image
            2.
    """
    def __init__(self, dbdict):
        """

        :param dbdict: Database in dictionary
        """
        self.logger = devlogger.Logger(logging.getLogger(__name__))
        self.db = dbdict
        self.class_list = list()

        # Method Calls
        self.get_class_list()
        self.stats = self.get_stats()

    def get_stats(self):
        """
        @brief: This function extracts the following statistics from the dataset
                -> statistics per image in dictionary with image name as key
                -> overall object counts
        :return: stats_dict

        """
        self.logger.log_i("Extracting statistics")
        stats_dict = self.image_level_stats_dict()
        stats_pd = self.image_level_stats_pd()

        return stats_dict

    def image_level_stats_dict(self):
        """
        @brief: This function takes annotation of an image in a list and extracts objects and their counts in the image.
        :return: stats_dict with extracted data
        """
        stats_dict = dict()
        stats_dict["images"] = dict()

        for im_name in self.db:
            # Extract Image Level Statistics
            ianno = self.db[im_name]["annotation"]
            temp_dict = dict()
            temp_dict["class_hist"] = dict()
            _class_list_per_image = list()
            for x in ianno:
                class_name = x[1].lower()
                if class_name not in self.class_list:
                    self.class_list.append(x[1].lower())
                if class_name not in _class_list_per_image:
                    _class_list_per_image.append(x[1].lower())

                if class_name in temp_dict["class_hist"]:
                    temp_dict["class_hist"][class_name] = temp_dict["class_hist"][class_name] + 1
                else:
                    temp_dict["class_hist"][class_name] = 1
            temp_dict["class_list"] = _class_list_per_image
            stats_dict["images"][im_name] = temp_dict

        return stats_dict

    def get_class_list(self):
        for idx in self.db:
            # Get annotation object
            ianno = self.db[idx]["annotation"]

            for x in ianno:
                class_name = x[1].lower()
                if class_name not in self.class_list:
                    self.class_list.append(class_name)
        return

    def image_level_stats_pd(self):
        """

        :return:
        """
        _temp_stats = dict()
        image_names = list()

        # make empty table for all classes per image
        zeros_list = [0] * len(self.db)
        for image_name in self.db:
            ianno = self.db[image_name]["annotation"]
            image_names.append(image_name)
            for iclass in self.class_list:
                _temp_stats[iclass] = zeros_list
        _temp_stats["images"] = image_names

        return _temp_stats
