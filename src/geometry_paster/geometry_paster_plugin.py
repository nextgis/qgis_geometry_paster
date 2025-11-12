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
import re
from os import path
from typing import List

from osgeo import gdal, ogr
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsMessageLog,
    QgsProject,
    QgsSettings,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon, QKeySequence
from qgis.PyQt.QtWidgets import QAction, QApplication

from .about_dialog import AboutDialog
from .compat import GeometryType
from .QGisPluginBase import QGISPluginBase


def getGeomtryName(geometry_type):
    if geometry_type == GeometryType.Point:
        return "Point"
    elif geometry_type == GeometryType.Line:
        return "Line"
    elif geometry_type == GeometryType.Polygon:
        return "Polygon"
    else:
        return "Unknown"


class GeometryPasterPlugin(QGISPluginBase):
    """docstring for Plugin"""

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.plugin_dir = path.dirname(__file__)

        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.i18nPath, f"geometry_paster_{locale}.qm"
        )
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def tr(self, message):
        return QApplication.translate(__class__.__name__, message)

    def initGui(self):
        self.paste_geometry_action = QAction(
            self.tr("Paste Geometry"), self.iface.mainWindow()
        )
        self.paste_geometry_action.setIcon(
            QIcon(os.path.join(self.dir, "icons/icon.svg"))
        )
        self.paste_geometry_action.setShortcut(QKeySequence("Ctrl+Shift+G"))
        self.paste_geometry_action.setToolTip(self.tr("Paste Geometry"))
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
        self.iface.addPluginToMenu(
            self.tr("Geometry Paster"), self.paste_geometry_action
        )

        self.action_about = QAction(
            QgsApplication.getThemeIcon("mActionPropertiesWidget.svg"),
            self.tr("About plugin…"),
            self.iface.mainWindow(),
        )
        self.action_about.triggered.connect(self.__open_about_dialog)
        self.iface.addPluginToMenu(
            self.tr("Geometry Paster"), self.action_about
        )

        self.__show_help_action = QAction(
            QIcon(os.path.join(self.dir, "icons/icon.svg")),
            "Geometry Paster",
        )
        self.__show_help_action.triggered.connect(self.__open_about_dialog)
        plugin_help_menu = self.iface.pluginHelpMenu()
        assert plugin_help_menu is not None
        plugin_help_menu.addAction(self.__show_help_action)

        self.iface.currentLayerChanged.connect(self._changeCurrentLayerHandle)
        self._changeCurrentLayerHandle(self.iface.activeLayer())

    def unload(self):
        self.iface.editMenu().removeAction(self.paste_geometry_action)
        self.iface.removePluginMenu(
            self.tr("Geometry Paster"), self.paste_geometry_action
        )
        self.iface.digitizeToolBar().removeAction(self.paste_geometry_action)
        self.paste_geometry_action.deleteLater()
        self.paste_geometry_action = None

        self.iface.removePluginMenu(
            self.tr("Geometry Paster"), self.action_about
        )
        self.action_about.deleteLater()
        self.action_about = None

        self.iface.currentLayerChanged.disconnect(
            self._changeCurrentLayerHandle
        )

    def pushMessage(self, title, message, level=Qgis.MessageLevel.Info):
        self.iface.messageBar().pushMessage(title, message, level)

    def pushLog(self, msg, level=Qgis.MessageLevel.Info):
        QgsMessageLog.logMessage(msg, self.name, level)

    def pasteGeometry(self):
        geoms = self._tryGetFeaturesGeomsFromClipBoard()
        if len(geoms) > 1:
            self.pushMessage(
                self.tr("Paste geometry"),
                self.tr("Fail to paste. Multiple features in the clipboard."),
                Qgis.MessageLevel.Critical,
            )
            return
        if len(geoms) == 0:
            self.pushMessage(
                self.tr("Paste geometry"),
                self.tr("Nothing to paste. No features in the clipboard."),
                Qgis.MessageLevel.Critical,
            )
            return

        geom = geoms[0]

        layer = self.iface.activeLayer()
        selected_features = layer.selectedFeatures()

        if len(selected_features) == 0:
            self.pushMessage(
                self.tr("Paste geometry"),
                self.tr("Nowhere to paste. No target feature selected."),
                Qgis.MessageLevel.Critical,
            )
            return

        if layer.geometryType() != geom.type():
            self.pushMessage(
                self.tr("Paste geometry"),
                self.tr("Incompatible geometries. Trying to paste %s to %s")
                % (
                    getGeomtryName(geom.type()),
                    getGeomtryName(layer.geometryType()),
                ),
                Qgis.MessageLevel.Critical,
            )
            return

        result = []
        layer.beginEditCommand("Paste geometries")
        for feature in selected_features:
            result.append(layer.changeGeometry(feature.id(), geom))
        layer.endEditCommand()

        if any(not is_success for is_success in result):
            self.pushMessage(
                self.tr("Paste geometry"),
                self.tr("Something is wrong. Can't change geometry."),
                Qgis.MessageLevel.Critical,
            )
            return

        # This is hack. It is not mandatory instruction.
        # But without new features not repaint.
        # May be I made something wrong above
        self.iface.mapCanvas().refresh()

    def _tryGetFeaturesGeomsFromClipBoard(self):
        clipboard = QApplication.clipboard()
        assert clipboard is not None
        clipboard_text = clipboard.text()

        return self.__parse_features_from_cliboard_content(clipboard_text)

    def _changeCurrentLayerHandle(self, layer):
        if layer and isinstance(layer, QgsVectorLayer):
            layer.selectionChanged.connect(self._checkPasteAvalability)
            layer.editingStarted.connect(self._checkPasteAvalability)
            layer.editingStopped.connect(self._checkPasteAvalability)
            self._checkPasteAvalability()

    def __open_about_dialog(self):
        dialog = AboutDialog(os.path.basename(self.plugin_dir))
        dialog.exec()

    def _checkPasteAvalability(self):
        layer = self.iface.activeLayer()
        is_available = False
        msg = ""
        if layer and isinstance(layer, QgsVectorLayer) and layer.isEditable():
            if len(layer.selectedFeatures()) >= 1:
                is_available = True
            else:
                msg = self.tr("Select a target feature!")
                is_available = False
        else:
            msg = self.tr("Start editing a vector layer!")
            is_available = False

        if is_available:
            if len(self._tryGetFeaturesGeomsFromClipBoard()) == 0:
                msg = self.tr(
                    "Copy feature with the geometry you need to paste first!"
                )
                is_available = False

        self.paste_geometry_action.setEnabled(is_available)
        if is_available:
            self.paste_geometry_action.setToolTip(self.tr("Paste Geometry"))
        else:
            self.paste_geometry_action.setToolTip(
                "{}. {}".format(self.tr("Paste Geometry"), msg)
            )

    def __parse_features_from_cliboard_content(
        self, content: str
    ) -> List[QgsGeometry]:
        # AttributesOnly = "AttributesOnly"
        AttributesWithWKT = "AttributesWithWKT"
        GeoJSON = "GeoJSON"
        copy_format = QgsSettings().value(
            "qgis/copyFeatureFormat", defaultValue=AttributesWithWKT
        )

        if copy_format == AttributesWithWKT:
            return self.__parse_csv(content)
        elif copy_format == GeoJSON:
            return self.__parse_geojson(content)

        self.pushLog("Copy format error", Qgis.MessageLevel.Critical)

        return []

    def __parse_csv(self, content: str) -> List[QgsGeometry]:
        result: List[QgsGeometry] = []

        content = content.replace('"', "")
        content = re.sub(r'"[^"]*"', "", content)

        lines = content.splitlines()
        if len(lines) == 0:
            return []

        wkt_index = 0
        for index, field in enumerate(lines[0].split("\t")):
            if field != "wkt_geom":
                continue
            wkt_index = index
            lines = lines[1:]
            break

        for line in lines:
            wkt_content = line.split("\t")[wkt_index]
            geometry = QgsGeometry.fromWkt(wkt_content)
            if geometry.isGeosValid():
                result.append(geometry)

        return result

    def __parse_geojson(self, content: str) -> List[QgsGeometry]:
        """
        Parse geometries from a GeoJSON string.

        :param content: GeoJSON data as a string.
        :type content: str

        :return: List of parsed QgsGeometry objects.
        :rtype: List[QgsGeometry]
        """
        driver: gdal.Driver = ogr.GetDriverByName("GeoJSON")
        datasource: gdal.Dataset = driver.Open(content)
        if datasource is None:
            return []

        layer = datasource.GetLayer()
        if layer is None:
            return []

        result: List[QgsGeometry] = []

        source_crs = QgsCoordinateReferenceSystem("EPSG:4326")

        active_layer = self.iface.activeLayer()
        if active_layer:
            target_crs = active_layer.crs()
        else:
            target_crs = QgsProject.instance().crs()

        transform = QgsCoordinateTransform(
            source_crs, target_crs, QgsProject.instance()
        )

        for feature in layer:
            wkt_content = feature.GetGeometryRef().ExportToWkt()
            geometry = QgsGeometry.fromWkt(wkt_content)
            geometry.transform(transform)
            result.append(geometry)

        return result
