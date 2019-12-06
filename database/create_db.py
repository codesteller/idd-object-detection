#!/usr/bin/env python

__author__ = "Pallab Maji"
__copyright__ = "Copyright 2019-2020, codesteller"
__license__ = "MIT"

"""
Created by              :   codesteller 
Date                    :   06/12/19
Description             :   create_db.py

Add Description Here

"""

import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
from devlogger import devlogger
import logging


class Database:
    """
    @brief: This is a database class that aggregates images and annotation.
    """
    def __init__(self, img_dir, lbl_dir):
        # Initialize logger
        self.logger = devlogger.Logger(logging.getLogger(__name__))

        self.img_dir = img_dir
        self.lbl_dir = lbl_dir
        self.imgtypes = ["png", "jpeg", "jpg"]
        self.lbltypes = ["xml"]

        # Call methods
        self.db = self._make_dataset()

    def _make_dataset(self):
        """
        @brief: Generate dataset from the image and annotation directories.
        This function extracts the image paths, corresponding label or annotation file path, parses the annotation file
        to extract image size and annotation information and makes a dictionary

        :return: database as a dictionary : keys = {image_path, label_path, image_size, annotation}

        ToDo: Add stats of the data parsed
        """
        imgpaths = self._get_images(self.img_dir, self.imgtypes)
        lblpaths = self._get_images(self.lbl_dir, self.lbltypes)
        db_dict = dict()

        for lbl_key in tqdm(lblpaths):
            _temp_dict = dict()
            annotation_tree = ET.parse(lblpaths[lbl_key])
            annotation_obj = annotation_tree.getroot()
            labels_dict = self._parse_annotation(annotation_obj)

            # get image paths
            try:
                _im_path = imgpaths[lbl_key]
            except KeyError:
                _im_path = None
                print("Image with key {} not found.".format(lbl_key))

            # Assemble the database dictionary
            _temp_dict["image_path"] = _im_path  # Image path
            _temp_dict["label_path"] = lblpaths[lbl_key]  # Annotation path
            _temp_dict["image_size"] = labels_dict['size']
            _temp_dict["annotation"] = labels_dict['object_list']

            db_dict[lbl_key] = _temp_dict

        self.logger.log_i("Extraction completed")
        return db_dict

    def _get_images(self, file_dir, file_types):
        """
        @brief: This method finds all files of file_types in the directory file_dir and returns a dictionary with
                file names as key
        :param file_dir: Directory to search
        :param file_types: file extensions to be searched
        :return: dictionary with file name as key
        """
        file_list = dict()
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                for filetype in file_types:
                    if file.endswith(filetype):
                        _path = os.path.join(root, file)
                        _temp = self._splitall(_path)
                        # get basename and remove extension and add hierarchy folder
                        _basename = _temp[-2] + "/" + os.path.splitext(os.path.basename(_path))[0]

                        if _basename not in file_list:
                            file_list[_basename] = _path
                        else:
                            self.logger.log_e("duplicate filename: {} & {}".format(_path, file_list[_basename]))
        return file_list

    @staticmethod
    def _parse_annotation(annotation_obj):
        """
        @brief: This function parses the annotation object in xml element tree form to extract
        the annotation information in to a dictionary.
        :param annotation_obj: xml element tree object
        :return: dictionary with metatdata (filename, folder, image size) and object list
        """
        anno_obj = dict()
        object_list = list()
        counter = 0

        for iobj in annotation_obj:
            temp = list()
            if iobj.tag.lower() == "folder":
                anno_obj["folder"] = [iobj.text]
            if iobj.tag.lower() == "filename":
                anno_obj["filename"] = [iobj.text]
            if iobj.tag.lower() == "size":
                anno_obj["size"] = [iobj[0].text, iobj[1].text]
            if iobj.tag.lower() == "object":
                temp.append(counter)  # Box ID
                temp.append(iobj[0].text)  # Box Class
                temp.append(int(iobj[1][0].text))  # Box x0
                temp.append(int(iobj[1][1].text))  # Box y0
                temp.append(int(iobj[1][2].text))  # Box x1
                temp.append(int(iobj[1][3].text))  # Box y1
                counter += 1
                object_list.append(temp)

        anno_obj["object_list"] = object_list
        return anno_obj

    @staticmethod
    def _splitall(path):
        """
        Function is reused from https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
        :param path: any file or directory path
        :return: list of the directories (in sequence) in the directory or file path
        """
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts
