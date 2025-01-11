#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script is a PyQt5 GUI for picking seismic traveltimes.
Copyright (C) 2024, 2025 Sylvain Pasquet
Email: sylvain.pasquet@sorbonne-universite.fr

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Import libraries
import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
    QFileDialog, QInputDialog, QAction, QLabel, QListWidget, QComboBox, QStatusBar,
    QPushButton, QDialog, QHBoxLayout, QVBoxLayout, QLineEdit
)
# from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QLocale
import pyqtgraph as pqg
from pyqtgraph.Qt import QtCore
import numpy as np
import matplotlib.pyplot as plt
import obspy
import re

# Obspy functions
def read_seismic_file(seismic_file, separate_sources=False):
    '''
    Read a seismic file and return a list of streams, one for each source.

    Parameters
    ----------
    seismic_file : str
        The path to the seismic file.
    separate_sources : bool, optional
        If True, separate the traces into different streams based on the original_field_record_number.
        Default is False.
        
    Returns
    -------
    stream : obspy.Stream
        The stream object containing the seismic data.
    '''
    # Read the seismic file
    stream = obspy.read(seismic_file,unpack_trace_headers=True)

    input_format = check_format(stream)

    if input_format == 'seg2':
        input_format = 'segy'
        file_base_name, _ = os.path.splitext(seismic_file)
        try: # Try to convert file_base_name to an integer
            ffid = int(file_base_name)
        except ValueError:
            ffid = 1
        stream.write('tmp.sgy',format='SEGY',data_encoding=5, byteorder='>')
        stream = obspy.read('tmp.sgy',unpack_trace_headers=True)
        os.remove('tmp.sgy')
        for trace_index, trace in enumerate(stream):
            trace.stats[input_format].trace_header.trace_sequence_number_within_line = trace_index+1 #tracl
            trace.stats[input_format].trace_header.trace_sequence_number_within_segy_file = trace_index+1 #tracr
            trace.stats[input_format].trace_header.original_field_record_number = ffid #fldr
            trace.stats[input_format].trace_header.trace_number_within_the_original_field_record = trace_index+1 #tracf
    
    if separate_sources:
        stream = separate_streams(stream)

    return stream

def check_format(stream):
    '''
    Check the input format of the stream.
    
    Parameters
    ----------
    stream : obspy.Stream
        The stream object containing the seismic data.
        
    Returns
    -------
    input_format : str
        The input format of the stream.
    '''

    if hasattr(stream[0].stats, 'su'):
        input_format = 'su'
    elif hasattr(stream[0].stats, 'segy'):
        input_format = 'segy'
    elif hasattr(stream[0].stats, 'seg2'):
        input_format = 'seg2'
    else:
        raise ValueError('The input format is not recognized')
    
    return input_format

def separate_streams(stream):
    '''
    Separate the traces into different streams based on the original_field_record_number.

    Parameters
    ----------
    stream : obspy.Stream
        The stream object containing the seismic data.

    Returns
    -------
    streams : list
        A list of streams, one for each source.
    '''
    
    # Check the input format
    input_format = check_format(stream)
        
    # Get the unique original_field_record_number values
    unique_record_numbers = sorted(list(set(trace.stats[input_format].trace_header.original_field_record_number for trace in stream)))
    
    # Initialize an empty list to store the shot gathers in different streams
    streams = []
    
    # Iterate over the unique record numbers
    for record_number in unique_record_numbers:
        # Select the traces with the current record number and add them to the list
        substream = obspy.Stream([trace for trace in stream if trace.stats[input_format].trace_header.original_field_record_number == record_number])
        streams.append(substream)
    
    return streams

# Custom classes
class CustomViewBox(pqg.ViewBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseDragEvent(self, ev, axis=None):
        if ev.button() == pqg.QtCore.Qt.LeftButton:
            self.setMouseMode(self.PanMode)  # Switch to pan mode
            ev.accept()  # Accept the event to handle it
            super().mouseDragEvent(ev, axis)
        elif ev.button() == pqg.QtCore.Qt.MiddleButton:
            self.setMouseMode(self.RectMode)
            super().mouseDragEvent(ev, axis)
        else:
            super().mouseDragEvent(ev, axis)

# Error Parameters Dialog
class ErrorParametersDialog(QDialog):
    def __init__(self, relativeError, absoluteError, maxRelativeError, minAbsoluteError, maxAbsoluteError, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Error Parameters")

        # Create layout
        layout = QVBoxLayout(self)

        # Create input fields
        self.relativeErrorLineEdit = self.createLineEdit(relativeError)
        self.absoluteErrorLineEdit = self.createLineEdit(absoluteError)
        self.maxRelativeErrorLineEdit = self.createLineEdit(maxRelativeError)
        self.minAbsoluteErrorLineEdit = self.createLineEdit(minAbsoluteError)
        self.maxAbsoluteErrorLineEdit = self.createLineEdit(maxAbsoluteError)

        # Add input fields to layout
        layout.addLayout(self.createFormItem("Relative Error:", self.relativeErrorLineEdit))
        layout.addLayout(self.createFormItem("Absolute Error:", self.absoluteErrorLineEdit))
        layout.addLayout(self.createFormItem("Max Relative Error:", self.maxRelativeErrorLineEdit))
        layout.addLayout(self.createFormItem("Min Absolute Error:", self.minAbsoluteErrorLineEdit))
        layout.addLayout(self.createFormItem("Max Absolute Error:", self.maxAbsoluteErrorLineEdit))

        # Add OK and Cancel buttons
        buttonLayout = QHBoxLayout()
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout.addLayout(buttonLayout)

        # Connect buttons
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)

    def createLineEdit(self, value):
        lineEdit = QLineEdit()
        if value is not None:
            lineEdit.setText(str(value))
        return lineEdit

    def createFormItem(self, label, widget):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(widget)
        return layout

    @property
    def relativeError(self):
        text = self.relativeErrorLineEdit.text()
        return float(text) if text else None

    @property
    def absoluteError(self):
        text = self.absoluteErrorLineEdit.text()
        return float(text) if text else None

    @property
    def maxRelativeError(self):
        text = self.maxRelativeErrorLineEdit.text()
        return float(text) if text else None

    @property
    def minAbsoluteError(self):
        text = self.minAbsoluteErrorLineEdit.text()
        return float(text) if text else None

    @property
    def maxAbsoluteError(self):
        text = self.maxAbsoluteErrorLineEdit.text()
        return float(text) if text else None

# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        centralWidget = QWidget()
        mainLayout = QHBoxLayout(centralWidget)  # Main horizontal layout
        self.setCentralWidget(centralWidget)

        # Create a horizontal QSplitter
        horSplitter = QSplitter(QtCore.Qt.Horizontal)

        # Create a vertical layout for the left side
        leftLayout = QVBoxLayout()

        # Create a QComboBox to select the display option
        self.displayOptionComboBox = QComboBox()
        self.displayOptionComboBox.addItems(["Filename", "Source Position", "FFID"])
        self.displayOptionComboBox.currentIndexChanged.connect(self.updateFileListDisplay)
        self.displayOptionComboBox.setMinimumSize(50, 30)  # Set minimum size for the QComboBox
        leftLayout.addWidget(self.displayOptionComboBox)

        # Create a QListWidget for file names and add it to the left
        self.fileListWidget = QListWidget()
        self.fileListWidget.itemSelectionChanged.connect(self.onFileSelectionChanged)
        self.fileListWidget.setMinimumSize(50, 200)  # Set minimum size for the QListWidget
        self.fileListWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Ensure it expands to fill space
        leftLayout.addWidget(self.fileListWidget)

        # Create a QWidget to hold the left layout and add it to the horizontal splitter
        leftWidget = QWidget()
        leftWidget.setLayout(leftLayout)
        horSplitter.addWidget(leftWidget)

        # Create a vertical QSplitter
        vertSplitter = QSplitter(QtCore.Qt.Vertical)

        # Create a top ViewBox for seismograms
        self.viewBox = CustomViewBox()
        self.viewBox.setBackgroundColor('w')
        self.viewBox.invertY(True)  # Invert the y-axis

        # Create a plot widget with the top ViewBox
        self.plotWidget = pqg.PlotWidget(viewBox=self.viewBox)
        self.plotWidget.setBackground('w')  # Set background color to white
        vertSplitter.addWidget(self.plotWidget)

        # Create the bottom ViewBox for the acquisition setup / traveltimes view
        self.bottomViewBox = CustomViewBox()
        self.bottomViewBox.setBackgroundColor('w')
        self.bottomViewBox.invertY(True)  # Invert the y-axis

        # Create a plot widget with the bottom ViewBox
        self.bottomPlotWidget = pqg.PlotWidget(viewBox=self.bottomViewBox)
        self.bottomPlotWidget.setBackground('w')  # Set background color to white
        vertSplitter.addWidget(self.bottomPlotWidget)

        # Set initial sizes for the splitters
        horSplitter.setSizes([25, 100])
        vertSplitter.setSizes([300, 300])

        # Add the vertical splitter to the horizontal splitter
        horSplitter.addWidget(vertSplitter)

        # Add the horizontal splitter to the main layout
        mainLayout.addWidget(horSplitter)

        # Resize the window to almost full screen
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() * 0.9), int(screen_size.height() * 0.9))  # Resize to 90% of the screen size

        # Alternatively, you can use the following line to maximize the window
        # self.showMaximized()

        # Set the title of the window
        self.statusBar = QStatusBar(self)
        permanentMessage = QLabel(self.statusBar)
        permanentMessage.setText('Sylvain Pasquet - 2024')
        self.statusBar.addPermanentWidget(permanentMessage)
        self.setStatusBar(self.statusBar)      

        # Connect the mouseClickEvent signal to the pickTime slot
        self.plotWidget.scene().sigMouseClicked.connect(self.pickTime)

        # Add a QLabel to the MainWindow
        self.label = QLabel(self)

        # Create a menu bar and add a File menu
        self.fileMenu = self.menuBar().addMenu('File')

        self.openFileAction = QAction('Open file(s)', self)
        self.fileMenu.addAction(self.openFileAction)
        self.openFileAction.triggered.connect(self.openFile)

        self.clearMemoryAction = QAction('Clear Memory', self)
        self.fileMenu.addAction(self.clearMemoryAction)
        self.clearMemoryAction.triggered.connect(self.clearMemory)

        # Create a menu bar and add a View menu
        self.viewMenu = self.menuBar().addMenu('View')

        # Create Menu for choosing bottom plot type
        self.bottomPlotSubMenu = self.viewMenu.addMenu('Bottom Plot Type')

        self.bottomPlotSetupAction = QAction('Source / Trace', self)
        self.bottomPlotSubMenu.addAction(self.bottomPlotSetupAction)
        self.bottomPlotSetupAction.triggered.connect(self.setPlotSetup)

        self.bottomPlotTravelTimeAction = QAction('Traveltimes', self)
        self.bottomPlotSubMenu.addAction(self.bottomPlotTravelTimeAction)
        self.bottomPlotTravelTimeAction.triggered.connect(self.setPlotTravelTime)

        # Create a submenu for x-axis plot types
        self.plotTypeSubMenu = self.viewMenu.addMenu('Plot traces by')

        self.tracePositionAction = QAction("Trace Position", self)
        self.plotTypeSubMenu.addAction(self.tracePositionAction)
        self.tracePositionAction.triggered.connect(self.setTracePosition)

        self.fileTraceNumberAction = QAction("File Trace Number", self)
        self.plotTypeSubMenu.addAction(self.fileTraceNumberAction)
        self.fileTraceNumberAction.triggered.connect(self.setFileTraceNumber)

        self.shotTraceNumberAction = QAction("Shot Trace Number", self)
        self.plotTypeSubMenu.addAction(self.shotTraceNumberAction)
        self.shotTraceNumberAction.triggered.connect(self.setShotTraceNumber)

        # Create a submenu for y-axis plot types
        self.plotTypeSubMenu = self.viewMenu.addMenu('Plot sources by')

        self.sourcePositionAction = QAction("Source Position", self)
        self.plotTypeSubMenu.addAction(self.sourcePositionAction)
        self.sourcePositionAction.triggered.connect(self.setSourcePosition)

        self.ffidAction = QAction("FFID", self)
        self.plotTypeSubMenu.addAction(self.ffidAction)
        self.ffidAction.triggered.connect(self.setFFID)

        self.offsetAction = QAction("Offset", self)
        self.plotTypeSubMenu.addAction(self.offsetAction)
        self.offsetAction.triggered.connect(self.setOffset)

        # Create QAction for resetting the view
        self.resetViewAction = QAction("Reset View", self)
        self.viewMenu.addAction(self.resetViewAction)
        self.resetViewAction.triggered.connect(self.resetSeismoView)
        self.resetViewAction.triggered.connect(self.resetBottomView)

        # Create a menu bar and add a Seismogram menu
        self.seismoMenu = self.menuBar().addMenu('Seismogram')

        # Create a submenu for wiggle plot options
        self.plotWiggleSubMenu = self.seismoMenu.addMenu('Amplitude Fill')

        self.fillPositiveAction = QAction("Fill positive amplitudes", self)
        self.plotWiggleSubMenu.addAction(self.fillPositiveAction)
        self.fillPositiveAction.triggered.connect(self.fillPositive)

        self.fillNegativeAction = QAction("Fill negative amplitudes", self)
        self.plotWiggleSubMenu.addAction(self.fillNegativeAction)
        self.fillNegativeAction.triggered.connect(self.fillNegative)

        self.noFillAction = QAction("No fill", self)
        self.plotWiggleSubMenu.addAction(self.noFillAction)
        self.noFillAction.triggered.connect(self.noFill)

        # Create a QAction for normalizing the traces
        self.normalizeAction = QAction("Normalize traces", self)
        self.seismoMenu.addAction(self.normalizeAction)
        self.normalizeAction.setCheckable(True)
        self.normalizeAction.setChecked(True)
        self.normalizeAction.triggered.connect((self.toggleNormalize))

        # Create a QAction for clipping the traces
        self.clipAction = QAction("Clip traces", self)
        self.seismoMenu.addAction(self.clipAction)
        self.clipAction.setCheckable(True)
        self.clipAction.setChecked(True)
        self.clipAction.triggered.connect((self.toggleClip))

        # Create a QAction for showing time samples
        self.showTimeSamplesAction = QAction("Show time samples", self)
        self.seismoMenu.addAction(self.showTimeSamplesAction)
        self.showTimeSamplesAction.setCheckable(True)
        self.showTimeSamplesAction.setChecked(False)
        self.showTimeSamplesAction.triggered.connect(self.toggleShowTimeSamples)

        # Create a QAction for setting the gain
        self.setGainAction = QAction("Set Gain", self)
        self.seismoMenu.addAction(self.setGainAction)
        self.setGainAction.triggered.connect(self.setGain)

        # Create a QAction for setting the maximum time 
        self.setMaxTimeAction = QAction("Set Maximum Time", self)
        self.seismoMenu.addAction(self.setMaxTimeAction)
        self.setMaxTimeAction.triggered.connect(self.setMaxTime)

        # Create a menu bar and add a Picks menu
        self.picksMenu = self.menuBar().addMenu('Picks')

        self.savePicksAction = QAction('Save Picks', self)
        self.picksMenu.addAction(self.savePicksAction)
        self.savePicksAction.triggered.connect(self.savePicks)

        self.loadPicksAction = QAction('Load Picks', self)
        self.picksMenu.addAction(self.loadPicksAction)
        self.loadPicksAction.triggered.connect(self.loadPicks)

        self.clearAllPicksAction = QAction('Clear All Picks', self)
        self.picksMenu.addAction(self.clearAllPicksAction)
        self.clearAllPicksAction.triggered.connect(self.clearAllPicks)

        self.clearCurrentPicksAction = QAction('Clear Current Picks', self)
        self.picksMenu.addAction(self.clearCurrentPicksAction)
        self.clearCurrentPicksAction.triggered.connect(self.clearCurrentPicks)

        self.setErrorParametersAction = QAction('Set Error Parameters', self)
        self.picksMenu.addAction(self.setErrorParametersAction)
        self.setErrorParametersAction.triggered.connect(self.setErrorParameters)

        self.setAllPickErrorAction = QAction('Set Errors For All Picks', self)
        self.picksMenu.addAction(self.setAllPickErrorAction)
        self.setAllPickErrorAction.triggered.connect(self.setAllPickError)

        # Create a Menu bar for exporting figures
        self.exportMenu = self.menuBar().addMenu('Export')

        self.exportSeismoAction = QAction('Export Seismogram', self)
        self.exportMenu.addAction(self.exportSeismoAction)
        self.exportSeismoAction.triggered.connect(self.exportSeismoPlot)

        # Initialize the variables
        self.clearMemory()

        # Update the file list display initially
        self.updateFileListDisplay()  
    
    def clearMemory(self):
        
        self.normalize = True
        self.polarity = 'negative'
        self.clip = True
        self.show_time_samples = False
        self.gain = 1
        self.mean_dx = 1
        self.bottomPlotType = 'setup'
        self.plotTypeX = 'shot_trace_number'
        self.plotTypeY = 'source_position'
        self.max_auto_load_files = 1000
        self.max_time = None
        self.col = 'k'
        self.x_label = 'Trace number in file'
        self.y_label = 'Source Position (m)'
        self.t_label = 'Time (s)'
        self.relativeError=0.05
        self.absoluteError=0
        self.maxRelativeError=None
        self.minAbsoluteError=None
        self.maxAbsoluteError=None

        self.plotWidget.clear()
        self.plotWidget.autoRange()
        self.viewBox.setLimits(xMin=None, xMax=None, yMin=None, yMax=None)
        self.bottomPlotWidget.clear()
        self.bottomPlotWidget.autoRange()
        self.bottomViewBox.setLimits(xMin=None, xMax=None, yMin=None, yMax=None)
        self.fileListWidget.clear()

        self.currentFileName = None
        self.currentIndex = None
        self.streamIndex = None
        self.stream = []
        self.fileNames = []
        self.streams = []
        self.time = []
        self.ffid = []
        self.source_position = []
        self.shot_trace_number = []
        self.trace_position = []
        self.file_trace_number = []
        self.offset = []
        self.picks = []
        self.error = []
        self.pickSeismoItems = []
        self.pickSetupItems = []

        # Example usage of the dictionary
        self.plotTypeDict = {
            'shot_trace_number': self.shot_trace_number,
            'file_trace_number': self.file_trace_number,
            'trace_position': self.trace_position,
            'source_position': self.source_position,
            'ffid': self.ffid,  
            'offset': self.offset
        }

    def updatePlotTypeDict(self):
        # Update the dictionary mapping plot types to attributes
        self.plotTypeDict = {
            'shot_trace_number': self.shot_trace_number,
            'file_trace_number': self.file_trace_number,
            'trace_position': self.trace_position,
            'source_position': self.source_position,
            'ffid': self.ffid,
            'offset': self.offset
        }

    def openFile(self, fileNames_new=None):
        if fileNames_new is None or not fileNames_new:
            fileNames_new, _ = QFileDialog.getOpenFileNames(self, "Open seismic file(s)", "", 
                                                        "Seismic files (*.seg2 *.dat *.segy *.sgy *.sg2 *.su)")
            
        firstNewFile = None
        counter_files = 0
        if fileNames_new:
            fileNames_new.sort(key=lambda x: self.extractFileNumber(os.path.basename(x)))  # Sort the new file paths by filename

            # Check if files are already in the list
            for i, fileName in enumerate(fileNames_new):
                if not fileName in self.fileNames:
                    counter_files += 1
                    
                    self.currentFileName = fileName
                    self.loadFile() # Load the file
                    
                    counter_stream = 0
                    for j in range(len(self.stream)):
                        if len(self.stream) > 1:
                            fileName = fileNames_new[i] + f'_{j+1}'
                        
                        if not fileName in self.fileNames:
                            counter_stream += 1
                            if firstNewFile is None: # Get the first new file
                                firstNewFile = fileName

                            self.currentIndex = len(self.fileNames) # Set the current index to the length of the file names list
                            self.currentFileName = fileName 
                            self.streamIndex = j

                            self.streams.append(None) # Add None to the streams list
                            self.fileNames.append(fileName) # Add the file path to the list
                            self.time.append(None)
                            self.ffid.append(None)
                            self.source_position.append(None)
                            self.offset.append(None)
                            self.trace_position.append(None)
                            self.shot_trace_number.append(None)
                            self.file_trace_number.append(None)
                            self.picks.append(None)
                            self.error.append(None)
                            self.pickSeismoItems.append(None) # Add an empty dictionary for the pick items on seismograms
                            self.pickSetupItems.append(None) # Add an empty dictionary for the pick items on setup plot

                            self.loadStream() # Load the file

                    if i == 0:
                        if self.max_time is None:
                            self.max_time = max(self.time[0])

                    if counter_stream > 0:           
                        self.currentFileName = firstNewFile
                        self.currentIndex = self.fileNames.index(firstNewFile)

            if counter_stream > 0:
                if counter_stream > 1:
                    print(f'{counter_files} file(s) succesfully loaded')
                    print(f'{counter_stream} streams succesfully loaded')
                else:
                    print(f'{counter_files} file(s) succesfully loaded')
            else:
                print('No new files loaded')

            self.sortFiles()  # Sort the files based on the file names
            self.sortFileList() # Sort the file list widget
            self.updatePlotTypeDict() # Update the plot type dictionary

    def loadFile(self):
        print(f"Loading file: {self.currentFileName}")
        # Load the seismic file
        self.stream = read_seismic_file(self.currentFileName, separate_sources=True)

    def loadStream(self):
        self.streams[self.currentIndex] = self.stream[self.streamIndex]
        self.getPlotParameters()

        # If it is the first time the file is loaded, update the sources and traces lists
        if self.picks[self.currentIndex] is None:
            # Initialize picks for the current file with a list of nans of the same length as the traces
            self.picks[self.currentIndex] = [np.nan] * len(self.trace_position[self.currentIndex])
            # Intialize errors for the current file with a list of nans of the same length as the traces
            self.error[self.currentIndex] = [np.nan] * len(self.trace_position[self.currentIndex])
            # Initialize the scatter items for the current file with list of empty lists of the same length as the traces
            self.pickSeismoItems[self.currentIndex] = [None] * len(self.trace_position[self.currentIndex])
            # Initialize the scatter items for the current file with list of empty lists of the same length as the traces
            self.pickSetupItems[self.currentIndex] = [None] * len(self.trace_position[self.currentIndex])

    def getPlotParameters(self):
        # Check the input format
        input_format = check_format(self.streams[self.currentIndex])
        # Get the trace numbers from the Stream
        shot_trace_number = [trace.stats[input_format].trace_header.trace_number_within_the_original_field_record 
                             for trace in self.streams[self.currentIndex]]
        # Get the file trace numbers from the Stream
        file_trace_number = np.arange(1, len(self.streams[self.currentIndex])+1)
        # Get the data and group coordinates from the Stream
        group_coordinates_x = [trace.stats[input_format].trace_header.group_coordinate_x / abs(trace.stats[input_format].trace_header.scalar_to_be_applied_to_all_coordinates) 
                               if trace.stats[input_format].trace_header.scalar_to_be_applied_to_all_coordinates < 0 
                               else trace.stats[input_format].trace_header.group_coordinate_x * trace.stats[input_format].trace_header.scalar_to_be_applied_to_all_coordinates 
                               for trace in self.streams[self.currentIndex]]
        
        # Check if group_coordinates_x has only zeros
        if np.all(np.array(group_coordinates_x) == 0):
            group_coordinates_x = file_trace_number

        # Get the source coordinate from the first trace
        source_coordinates_x = [trace.stats[input_format].trace_header.source_coordinate_x / abs(trace.stats[input_format].trace_header.scalar_to_be_applied_to_all_coordinates) 
                                if trace.stats[input_format].trace_header.scalar_to_be_applied_to_all_coordinates < 0 
                                else trace.stats[input_format].trace_header.source_coordinate_x * trace.stats[input_format].trace_header.scalar_to_be_applied_to_all_coordinates 
                                for trace in self.streams[self.currentIndex]]
        source_coordinate_x = np.unique(source_coordinates_x)[0]
        # Get the sample interval and delay from the first trace
        sample_interval = self.streams[self.currentIndex][0].stats[input_format].trace_header.sample_interval_in_ms_for_this_trace / 1_000_000 
        delay = self.streams[self.currentIndex][0].stats[input_format].trace_header.delay_recording_time/1000

        n_sample = len(self.streams[self.currentIndex][0].data)

        self.time[self.currentIndex] = np.arange(n_sample) * sample_interval + delay
        self.ffid[self.currentIndex] = self.streams[self.currentIndex][0].stats[input_format].trace_header.original_field_record_number
        self.offset[self.currentIndex] = [group_coordinates_x[i] - source_coordinate_x for i in range(len(group_coordinates_x))]
        self.source_position[self.currentIndex] = source_coordinate_x
        self.trace_position[self.currentIndex] = group_coordinates_x
        self.shot_trace_number[self.currentIndex] = shot_trace_number
        self.file_trace_number[self.currentIndex] = file_trace_number

    def sortFiles(self):
        # Sort files based on the file names
        # Original file paths
        fileNames = self.fileNames
        
        # Get sorted indices based on the file names
        sorted_indices = sorted(range(len(fileNames)), key=lambda i: self.extractFileNumber(os.path.basename(fileNames[i])))
        # Sort the file paths using the sorted indices
        self.fileNames = [fileNames[i] for i in sorted_indices]
        # Sort the streams using the sorted indices
        self.streams = [self.streams[i] for i in sorted_indices]
        # Sort the times using the sorted indices
        self.time = [self.time[i] for i in sorted_indices]
        # Sort the ffids using the sorted indices
        self.ffid = [self.ffid[i] for i in sorted_indices]
        # Sort the sources using the sorted indices
        self.source_position = [self.source_position[i] for i in sorted_indices]
        # Sort the offsets using the sorted indices
        self.offset = [self.offset[i] for i in sorted_indices]
        # Sort the trace positions using the sorted indices
        self.trace_position = [self.trace_position[i] for i in sorted_indices]
        # Sort the shot trace numbers using the sorted indices
        self.shot_trace_number = [self.shot_trace_number[i] for i in sorted_indices]
        # Sort the file trace numbers using the sorted indices
        self.file_trace_number = [self.file_trace_number[i] for i in sorted_indices]
        # Sort the picks using the sorted indices
        self.picks = [self.picks[i] for i in sorted_indices]
        # Sort the errors using the sorted indices
        self.error = [self.error[i] for i in sorted_indices]
        # Sort the scatter items using the sorted indices
        self.pickSeismoItems = [self.pickSeismoItems[i] for i in sorted_indices]
        # Sort the scatter items using the sorted indices
        self.pickSetupItems = [self.pickSetupItems[i] for i in sorted_indices]

    def extractFileNumber(self, filename):
        # Extract the numeric part from the filename
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')

    def sortFileList(self):
        self.fileListWidget.clear()  # Clear the list widget
        for fileName in self.fileNames: #: Add the file names to the list widget
            baseName = os.path.basename(fileName)
            self.fileListWidget.addItem(baseName)
        
        self.fileListWidget.setCurrentRow(self.currentIndex) # Set the current row to the current index

    def updateFileListDisplay(self):
        # Clear the current items in the QListWidget
        self.fileListWidget.clear()

        # Get the selected display option
        display_option = self.displayOptionComboBox.currentText()

        # Update the QListWidget based on the selected display option
        if display_option == "Filename":
            for file_path in self.fileNames:
                self.fileListWidget.addItem(os.path.basename(file_path))
        elif display_option == "Source Position":
            for source_position in self.source_position:
                self.fileListWidget.addItem(str(source_position))
        elif display_option == "FFID":
            for ffid in self.ffid:
                self.fileListWidget.addItem(str(ffid))

    def onFileSelectionChanged(self):
        # Get the selected item
        selectedItems = self.fileListWidget.selectedItems()
        # If an item is selected
        if selectedItems:
            selectedBaseName = selectedItems[0].text() # Get the text of the selected item
            
            # Find the index of the selected file path
            for index in range(self.fileListWidget.count()):
                # If the text of the item at the index is the same as the selected base name
                if self.fileListWidget.item(index).text() == selectedBaseName:
                    self.currentFileName = self.fileNames[index] # Set the current file name
                    self.currentIndex = index # Set the current index
                    break
            # Plot the selected file
            self.plotSeismo()
            self.plotBottom()

    def resetSeismoView(self):
        self.plotWidget.autoRange()
        self.plotWidget.getViewBox().setLimits(xMin=None, xMax=None, yMin=None, yMax=None)

        if self.streams:
            # Ensure the dictionary is updated
            self.updatePlotTypeDict()

            # Access the appropriate attribute based on self.plotTypeX
            plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])

            # Flatten the list of lists into a single list
            flat_plot_data_x = [item for sublist in plot_data_x for item in sublist]

            # Set x and y limits
            self.plotWidget.getViewBox().setXRange(min(flat_plot_data_x) - self.mean_dx, 
                                                max(flat_plot_data_x) + self.mean_dx)
            self.plotWidget.getViewBox().setYRange(min(self.time[self.currentIndex]), 
                                                self.max_time)
            # Set zoom limits
            self.plotWidget.getViewBox().setLimits(xMin=min(flat_plot_data_x) - self.mean_dx, 
                                                xMax=max(flat_plot_data_x) + self.mean_dx, 
                                                yMin=min(self.time[self.currentIndex]), 
                                                yMax=self.max_time)
            
    def resetBottomView(self):
        if self.bottomPlotType == 'setup':
            self.resetSetupView()
        elif self.bottomPlotType == 'traveltime':
            self.resetTravelTimeView()

    def resetSetupView(self):
        self.bottomPlotWidget.autoRange()
        self.bottomPlotWidget.getViewBox().setLimits(xMin=None, xMax=None, yMin=None, yMax=None)

        self.updatePlotTypeDict()
        
        if self.source_position:
            # Access the appropriate attribute based on self.plotTypeX (shot_trace_number, file_trace_number, trace_position)
            plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])
            # Flatten the list of lists into a single list
            flat_plot_data_x = [item for sublist in plot_data_x for item in sublist]

            # Access the appropriate attribute based on self.plotTypeY (source_position, ffid, offset)
            plot_data_y = self.plotTypeDict.get(self.plotTypeY, [])
            if self.plotTypeY == 'offset':
                flat_plot_data_y = [item for sublist in plot_data_y for item in sublist] # Flatten the list of lists into a single list
            else:
                flat_plot_data_y = plot_data_y
            
            # Get unique traces and sources from list of list of traces array that are not None
            traces = [trace for trace in flat_plot_data_x if trace is not None]
            sources = [source for source in flat_plot_data_y if source is not None]

            # Set x and y limits
            self.bottomPlotWidget.getViewBox().setXRange(min(traces) - self.mean_dx, 
                                                         max(traces) + self.mean_dx)
            self.bottomPlotWidget.getViewBox().setYRange(min(sources) - 1,
                                                         max(sources) + 1)
            self.bottomPlotWidget.getViewBox().setLimits(xMin=min(traces) - self.mean_dx,
                                                         xMax=max(traces) + self.mean_dx,
                                                         yMin=min(sources) - 1,
                                                         yMax=max(sources) + 1)
            
    def resetTravelTimeView(self):
        self.bottomPlotWidget.autoRange()
        self.bottomPlotWidget.getViewBox().setLimits(xMin=None, xMax=None, yMin=None, yMax=None)

        self.updatePlotTypeDict()
        
        if self.source_position:
            # Access the appropriate attribute based on self.plotTypeX (shot_trace_number, file_trace_number, trace_position)
            plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])
            # Flatten the list of lists into a single list
            flat_plot_data_x = [item for sublist in plot_data_x for item in sublist]

            # Access the appropriate attribute based on self.plotTypeY (source_position, ffid, offset)
            plot_data_y = self.picks
            # Flatten the list of lists into a single list
            flat_plot_data_y = [item for sublist in plot_data_y for item in sublist]

            # Get unique traces and times from list of list of traces array that are not None
            traces = [trace for trace in flat_plot_data_x if trace is not None]
            times = [time for time in flat_plot_data_y if time is not None]

            # Keep only the times where times is not Nan
            times = [time for time in times if not np.isnan(time)]

            # If there are no times, set the min time to 0 and max time to 1
            if not times:
                times = [np.min(self.time[self.currentIndex]), np.max(self.time[self.currentIndex])]
            
            # Set x and y limits
            self.bottomPlotWidget.getViewBox().setXRange(min(traces) - self.mean_dx, 
                                                         max(traces) + self.mean_dx)
            self.bottomPlotWidget.getViewBox().setYRange(min(times) - min(times)*0.1,
                                                         max(times) + max(times)*0.1)
            self.bottomPlotWidget.getViewBox().setLimits(xMin=min(traces) - self.mean_dx,
                                                            xMax=max(traces) + self.mean_dx,
                                                            yMin=min(times) - min(times)*0.1,
                                                            yMax=max(times) + max(times)*0.1)
    
    def setMaxTime(self):
        # Save the current locale
        original_locale = QLocale()
        # Set the locale to 'C' to use the dot as the decimal separator
        QLocale.setDefault(QLocale(QLocale.C))

        if self.max_time is None:
            self.max_time = 0.05

        # Open a dialog to set the maximum time to display
        self.max_time, ok = QInputDialog.getDouble(self, "Set Maximum Time", "Enter maximum time to plot (in s):",  
            decimals=2, value=self.max_time)
        
        # Restore the original locale
        QLocale.setDefault(original_locale)

        if ok:
            print(f"Maximum time set to {self.max_time} s")
            self.updatePlotWithMaxTime()

    def toggleClip(self):
        self.clip = self.clipAction.isChecked()
        if self.streams:
            self.plotSeismo()

    def toggleNormalize(self):
        self.normalize = self.normalizeAction.isChecked()
        if self.streams:
            self.plotSeismo()

    def toggleShowTimeSamples(self):
        self.show_time_samples = self.showTimeSamplesAction.isChecked()
        if self.streams:
            self.plotSeismo()

    def setGain(self):
        # Open a dialog to set the gain
        self.gain, ok = QInputDialog.getDouble(self, "Set Gain", "Enter gain:", 
            min=self.gain, decimals=2)
        if ok and self.streams:
            self.plotSeismo()

    def updatePlotWithMaxTime(self):
        # Update the plot to limit the y-axis to the specified maximum time
        self.plotWidget.getViewBox().setYRange(0, self.max_time)
        self.viewBox.setLimits(yMax=self.max_time)

    def setTracePosition(self):
        self.plotTypeX = 'trace_position'
        self.statusBar.showMessage('Switching to trace position',1000)
        if len(self.streams[self.currentIndex]) == 1:
            self.mean_dx = 1
        else:
            self.mean_dx = np.mean(np.diff(self.trace_position[self.currentIndex]))
        self.x_label = 'Trace Position (m)'
        if self.streams:
            self.plotSeismo()
            self.plotBottom()

    def setFileTraceNumber(self):
        self.plotTypeX = 'file_trace_number'
        self.statusBar.showMessage('Switching to file trace number',1000)
        self.mean_dx = 1
        self.x_label = 'Trace number in shot'
        if self.streams:
            self.plotSeismo()
            self.plotBottom()

    def setShotTraceNumber(self):
        self.plotTypeX = 'shot_trace_number'
        self.statusBar.showMessage('Switching to shot trace number',1000)
        self.mean_dx = 1
        self.x_label = 'Trace number in file'
        if self.streams:
            self.plotSeismo()
            self.plotBottom()

    def setSourcePosition(self):
        self.plotTypeY = 'source_position'
        self.statusBar.showMessage('Switching to source position',1000)
        self.y_label = 'Source Position (m)'
        if self.streams:
            self.plotBottom()

    def setFFID(self):
        self.plotTypeY = 'ffid'
        self.statusBar.showMessage('Switching to FFID',1000)
        self.y_label = 'FFID'
        if self.streams:
            self.plotBottom()

    def setOffset(self):
        self.plotTypeY = 'offset'
        self.statusBar.showMessage('Switching to offset',1000)
        self.y_label = 'Offset (m)'
        if self.streams:
            self.plotBottom()

    def LoadAllFiles(self):
        for filepath in self.fileNames:
            self.currentFileName = filepath
            self.loadFile()

        print(f'{len(self.fileNames)} files succesfully loaded.')

    def updatePickPosition(self, i):
        # Ensure the dictionary is updated
        self.updatePlotTypeDict()

        # Access the appropriate attribute based on self.plotTypeX
        plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])

        # Flatten the list of lists into a single list
        flat_plot_data_x = [item for sublist in plot_data_x for item in sublist]

        # Get the x position based on the plot type
        x_ok = flat_plot_data_x[i] if i < len(flat_plot_data_x) else None

        # Get the y position (assuming y_ok is already defined)
        y_ok = self.picks[self.currentIndex][i] if i < len(self.picks[self.currentIndex]) else None

        # Update the pick position if x_ok and y_ok are valid
        if x_ok is not None and y_ok is not None:
            self.pickSeismoItems[self.currentIndex][i].setData(x=[x_ok], y=[y_ok])

    def fillPositive(self):
        self.polarity = 'positive'
        self.statusBar.showMessage('Filling positive amplitudes',1000)
        if self.streams:
            self.plotSeismo()

    def fillNegative(self):
        self.polarity = 'negative'
        self.statusBar.showMessage('Filling negative amplitudes',1000)
        if self.streams:
            self.plotSeismo()

    def noFill(self):
        self.polarity = 'None'
        self.statusBar.showMessage('No fill',1000)
        if self.streams:
            self.plotSeismo()

    def updateTitle(self):
        if self.streams:
            title = f"FFID: {self.ffid[self.currentIndex]}  |  Source at {self.source_position[self.currentIndex]} m"
            self.plotWidget.getPlotItem().setTitle(title, size='12pt', color='k')

    def getWiggleInfo(self, i, trace):

        # Ensure trace.data is a NumPy array of floats
        trace_data = np.array(trace.data, dtype=float)

        if self.normalize:
            # Normalize to max value of 1 and scale by mean_dx/2
            normalized_trace_data = (trace_data / np.max(np.abs(trace_data))) * (self.mean_dx/2) * self.gain
        else: 
            normalized_trace_data = trace_data * self.gain

        # Clip the trace data
        if self.clip:
            normalized_trace_data = np.clip(normalized_trace_data, -(self.mean_dx/2), (self.mean_dx/2))

        # Access the appropriate attribute based on self.plotTypeX (shot_trace_number, file_trace_number, trace_position)
        plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])

        # Ensure offset is a float
        offset = float(plot_data_x[self.currentIndex][i])

        # Add the offset to the normalized trace data
        x = normalized_trace_data + offset

        # Get the fill level and put in a NumPy array of floats (in order to make the curve filling work)
        fillLevel = np.array(offset)

        # Create a mask for positive or negative amplitudes
        if self.polarity == 'positive':
            mask = x >= fillLevel
        elif self.polarity == 'negative':
            mask = x <= fillLevel
        else:
            mask = None

        # Interpolate points to ensure smooth transition
        x_interpolated = []
        t_interpolated = []
        for j in range(len(x) - 1):
            x_interpolated.append(x[j])
            t_interpolated.append(self.time[self.currentIndex][j])
            if mask is not None and mask[j] != mask[j + 1]:
                # Linear interpolation
                t_interp = self.time[self.currentIndex][j] + (self.time[self.currentIndex][j + 1] - self.time[self.currentIndex][j]) * (fillLevel - x[j]) / (x[j + 1] - x[j])
                x_interpolated.append(fillLevel)
                t_interpolated.append(t_interp)

        x_interpolated.append(x[-1])
        t_interpolated.append(self.time[self.currentIndex][-1])

        x_interpolated = np.array(x_interpolated)
        t_interpolated = np.array(t_interpolated)

        # Create arrays for the positive parts
        if self.polarity == 'positive':
            x_filled = np.where(x_interpolated >= fillLevel, x_interpolated, fillLevel)
        elif self.polarity == 'negative':
            x_filled = np.where(x_interpolated <= fillLevel, x_interpolated, fillLevel)
        else:
            x_filled = x_interpolated

        return x, x_filled, t_interpolated, fillLevel, mask

    def plotSeismo(self):

        # Clear previous plots
        self.plotWidget.clear()

        # Update the title
        self.updateTitle()

        # Set axis labels
        self.plotWidget.setLabel('left', self.t_label)
        self.plotWidget.setLabel('top', self.x_label)

        # Move x-axis to the top
        self.plotWidget.getAxis('bottom').setLabel('')
        self.plotWidget.getAxis('top').setLabel(self.x_label)
        self.plotWidget.showAxis('top')
        self.plotWidget.showAxis('bottom')
        self.plotWidget.showAxis('left')
        self.plotWidget.showAxis('right')

        # Display shot position and ffid in the title
        self.statusBar.showMessage(f'FFID: {self.ffid[self.currentIndex]} | Source at {self.source_position[self.currentIndex]} m')
        
        for i, trace in enumerate(self.streams[self.currentIndex]):
            
            # Get the wiggle info
            x, x_filled, t_interpolated, fillLevel, mask = self.getWiggleInfo(i, trace)

            # Plot the original curve
            if self.show_time_samples:
                self.plotWidget.plot(x, self.time[self.currentIndex], pen=self.col,
                                                 symbol='o', symbolBrush='k', symbolPen='k', symbolSize=2)
            else:
                self.plotWidget.plot(x, self.time[self.currentIndex], pen=self.col)

            # Plot the positive/negative part of the curve with fill
            if mask is not None:
                self.plotWidget.plot(x_filled, t_interpolated, pen=None, 
                                    fillLevel=fillLevel, fillBrush=(0, 0, 0, 150))

            # Plot the picks
            if not np.isnan(self.picks[self.currentIndex][i]):
                self.updatePickPosition(i)
                scatter = self.pickSeismoItems[self.currentIndex][i]
                self.plotWidget.addItem(scatter)

        self.resetSeismoView()  # Reset the plot 

    def pickTime(self, event):

        if event.button() == QtCore.Qt.LeftButton or event.button() == QtCore.Qt.MiddleButton:
            mousePoint = self.plotWidget.plotItem.vb.mapSceneToView(event.scenePos())
            x = mousePoint.x()
            y = mousePoint.y()
            
            # Get the current axis ranges
            x_range = self.plotWidget.plotItem.vb.viewRange()[0]
            y_range = self.plotWidget.plotItem.vb.viewRange()[1]

            # Access the appropriate attribute based on self.plotTypeX (shot_trace_number, file_trace_number, trace_position)
            plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])

            # Check if the clicked position is within the axis bounds
            if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                # Calculate the distance between the clicked point and the trace
                x_distance = np.array(plot_data_x[self.currentIndex]) - x
                y_distance = np.array(self.time[self.currentIndex]) - y

                # Get index of the closest trace
                index_x = np.argmin(np.abs(x_distance))
                index_y = np.argmin(np.abs(y_distance))

                # Get the x and y values of the closest trace
                x_ok = np.array(self.plotTypeDict[self.plotTypeX][self.currentIndex])[index_x]
                y_ok = np.array(self.time[self.currentIndex])[index_y]

                # Set the text of the QLabel to the clicked position
                self.label.setText(f"Clicked position: x = {x_ok}, y = {y_ok}")

                # If there's already a scatter plot item for this trace, update its position
                if self.pickSeismoItems[self.currentIndex][index_x] is not None:
                    if event.button() == QtCore.Qt.LeftButton:
                        self.pickSeismoItems[self.currentIndex][index_x].setData(x=[x_ok], y=[y_ok])
                        
                        self.picks[self.currentIndex][index_x] = y_ok # Update the pick
                        self.error[self.currentIndex][index_x] = self.pickError(y_ok) # Update the error
                        
                    else:
                        self.plotWidget.removeItem(self.pickSeismoItems[self.currentIndex][index_x])
                        self.pickSeismoItems[self.currentIndex][index_x] = None

                        self.picks[self.currentIndex][index_x] = np.nan # Remove the pick
                        self.error[self.currentIndex][index_x] = np.nan # Remove the error
                else:
                    if event.button() == QtCore.Qt.LeftButton:
                        # Otherwise, create a new scatter plot item and add it to the plot widget and the dictionary
                        scatter1 = pqg.ScatterPlotItem(x=[x_ok], y=[y_ok], pen='r', symbol='+')
                        self.plotWidget.addItem(scatter1)
                        self.pickSeismoItems[self.currentIndex][index_x] = scatter1

                        self.picks[self.currentIndex][index_x] = y_ok # Add the pick
                        self.error[self.currentIndex][index_x] = self.pickError(y_ok) # Add the error
                # Update the color map if there are picks that are not nan in all files
                if not np.isnan(self.picks).all():
                    self.createPicksColorMap()

                self.plotBottom() # Update the setup plot

    def setErrorParameters(self):
        # Open a dialog to set the error parameters where default values are the current values
        dialog = ErrorParametersDialog(self.relativeError, self.absoluteError, self.maxRelativeError, self.minAbsoluteError, self.maxAbsoluteError)
        if dialog.exec_():
            self.relativeError = dialog.relativeError
            self.absoluteError = dialog.absoluteError
            self.maxRelativeError = dialog.maxRelativeError
            self.minAbsoluteError = dialog.minAbsoluteError
            self.maxAbsoluteError = dialog.maxAbsoluteError
        
    def pickError(self, pick):
        
        error = pick * self.relativeError + self.absoluteError
        if self.maxAbsoluteError is not None:
            if error > self.maxAbsoluteError:
                error = self.maxAbsoluteError
        if self.minAbsoluteError is not None:
            if error < self.minAbsoluteError:
                error = self.minAbsoluteError
        if self.maxRelativeError is not None:
            if error > self.maxRelativeError * pick:
                error = self.maxRelativeError * pick

        return error
    
    def setAllPickError(self):
        # Set self.error to the error calculated from the picks
        for i, _ in enumerate(self.picks):
            for j, pick in enumerate(self.picks[i]):
                if not np.isnan(pick):
                    self.error[i][j] = self.pickError(pick)

    def createPicksColorMap(self):
        # Create a colormap
        colormap = pqg.colormap.get('Spectral_r',source='matplotlib')

        # Get the values of the picks that are not nan in a list of list
        values = [value for sublist in self.picks for value in sublist if not np.isnan(value)]

        # Normalize the values to the range [0, 1]
        min_val = min(values)
        max_val = max(values)
        if min_val == max_val:
            min_val = min_val - 1
            max_val = max_val + 1
        normalized_values = [(val - min_val) / (max_val - min_val) for val in values]

        # Map values to colors
        self.colors = colormap.map(normalized_values, mode='qcolor')

    def plotSetup(self):

        # Clear previous plots
        self.bottomPlotWidget.clear()

        # Flatten the traces and repeat sources
        x_all = []
        y_all = []
        pick_all = []
        
        for i, _ in enumerate(self.source_position):
            traces = self.plotTypeDict[self.plotTypeX][i]  # List of traces for the current source
            m = len(traces)  # Number of traces for the current source
            x_all.extend(traces)  # Add traces to x_values
            plot_y = self.plotTypeDict[self.plotTypeY] # List of sources for the current trace

            if self.plotTypeY == 'offset':
                y_all.extend(plot_y[i])
            else:
                y_all.extend([plot_y[i]] * m)
            pick_all.extend(self.picks[i])  # Add picks to pick_all

        scatter = pqg.ScatterPlotItem(x=x_all, y=y_all, symbol='o',
                                      brush =(0, 0, 0, 150), size=5) 
        self.bottomPlotWidget.addItem(scatter)        

        # If there are picks that are not nan, plot them with colors      
        x_pick = [x_all[i] for i in range(len(x_all)) if not np.isnan(pick_all[i])]
        y_pick = [y_all[i] for i in range(len(y_all)) if not np.isnan(pick_all[i])]

        if x_pick:
            # Create a colormap
            self.createPicksColorMap()

            # Create ScatterPlotItem with colors
            scatter = pqg.ScatterPlotItem(x=x_pick, y=y_pick, symbol='s', 
                                          brush=self.colors, pen=self.colors, size=8)
            self.bottomPlotWidget.addItem(scatter)

        # Add horizontal lines around the current source position
        if self.source_position:
            current_source = self.plotTypeDict[self.plotTypeY][self.currentIndex]
            first_trace = self.plotTypeDict[self.plotTypeX][self.currentIndex][0]
            last_trace = self.plotTypeDict[self.plotTypeX][self.currentIndex][-1]

            if len(self.source_position) > 1:
                if self.plotTypeY == 'offset':
                    first_y = current_source[0]
                    last_y = current_source[-1]
                    mean_dy = np.mean(np.abs(np.diff(self.plotTypeDict[self.plotTypeY][self.currentIndex])))
                else:
                    first_y = current_source
                    last_y = current_source
                    mean_dy = np.mean(np.abs(np.diff(self.plotTypeDict[self.plotTypeY])))

                x_line = [first_trace - self.mean_dx, last_trace + self.mean_dx]
                y_line_1 = [first_y - mean_dy, last_y - mean_dy]
                y_line_2 = [first_y + mean_dy, last_y + mean_dy]

                line1 = pqg.PlotDataItem(x_line, y_line_1, pen='k')
                line2 = pqg.PlotDataItem(x_line, y_line_2, pen='k')
                self.bottomPlotWidget.addItem(line1)
                self.bottomPlotWidget.addItem(line2)

        # Set axis labels
        self.bottomPlotWidget.setLabel('left', self.y_label)
        self.bottomPlotWidget.setLabel('top', self.x_label)
        self.bottomPlotWidget.showAxis('top')
        self.bottomPlotWidget.showAxis('bottom')
        self.bottomPlotWidget.showAxis('left')
        self.bottomPlotWidget.showAxis('right')

        # Reset the view
        self.resetSetupView()

    def plotTravelTime(self):

        # Clear previous plots
        self.bottomPlotWidget.clear()

        # Loop over the sources
        for i, _ in enumerate(self.source_position):
            # Check if the list of picks is not None or full of nans
            if self.picks[i] is not None and not np.isnan(self.picks[i]).all():
                
                # Plot trace position vs travel time with points and lines
                if i == self.currentIndex:
                    pen = pqg.mkPen('b', width=2)
                    # Plot the trace position vs travel time with different color
                    plot_item = pqg.PlotDataItem(x=self.plotTypeDict[self.plotTypeX][i], y=self.picks[i], 
                                                 symbol='+', pen=pen, symbolBrush='r', symbolPen='r', symbolSize=8)
                else:
                    # Plot the trace position vs travel time with default color
                    plot_item = pqg.PlotDataItem(x=self.plotTypeDict[self.plotTypeX][i], y=self.picks[i], 
                                                 symbol='o', pen='k', symbolBrush='k', symbolPen='k', symbolSize=2)
                self.bottomPlotWidget.addItem(plot_item)

        # Set axis labels
        self.bottomPlotWidget.setLabel('left', self.t_label)
        self.bottomPlotWidget.setLabel('top', self.x_label)
        self.bottomPlotWidget.showAxis('top')
        self.bottomPlotWidget.showAxis('bottom')
        self.bottomPlotWidget.showAxis('left')
        self.bottomPlotWidget.showAxis('right')

        # Reset the view
        self.resetTravelTimeView()

    def savePicks(self):
        # Save the picks to a pygimli .sgt file 

        # Get unique traces from list of list of traces array that are not None
        traces = [trace for sublist in self.trace_position if sublist is not None for trace in sublist]
        # Get unique sources from list of sources array
        sources = [source for source in self.source_position if source is not None]
        # Get unique stations from traces and sources
        stations = np.unique(np.concatenate((traces, sources)))
        # Get trace indices in station list
        trace_indices = [np.where(stations == trace)[0][0] for trace in traces]
        # Get source indices in station list
        source_indices = [np.where(stations == source)[0][0] for source in sources]

        # Number of non-NaN picks in the list of picks where list of picks is not None
        picks = [pick for sublist in self.picks if sublist is not None for pick in sublist]
        n_picks = np.sum(~np.isnan(picks))

        # Write file with the following format:
        # Number of stations
        # x, y, z coordinates of stations
        # Number of picks
        # Source index, trace index, pick time, pick error

        ### TODO
        # Add z coordinates of stations
        # Add pick errors
        # Remove unused stations (or not)

        if n_picks == 0:
            self.statusBar.showMessage('No picks to save!', 2000)
            return
        
        # The first argument returned is the filename and path
        fname, _ = QFileDialog.getSaveFileName(
            self, 'Save to file', filter='Source-Geophone-Time file (*.sgt)')
        
        if fname != "":
            with open(fname, 'w') as f:
                # Write number of stations
                f.write(f"{len(stations)} # shot/geophone points\n")
                f.write("# x\ty\n")
                for station in stations:
                    x = station
                    y = 0
                    f.write(f"{x}\t{y}\n")
                # Write number of picks
                f.write(f"{n_picks} # measurements\n")
                f.write("# s\tg\tt\terr\n")

                for i, pick_list in enumerate(self.picks):
                    if pick_list is not None:
                        for j, pick in enumerate(pick_list):
                            if not np.isnan(pick):
                                # Write source index, trace index, pick time, pick error
                                # format for time is in seconds with 5 decimal places
                                error = self.error[i][j]
                                f.write(f"{source_indices[i] + 1}\t{trace_indices[j] + 1}\t{pick:.5f}\t{error:.5f}\n")

            self.statusBar.showMessage(f'Picking saved at: {fname}.', 10000)
        else:
            self.statusBar.showMessage('No file saved!', 2000)

    def setPlotTravelTime(self):
        self.bottomPlotType = 'traveltime'
        self.statusBar.showMessage('Switching to traveltime plot',1000)
        if self.streams:
            self.plotTravelTime()

    def setPlotSetup(self):
        self.bottomPlotType = 'setup'
        self.statusBar.showMessage('Switching to source/trace diagram',1000)
        if self.streams:
            self.plotSetup()

    def plotBottom(self):
        if self.bottomPlotType == 'traveltime':
            self.plotTravelTime()
        elif self.bottomPlotType == 'setup':
            self.plotSetup()

    def loadPicks(self, fname=None, verbose=False):
        # Load picks from a pygimli .sgt file

        # The first argument returned is the filename and path
        if fname is None or not fname:
            fname, _ = QFileDialog.getOpenFileName(
                self, 'Open file', filter='Source-Geophone-Time file (*.sgt)')
        
        if fname != "":
            with open(fname, 'r') as f:
                # Read number of stations
                n_stations = int(f.readline().split('#')[0].strip())
                if verbose:
                    print(f"Number of stations: {n_stations}")

                # Read line and check if it is a comment
                flag_comment = True
                while flag_comment:
                    line = f.readline().strip()
                    
                    if '#' in line[0]:
                        if verbose:
                            print(f"Comment: {line}")
                        flag_comment = True
                    else:
                        flag_comment = False

                # Read x, y coordinates of stations
                uploaded_stations = []
                for i in range(n_stations):
                    if i>0:
                        line = f.readline().strip()

                    if verbose:
                        if i < 5 or i > n_stations - 5:
                            print(f"Reading station line: {line}")
                
                    if line:  # Check if the line is not empty
                        parts = line.split()
                        if len(parts) == 2:  # Ensure there are exactly two values
                            x, y = map(float, parts)
                            uploaded_stations.append((x, y))
                        elif len(parts) == 3:  # Ensure there are exactly three values
                            x, y, z = map(float, parts)
                            uploaded_stations.append((x, y, z))
                            
                # Read number of picks
                n_picks = int(f.readline().split('#')[0].strip())
                if verbose:
                    print(f"Number of picks: {n_picks}")

                # Read line and check if it is a comment
                flag_comment = True
                while flag_comment:
                    line = f.readline().strip()
                    
                    if '#' in line[0]:
                        if verbose:
                            print(f"Comment: {line}")
                        flag_comment = True
                        # Find order of s, g, t and err in comment line
                        if 's' in line:
                            s_ind = line.split().index('s') - 1
                        if 'g' in line:
                            g_ind = line.split().index('g') - 1
                        if 't' in line:
                            t_ind = line.split().index('t') - 1
                        if 'err' in line:
                            err_ind = line.split().index('err') - 1
                    else:
                        flag_comment = False

                # Read source index, trace index, pick time, pick error
                uploaded_picks = []
                for i in range(n_picks):
                    if i>0:
                        line = f.readline().strip()

                    if verbose:
                        if i < 5 or i > n_picks - 5:
                            print(f"Reading pick line: {line}")

                    if line:  # Check if the line is not empty
                        parts = line.split()
                        #### TODO 
                        # handle more or less values than 4
                        if len(parts) == 4:  # Ensure there are exactly four values (could be more or less)
                            # use the indices to get the values
                            source = int(parts[s_ind])
                            trace = int(parts[g_ind])
                            pick = float(parts[t_ind])
                            error = float(parts[err_ind])
                            uploaded_picks.append((source, trace, pick, error))

                self.statusBar.showMessage(f'Picking loaded from: {fname}.', 10000)    

            if self.currentFileName is not None:
                # Get current file index
                n_picks_total = 0
                n_sources_total = 0

                # Loop over files in self.fileNames
                for i, _ in enumerate(self.fileNames):
                    # Get the current source
                    source = self.source_position[i]

                    # Loop over uploaded picks
                    if source is not None:

                        # Find the source index in the uploaded stations
                        try:
                            source_index = np.where(np.array(uploaded_stations) == source)[0][0]
                        except IndexError:
                            print(f"Source {source} not found in uploaded_stations")
                            # Handle the case where the source is not found
                            source_index = None  # or any other appropriate action

                        # Find the corresponding picks for the current source
                        up_picks_tmp = [pick for pick in uploaded_picks if pick[0] == source_index + 1]
                
                        # Unpack the picks to get the trace indices, picks and errors
                        trace_indices = [int(pick[1]) - 1 for pick in up_picks_tmp]
                        picks = [pick[2] for pick in up_picks_tmp]
                        errors = [pick[3] for pick in up_picks_tmp]

                        if picks:
                            print(f"{len(picks)} picks loaded for source at {source} m")
                            n_picks_total += len(picks)
                            n_sources_total += 1

                        # Update the picks list
                        if self.picks[i] is None:
                            self.picks[i] = [np.nan] * len(self.trace_position[i])

                        # Access the appropriate attribute based on self.plotTypeX (shot_trace_number, file_trace_number, trace_position)
                        plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])

                        for trace_index_all, pick, error in zip(trace_indices, picks, errors):
                            # Get trace position from uploaded_stations
                            trace = uploaded_stations[trace_index_all][0]
                            # Find the trace index in the current file
                            trace_index_source = np.where(np.array(self.trace_position[i]) == trace)[0][0]

                            scatter1 = pqg.ScatterPlotItem(x=[plot_data_x[i][trace_index_source]], 
                                                          y=[pick], pen='r', symbol='+')

                            if i == self.currentIndex:
                                if ~np.isnan(self.picks[i][trace_index_source]):
                                    self.plotWidget.removeItem(self.pickSeismoItems[i][trace_index_source])
                                
                                self.plotWidget.addItem(scatter1)

                            self.pickSeismoItems[i][trace_index_source] = scatter1
                            self.picks[i][trace_index_source] = pick
                            self.error[i][trace_index_source] = error
                                                                
                print(f'{n_picks_total} picks loaded for {n_sources_total} sources')
                self.plotBottom()

        else:
            self.statusBar.showMessage('No file loaded!', 2000) 

    def clearAllPicks(self):
        # Reset all picks to nan
        for i, _ in enumerate(self.picks):
            if self.picks[i] is not None:
                for j, _ in enumerate(self.picks[i]):
                    self.picks[i][j] = np.nan
                    self.error[i][j] = np.nan
                    if self.pickSeismoItems[i][j] is not None:
                        self.plotWidget.removeItem(self.pickSeismoItems[i][j])
                        self.pickSeismoItems[i][j] = None
        self.plotBottom()

    def clearCurrentPicks(self):
        # Reset picks to nan for the current file
        if self.fileNames:
            if self.picks[self.currentIndex] is not None:
                for i, _ in enumerate(self.picks[self.currentIndex]):
                    self.picks[self.currentIndex][i] = np.nan
                    self.error[self.currentIndex][i] = np.nan
                    if self.pickSeismoItems[self.currentIndex][i] is not None:
                        self.plotWidget.removeItem(self.pickSeismoItems[self.currentIndex][i])
                        self.pickSeismoItems[self.currentIndex][i] = None
            self.plotBottom()
    
    def mplPlotSeismo(self):
        # Plot the seismogram using matplotlib
        aspect_ratio = (10,5)
        show_source = True
        fontsize = 12

        if self.streams:
            # Create a figure and axis
            _, ax = plt.subplots(figsize=aspect_ratio)

            if show_source:
                if self.plotTypeX == 'trace_position':
                    # Display a red star at the source location on the bottom x-axis
                    ax.scatter(self.source_position[self.currentIndex], 0, 
                            color='red', marker='*', s=100, transform=ax.get_xaxis_transform(), clip_on=False)
                else:
                    print('Source position not yet displayed for this plot type')
                
            for i, trace in enumerate(self.streams[self.currentIndex]):
                
                # Get the wiggle info
                x, _, _, _, mask = self.getWiggleInfo(i, trace)

                ax.plot(x, self.time[self.currentIndex], color='k',linewidth=0.5)
                ax.fill_betweenx(self.time[self.currentIndex], self.plotTypeDict[self.plotTypeX][self.currentIndex][i],
                                    x, where=mask, color='k', alpha=0.75, interpolate=True)

            # Access the appropriate attribute based on self.plotTypeX
            plot_data_x = self.plotTypeDict.get(self.plotTypeX, [])

            # Flatten the list of lists into a single list
            flat_plot_data_x = [item for sublist in plot_data_x for item in sublist]
        
            # Set the limits of the x and y axes
            ax.set_xlim(min(flat_plot_data_x) - self.mean_dx, max(flat_plot_data_x) + self.mean_dx)
            ax.set_ylim(min(self.time[self.currentIndex]), self.max_time)

            # Move the x-axis labels to the top
            ax.xaxis.tick_top()
            ax.xaxis.set_label_position('top')
            # Set the font size of the tick labels
            ax.tick_params(axis='both', labelsize=fontsize)
            # Invert the y-axis
            ax.invert_yaxis()  

            # Set the x-axis label and get its position
            ax.set_xlabel(self.x_label, fontsize=fontsize)
            # Set the y-axis label and get its position
            ax.set_ylabel('Time (s)', fontsize=fontsize)

            title = f"FFID: {self.ffid[self.currentIndex]}  |  Source at {self.source_position[self.currentIndex]} m"

            # Set the title
            plt.text(0.025, 0.05, title, fontsize=fontsize, ha='left', va='bottom', weight='bold',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'), transform=plt.gca().transAxes)

    def exportSeismoPlot(self):
        # Export the seismogram plot as an image with matplotlib

        # The first argument returned is the filename and path
        fname, _ = QFileDialog.getSaveFileName(
            self, 'Save to file', filter='PNG image (*.png)')
        
        if fname != "":
            # Create figure and axis with matplotlib
            self.mplPlotSeismo()

            # Save the figure
            plt.savefig(fname, dpi=300, bbox_inches='tight')


def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()