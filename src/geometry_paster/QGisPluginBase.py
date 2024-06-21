# ***************************************************************************
# qgi23.py  -  Geometry Paster QGIS plugin
# ---------------------
#     begin                : 2018-12-13
#     copyright            : (C) 2018 by NextGIS
#     email                : info@nextgis.com
# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************
# This script define base plugin class

import configparser
import os

this_script_path = os.path.abspath(os.path.dirname(__file__))


class QGISPluginBase:
    def __init__(self):
        self.__md_filename = os.path.join(this_script_path, "metadata.txt")
        if not os.path.exists(self.__md_filename):
            raise ValueError("File metadata.txt not found")

        config = configparser.ConfigParser()
        config.read([self.__md_filename])

        self.__name = config.get("general", "name").strip()
        self.__version = config.get("general", "version")
        self.__description = config.get("general", "description")

        self.__pack_name = self.generate_plugin_pack_name(self.__name)

    @staticmethod
    def generate_metadata(plname):
        config = configparser.RawConfigParser()
        config.add_section("general")
        config.set("general", "name", plname)

        config.set("general", "qgisMinimumVersion", "")
        config.set("general", "description", "")
        config.set("general", "version", "")
        config.set("general", "author", "")
        config.set("general", "about", "")

        with open(
            os.path.join(this_script_path, "metadata.txt"), "w"
        ) as metafile:
            config.write(metafile)

    @staticmethod
    def generate_plugin_pack_name(name):
        pl_dir_name = ""

        i = 0
        if name.find(" ") > 0:
            while i < len(name):
                if name[i] == " ":
                    while name[i] == " ":
                        i += 1
                    pl_dir_name += "_"

                pl_dir_name += name[i].lower()
                i += 1
        else:
            while i < len(name):
                if name[i].isupper():
                    pl_dir_name += "_"
                    while name[i].isupper():
                        pl_dir_name += name[i].lower()
                        i += 1

                pl_dir_name += name[i]
                i += 1

        return pl_dir_name.strip("_")

    @property
    def pack_name(self):
        return self.__pack_name

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def i18nPath(self):
        return os.path.join(this_script_path, "i18n")

    @property
    def dir(self):
        return this_script_path

    @property
    def description(self):
        return self.__description
