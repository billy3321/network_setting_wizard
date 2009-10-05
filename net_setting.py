#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 05 Oct 2009
# The setting.

from optparse import OptionParser 
import ConfigParser

parser = OptionParser()
   
parser.add_option("-c", "--create", dest="create", default="Temporary_setting", help="Create a setting named SETTING_NAME.", metavar="SETTING_NAME")
parser.add_option("-s", "--setup", dest="setup", default=None, help="Setup a setting named SETTING_NAME.", metavar="SETTING_NAME")
parser.add_option("--save", dest="save", default="net_config.ini", help="Save the setting to CONFIG_FILE_PATH", metavar="CONFIG_FILE_PATH")
parser.add_option("--load", dest="load", default="net_config.ini", help="Load the setting to CONFIG_FILE_PATH", metavar="CONFIG_FILE_PATH")
               
(options, args) = parser.parse_args()

