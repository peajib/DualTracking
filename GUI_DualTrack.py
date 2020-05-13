# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic 
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import numpy as np
import pandas as pd
import sys
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.style
import matplotlib as mpl
mpl.style.use('seaborn-bright')

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('DualTrack_Analyzer_simple2.ui',self)
        self.show()
        self.title = 'CICADA Dual Tracking Analysis'
        self.setWindowTitle(self.title)
    
        self.fig, (self.ax1,self.ax2,self.ax3) = plt.subplots(3,2)
        #self.ax1[0].plot()
        #self.ax2[0].plot()

                
        self.fig.tight_layout()
        #self.ax.plot(np.random.rand(5)) 
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.gridLayout.addWidget(self.canvas)
        self.gridLayout.addWidget(self.toolbar)

        self.canvas.draw()
        self.canvas.flush_events()
        #self.toolbar = NavigationToolbar(self.canvas,self.mplwindow1,coordinates=True)
        #self.mplvl.addWidget(self.toolbar)

        self.actionExit.triggered.connect(self.exit)
        self.actionOpen.triggered.connect(self.openf)
        self.actionOpen.setStatusTip('Click here to open a file')
        
        
    def openf(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        self.fname_loaded.setText(fileName)
        
        if fileName:
            print(fileName)
            self.data = pd.read_fwf(fileName)
            #self.textEdit.setText('Basic info: \n'+str(self.data.size)+' elements\n'+ str(self.data.shape[0])+' rows \n'+ str(self.data.shape[1])+' columns')
            #self.columns.setText(str(self.data.dtypes))
            #self.lineEdit.setText(fileName)
        else:
            print('no file selected')
        
        #self.ax1.clear()
        #self.ax2.clear()
        #self.ax3.clear()
        
        t = self.data['PollTime']
        t = t - t[0]
        Xdefl = self.data['X-defl']*1000
        Ydefl = self.data['Y-defl']*1000
        Az = self.data['CurGimAz']
        El = self.data['CurGimEl']    
        NFOV_power = self.data['NFOV-Pwr']
        NFOV_XErr = self.data['NFOV-X']
        NFOV_YErr = self.data['NFOV-Y']
        APD_current = self.data['APD-Cur']
        
        plt.gcf().subplots_adjust(bottom=0.15)
        self.ax1[0].plot(t,Xdefl)
        #self.ax1[0].set_xlabel('PollTime [s]')
        self.ax1[0].set_ylabel('X Deflection [mrad]')

        self.ax1[1].plot(t,Ydefl,color='red')
        #self.ax1[1].set_xlabel('PollTime [s]')
        self.ax1[1].set_ylabel('Y Deflection [mrad]')

        self.ax2[0].plot(t,Az)
        #self.ax2[0].set_xlabel('PollTime [s]')
        self.ax2[0].set_ylabel('Gimbal Azimuth')

        self.ax2[1].plot(t,El,color='red')
        #self.ax2[1].set_xlabel('PollTime [s]')
        self.ax2[1].set_ylabel('Gimbal Elevation')
        
        self.ax3[0].plot(t,NFOV_XErr/NFOV_power)
        self.ax3[0].plot(t,NFOV_YErr/NFOV_power,color='red',alpha=0.7)
        self.ax3[0].set_xlabel('PollTime [s]')
        self.ax3[0].set_ylabel('NFOV x/y error [norm]')
        
        self.ax3[1].plot(t,NFOV_power)
        self.ax3[1].set_xlabel('PollTime [s]')
        self.ax3[1].set_ylabel('NFOV Total Power')
        #plt.plot(t,Xdefl)
        
        self.canvas.draw()

    

        
                
    def exit(self):
        QtWidgets.QApplication.exit()
        
                
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()





