# -*- coding: utf-8 -*-
"""

    mslib.msui.topview
    ~~~~~~~~~~~~~~~~~~

    Top view implementation for the msui.
    See the reference documentation, Supplement, for details on the
    implementation.

    This file is part of mss.

    :copyright: Copyright 2008-2014 Deutsches Zentrum fuer Luft- und Raumfahrt e.V.
    :copyright: Copyright 2011-2014 Marc Rautenhaus (mr)
    :copyright: Copyright 2016-2017 by the mss team, see AUTHORS.
    :license: APACHE-2.0, see LICENSE for details.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from builtins import str

import functools
import logging
from mslib.utils import config_loader, get_projection_params, save_settings_pickle, load_settings_pickle
from mslib.msui import MissionSupportSystemDefaultConfig as mss_default
from mslib.msui.mss_qt import QtGui, QtWidgets
from mslib.msui.mss_qt import ui_topview_window as ui
from mslib.msui.mss_qt import ui_topview_mapappearance as ui_ma
from mslib.msui.viewwindows import MSSMplViewWindow
from mslib.msui import wms_control as wc
from mslib.msui import satellite_dockwidget as sat
from mslib.msui import remotesensing_dockwidget as rs
from mslib.msui import kmloverlay_dockwidget as kml
from mslib.msui.icons import icons

# Dock window indices.
WMS = 0
SATELLITE = 1
REMOTESENSING = 2
KMLOVERLAY = 3


class MSS_TV_MapAppearanceDialog(QtWidgets.QDialog, ui_ma.Ui_MapAppearanceDialog):
    """Dialog to set map appearance parameters. User interface is
       defined in "ui_topview_mapappearance.py".
    """

    def __init__(self, parent=None, settings_dict=None):
        """
        Arguments:
        parent -- Qt widget that is parent to this widget.
        settings_dict -- dictionary containing topview options.
        """
        super(MSS_TV_MapAppearanceDialog, self).__init__(parent)
        self.setupUi(self)
        if settings_dict is None:
            settings_dict = {"draw_graticule": True,
                             "draw_coastlines": True,
                             "fill_waterbodies": True,
                             "fill_continents": True,
                             "draw_flighttrack": True,
                             "label_flighttrack": True,
                             "colour_water": (0, 0, 0, 0),
                             "colour_land": (0, 0, 0, 0),
                             "colour_ft_vertices": (0, 0, 0, 0),
                             "colour_ft_waypoints": (0, 0, 0, 0)}

        self.cbDrawGraticule.setChecked(settings_dict["draw_graticule"])
        self.cbDrawCoastlines.setChecked(settings_dict["draw_coastlines"])
        self.cbFillWaterBodies.setChecked(settings_dict["fill_waterbodies"])
        self.cbFillContinents.setChecked(settings_dict["fill_continents"])
        self.cbDrawFlightTrack.setChecked(settings_dict["draw_flighttrack"])
        self.cbLabelFlightTrack.setChecked(settings_dict["label_flighttrack"])

        for button, ids in [(self.btWaterColour, "colour_water"),
                            (self.btLandColour, "colour_land"),
                            (self.btWaypointsColour, "colour_ft_waypoints"),
                            (self.btVerticesColour, "colour_ft_vertices")]:
            palette = QtGui.QPalette(button.palette())
            colour = QtGui.QColor()
            colour.setRgbF(*settings_dict[ids])
            palette.setColor(QtGui.QPalette.Button, colour)
            button.setPalette(palette)

        # Connect colour button signals.
        self.btWaterColour.clicked.connect(functools.partial(self.setColour, "water"))
        self.btLandColour.clicked.connect(functools.partial(self.setColour, "land"))
        self.btWaypointsColour.clicked.connect(functools.partial(self.setColour, "ft_waypoints"))
        self.btVerticesColour.clicked.connect(functools.partial(self.setColour, "ft_vertices"))

    def get_settings(self):
        """
        """
        settings_dict = {
            "draw_graticule": self.cbDrawGraticule.isChecked(),
            "draw_coastlines": self.cbDrawCoastlines.isChecked(),
            "fill_waterbodies": self.cbFillWaterBodies.isChecked(),
            "fill_continents": self.cbFillContinents.isChecked(),
            "draw_flighttrack": self.cbDrawFlightTrack.isChecked(),
            "label_flighttrack": self.cbLabelFlightTrack.isChecked(),

            "colour_water":
                QtGui.QPalette(self.btWaterColour.palette()).color(QtGui.QPalette.Button).getRgbF(),
            "colour_land":
                QtGui.QPalette(self.btLandColour.palette()).color(QtGui.QPalette.Button).getRgbF(),
            "colour_ft_vertices":
                QtGui.QPalette(self.btVerticesColour.palette()).color(QtGui.QPalette.Button).getRgbF(),
            "colour_ft_waypoints":
                QtGui.QPalette(self.btWaypointsColour.palette()).color(QtGui.QPalette.Button).getRgbF(),
        }
        return settings_dict

    def setColour(self, which):
        """Slot for the colour buttons: Opens a QColorDialog and sets the
           new button face colour.
        """
        if which == "water":
            button = self.btWaterColour
        elif which == "land":
            button = self.btLandColour
        elif which == "ft_vertices":
            button = self.btVerticesColour
        elif which == "ft_waypoints":
            button = self.btWaypointsColour

        palette = QtGui.QPalette(button.palette())
        colour = palette.color(QtGui.QPalette.Button)
        colour = QtWidgets.QColorDialog.getColor(colour)
        if colour.isValid():
            palette.setColor(QtGui.QPalette.Button, colour)
            button.setPalette(palette)


class MSSTopViewWindow(MSSMplViewWindow, ui.Ui_TopViewWindow):
    """PyQt window implementing a MapCanvas as an interactive flight track
       editor.
    """
    name = "Top View"

    def __init__(self, parent=None, model=None):
        """Set up user interface, connect signal/slots.
        """
        super(MSSTopViewWindow, self).__init__(parent, model)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(icons('64x64')))

        # Dock windows [WMS, Satellite, Trajectories, Remote Sensing, KML Overlay]:
        self.docks = [None, None, None, None, None]

        self.settings_tag = "topview"
        self.load_settings()

        # Initialise the GUI elements (map view, items of combo boxes etc.).
        self.setup_top_view()

        # Connect slots and signals.
        # ==========================

        # Map controls.
        self.btMapRedraw.clicked.connect(self.mpl.canvas.redraw_map)
        self.cbChangeMapSection.activated.connect(self.changeMapSection)

        # Settings
        self.btSettings.clicked.connect(self.settings_dialogue)

        # Tool opener.
        self.cbTools.currentIndexChanged.connect(self.openTool)

    def __del__(self):
        del self.mpl.canvas.waypoints_interactor

    def setup_top_view(self):
        """Initialise GUI elements. (This method is called before signals/slots
           are connected).
        """
        toolitems = ["(select to open control)", "Web Map Service", "Satellite Tracks", "Remote Sensing", "KML Overlay"]
        self.cbTools.clear()
        self.cbTools.addItems(toolitems)

        # Fill combobox for predefined map sections.
        self.cbChangeMapSection.clear()
        predefined_map_sections = config_loader(dataset="predefined_map_sections",
                                                default=mss_default.predefined_map_sections)
        items = sorted(predefined_map_sections.keys())
        self.cbChangeMapSection.addItems(items)

        # Initialise the map and the flight track. Get the initial projection
        # parameters from the tables in mss_settings.
        kwargs = self.changeMapSection(only_kwargs=True)
        self.mpl.canvas.init_map(**kwargs)
        self.setFlightTrackModel(self.waypoints_model)

    def openTool(self, index):
        """Slot that handles requests to open control windows.
        """
        index = self.controlToBeCreated(index)
        if index >= 0:
            if index == WMS:
                # Create a new WMSDockWidget.
                title = "Web Map Service (Top View)"
                widget = wc.HSecWMSControlWidget(
                    default_WMS=config_loader(dataset="default_WMS", default=mss_default.default_WMS),
                    view=self.mpl.canvas,
                    parent=self,
                    wms_cache=config_loader(dataset="wms_cache", default=mss_default.wms_cache))
            elif index == SATELLITE:
                title = "Satellite Track Prediction"
                widget = sat.SatelliteControlWidget(view=self.mpl.canvas)
            elif index == REMOTESENSING:
                title = "Remote Sensing Tools"
                widget = rs.RemoteSensingControlWidget(view=self.mpl.canvas)
            elif index == KMLOVERLAY:
                title = "KML Overlay"
                widget = kml.KMLOverlayControlWidget(view=self.mpl.canvas)
            else:
                raise IndexError("invalid control index")

            # Create the actual dock widget containing <widget>.
            self.createDockWidget(index, title, widget)

    def changeMapSection(self, index=0, only_kwargs=False):
        """Change the current map section to one of the predefined regions.
        """
        # Get the initial projection parameters from the tables in mss_settings.
        current_map_key = str(self.cbChangeMapSection.currentText())
        predefined_map_sections = config_loader(dataset="predefined_map_sections",
                                                default=mss_default.predefined_map_sections)
        current_map = predefined_map_sections[current_map_key]
        crs_to_mpl_basemap_table = config_loader(dataset="crs_to_mpl_basemap_table",
                                                 default=mss_default.crs_to_mpl_basemap_table)
        proj_params = crs_to_mpl_basemap_table.get(current_map["CRS"])
        if proj_params is None:
            proj_params = get_projection_params(current_map["CRS"])
        if proj_params is None:
            raise ValueError(u"unknown EPSG code: {:}".format(current_map["CRS"]))

        # Create a keyword arguments dictionary for basemap that contains
        # the projection parameters.
        kwargs = current_map["map"]
        kwargs.update({"CRS": current_map["CRS"]})
        kwargs.update({"BBOX_UNITS": proj_params["bbox"]})
        kwargs.update(proj_params["basemap"])

        if only_kwargs:
            # Return kwargs dictionary and do NOT redraw the map.
            return kwargs

        logging.debug("switching to map section %s", current_map_key)
        self.mpl.canvas.redraw_map(kwargs)

    def setIdentifier(self, identifier):
        super(MSSTopViewWindow, self).setIdentifier(identifier)
        self.mpl.canvas.map.set_identifier(identifier)

    def settings_dialogue(self):
        """
        """
        settings = self.getView().get_map_appearance()
        dlg = MSS_TV_MapAppearanceDialog(parent=self, settings_dict=settings)
        dlg.setModal(True)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            settings = dlg.get_settings()
            self.getView().set_map_appearance(settings)
            self.save_settings()
            self.mpl.canvas.waypoints_interactor.redraw_path()
        dlg.destroy()

    def save_settings(self):
        """Save the current settings (map appearance) to the file
           self.settingsfile.
        """
        # TODO: ConfigParser and a central configuration file might be the better solution than pickle.
        # http://stackoverflow.com/questions/200599/whats-the-best-way-to-store-simple-user-settings-in-python
        settings = self.getView().get_map_appearance()
        save_settings_pickle(self.settings_tag, settings)

    def load_settings(self):
        """Load settings from the file self.settingsfile.
        """
        settings = load_settings_pickle(self.settings_tag, {})
        self.getView().set_map_appearance(settings)
