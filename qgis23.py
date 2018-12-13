# -*- coding: utf-8 -*-
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
# This script define objects to help write plugins for both version 2.x and 3.x

from qgis import core

if hasattr(core, "QGis"):
    from qgis.core import QGis
else:
    from qgis.core import Qgis as QGis

if QGis.QGIS_VERSION_INT >= 30000:
    message_log_levels = {
        "Info": QGis.Info,
        "Warning": QGis.Warning,
        "Critical": QGis.Critical,
    }
    message_bar_levels = message_log_levels
    geometry_types = {
        "Point": core.QgsWkbTypes.PointGeometry,
        "Line": core.QgsWkbTypes.LineGeometry,
        "Polygon": core.QgsWkbTypes.PolygonGeometry,
        "UnknownGeometry": core.QgsWkbTypes.UnknownGeometry,
        "NoGeometry": core.QgsWkbTypes.NullGeometry,
    }
else:
    from qgis.gui import QgsMessageBar
    from qgis.core import QgsMessageLog
    message_log_levels = {
        "Info": QgsMessageLog.INFO,
        "Warning": QgsMessageLog.WARNING,
        "Critical": QgsMessageLog.CRITICAL,
    }
    message_bar_levels = {
        "Info": QgsMessageBar.INFO,
        "Warning": QgsMessageBar.WARNING,
        "Critical": QgsMessageBar.CRITICAL,
    }
    geometry_types = {
        "Point": QGis.Point,
        "Line": QGis.Line,
        "Polygon": QGis.Polygon,
        "UnknownGeometry": QGis.UnknownGeometry,
        "NoGeometry": QGis.NoGeometry,
    }

QGis23MessageLogLevel = type('QGis23MessageLogLevel', (), (message_log_levels)) 
QGis23MessageBarLevel = type('QGis23MessageBarLevel', (), (message_bar_levels))
QGis23GeometryType = type('QGisGeometryType', (), (geometry_types))