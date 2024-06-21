# ***************************************************************************
# __init__.py  -  Geometry Paster QGIS plugin
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
# This script initializes the plugin, making it known to QGIS.


def classFactory(iface):
    from .plugin import Plugin

    return Plugin(iface)
