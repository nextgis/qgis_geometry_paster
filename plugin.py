# -*- coding: utf-8 -*-
# ***************************************************************************
# plugin.py  -  Geometry Paster QGIS plugin
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
# This script is main plugin script.

import os
import csv
import sys
import ctypes

csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO

from qgis.PyQt.QtCore import QSettings, QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon, QKeySequence
from qgis.PyQt.QtWidgets import QApplication, QAction
from qgis.core import QgsGeometry, QgsVectorLayer, QgsMessageLog

from .QGisPluginBase import QGISPluginBase

from .qgis23 import (
    QGis23MessageLogLevel,
    QGis23MessageBarLevel,
    QGis23GeometryType,
)


def getGeomtryName(geometry_type):
    if geometry_type == QGis23GeometryType.Point:
        return 'Point'
    elif geometry_type == QGis23GeometryType.Line:
        return 'Line'
    elif geometry_type == QGis23GeometryType.Polygon:
        return 'Polygon'
    elif geometry_type == QGis23GeometryType.UnknownGeometry:
        return 'UnknownGeometry'
    elif geometry_type == QGis23GeometryType.NoGeometry:
        return 'NoGeometry'
    else:
        return 'Unknown'


class Plugin(QGISPluginBase):
    """docstring for Plugin"""
    def __init__(self, iface):
        super(Plugin, self).__init__()
        self.iface = iface

        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.i18nPath,
            'plugin_{}.qm'.format(locale)
        )
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def tr(self, message):
        return QApplication.translate('Plugin', message)

    def initGui(self):
        self.paste_geometry_action = QAction(
            self.tr('Paste Geometry'),
            self.iface.mainWindow()
        )
        self.paste_geometry_action.setIcon(
            QIcon(os.path.join(self.dir, 'icon.svg'))
        )
        self.paste_geometry_action.setShortcut(QKeySequence('Ctrl+Shift+G'))
        self.paste_geometry_action.setToolTip(self.tr('Paste Geometry'))
        self.paste_geometry_action.setStatusTip(self.description)
        self.paste_geometry_action.setEnabled(False)
        self.paste_geometry_action.triggered.connect(self.pasteGeometry)

        self.iface.editMenu().insertAction(
            self.iface.actionDeleteSelected(),
            self.paste_geometry_action,
        )
        self.iface.digitizeToolBar().insertAction(
            self.iface.actionDeleteSelected(),
            self.paste_geometry_action,
        )

        self.iface.currentLayerChanged.connect(self._changeCurrentLayerHandle)
        self._changeCurrentLayerHandle(self.iface.activeLayer())

    def unload(self):
        self.iface.editMenu().removeAction(
            self.paste_geometry_action
        )
        self.iface.digitizeToolBar().removeAction(self.paste_geometry_action)
        self.iface.currentLayerChanged.disconnect(self._changeCurrentLayerHandle)

    def pushMessage(self, title, message, level=QGis23MessageBarLevel.Info):
        self.iface.messageBar().pushMessage(
            title,
            message,
            level
        )

    def pushLog(self, msg, level=QGis23MessageLogLevel.Info):
        QgsMessageLog.logMessage(
            msg,
            self.name,
            level
        )

    def pasteGeometry(self):
        geoms = self._tryGetFeaturesGeomsFromClipBoard()
        if len(geoms) > 1:
            self.pushMessage(
                self.tr('Paste geometry'),
                self.tr('Fail to paste. Multiple features in the clipboard.'),
                QGis23MessageBarLevel.Critical
            )
            return
        if len(geoms) == 0:
            self.pushMessage(
                self.tr('Paste geometry'),
                self.tr('Nothing to paste. No features in the clipboard.'),
                QGis23MessageBarLevel.Critical
            )
            return

        geom = geoms[0]

        layer = self.iface.activeLayer()
        selected_features = layer.selectedFeatures()

        if len(selected_features) > 1:
            self.pushMessage(
                self.tr('Paste geometry'),
                # 'Multiple features selected. Need only one.',
                self.tr('Multiple features are selected. There should be only one.'),
                QGis23MessageBarLevel.Critical
            )
            return

        if len(selected_features) == 0:
            self.pushMessage(
                self.tr('Paste geometry'),
                self.tr('Nowhere to paste. No target feature selected.'),
                QGis23MessageBarLevel.Critical
            )
            return

        feature = selected_features[0]

        if feature.geometry().type() != geom.type():
            self.pushMessage(
                self.tr('Paste geometry'),
                self.tr('Incompatible geometries. Trying to paste %s to %s') % (
                    getGeomtryName(geom.type()),
                    getGeomtryName(feature.geometry().type())
                ),
                QGis23MessageBarLevel.Critical
            )
            return

        result = layer.changeGeometry(feature.id(), geom)

        if not result:
            self.pushMessage(
                self.tr('Paste geometry'),
                self.tr('Something is wrong. Can\'t change geometry.'),
                QGis23MessageBarLevel.Critical
            )
            return

        # This is hack. It is not mandatory instruction.
        # But without new features not repaint.
        # May be I made something wrong above
        self.iface.mapCanvas().refresh()

    def _tryGetFeaturesGeomsFromClipBoard(self):
        cb = QApplication.clipboard()
        clipboard_text = cb.text()
        if sys.version_info[0] == 2:
            clipboard_text = clipboard_text.encode('utf-8')

        reader = csv.DictReader(
            StringIO(clipboard_text),
            delimiter='\t'
        )

        geoms = []
        for row in reader:
            wkt_geom = row.get('wkt_geom')
            geom = QgsGeometry.fromWkt(wkt_geom)

            if not geom:
                self.pushLog('Can\'t create geometry from wkt: %s' % wkt_geom)
                continue

            geoms.append(geom)
        return geoms

    def _changeCurrentLayerHandle(self, layer):
        if layer and isinstance(layer, QgsVectorLayer):
            layer.selectionChanged.connect(
                self._checkPasteAvalability
            )
            layer.editingStarted.connect(
                self._checkPasteAvalability
            )
            layer.editingStopped.connect(
                self._checkPasteAvalability
            )
            self._checkPasteAvalability()

    def _checkPasteAvalability(self):
        layer = self.iface.activeLayer()
        is_available = False
        if layer and isinstance(layer, QgsVectorLayer) and layer.isEditable():

            if len(layer.selectedFeatures()) == 1:
                is_available = True
            else:
                msg = self.tr("Select a target feature!")
                is_available = False
        else:
            msg = self.tr("Start editing a vector layer!")
            is_available = False

        if is_available:
            if len(self._tryGetFeaturesGeomsFromClipBoard()) == 0:
                msg = self.tr("Copy feature with the geometry you need to paste first!")
                is_available = False

        self.paste_geometry_action.setEnabled(is_available)
        if is_available:
            self.paste_geometry_action.setToolTip(self.tr('Paste Geometry'))
        else:
            self.paste_geometry_action.setToolTip(
                "%s. %s" % (
                    self.tr('Paste Geometry'),
                    msg
                )
            )
