from __future__ import with_statement
from contextlib import contextmanager
from matplotlib import rcParams
import numpy as np
import scipy
import scipy.io
import xlrd
import csv
from matplotlib import gridspec
import matplotlib.pylab as plt
from pylab import *
import os
# import skimage.io as io
import pandas as pd

import time

def getData(strs):
    strings = strs
    numbs = strings.count('E')
    data = []
    for i in range(numbs):
        inde = strings.find('E')
        data.append(float(strings[inde-5:inde+3]))
        strings = strings.replace('E','Z',1)
    return data

def gettime(strings):
    hrs = float(strings[0:2])
    mins = float(strings[3:5])
    secs = float(strings[6:])
    datime = hrs*60+mins+secs/60.0
    return datime

def gettempData(strings):
    dinde0 = strings.find(',')
    strings = strings.replace(',','Z',1)
    dinde1 = strings.find(',')
    tempData = float(strings[dinde1+1:])
    return tempData



def getGaugeData(date, PathDir):
    file = PathDir + date+'\\maxigauge '+date+'.log'
    gaugeData = []
    datimes = []
    with open(file,'r') as f:
        while True:
            line1 = f.readline()
            if line1:
                recline = line1
                data = getData(line1)
                # print (line1[9:17])
                datime = gettime(line1[9:17])
                gaugeData.append(data)
                datimes.append(datime)
            else:
                print 'the latest time: ',date+','+recline[9:18]
                break
    datimes = datimes
    gaugeData = gaugeData
    return datimes, gaugeData
    
def getTempData(date, PathDir):
    
    filepath = PathDir + date + '\\'
    filenames = ['CH1 T '+date+'.log','CH2 T '+date+'.log','CH5 T '+date+'.log','CH6 T '+date+'.log']
    tempsfiles = [filepath + filename for filename in filenames]
    # return tempsfiles
    tempDataAll = []
    datimeAll = []
    
    channels = len(tempsfiles)
    for i in range(channels):
        tempDatas = []
        datimes = []
        try:
            with open(tempsfiles[i],'r') as f:

                while True:
                    line1 = f.readline()
                    if line1:
                        recline = line1
                        tempData = gettempData(line1[:-1])
                        # print (line1[10:18])
                        datime = gettime(line1[9:17])
                        tempDatas.append(tempData)
                        datimes.append(datime)
                    else:
                        print 'the latest time: ',date+','+recline[9:17]
                        break
        except:
            
            aa = tempsfiles[i]
            
            aa = aa.replace('T', 'R')
            
            with open(aa,'r') as f:
                while True:
                    line1 = f.readline()
                    if line1:
                        recline = line1
                        tempData = gettempData(line1[:-1])
                        # print (line1[10:18])
                        datime = gettime(line1[9:17])
                        tempDatas.append(tempData)
                        datimes.append(datime)
                    else:
                        print 'the latest time: ',date+','+recline[9:17]
                        break
        tempDataAll.append(tempDatas)
        datimeAll.append(np.array(datimes))
    tempDataAll = np.transpose(np.array(tempDataAll))
    datimeAll = np.transpose(np.array(datimeAll))
    
    return datimeAll, tempDataAll

def compareBlueForsGaugeAndTemp(date0=['22-07-18'], date1=['22-07-20'], figs=[None, None], doPlot=True, toff=0.0, alphas=[0.4,1.0], plotGauge=True, plotTemp=True):
    '''
    kaixuan
    20210409
    '''
    PathDir = 'C:\\SO01347\\log-data\\192.168.1.20\\'
    names = ['CAN','STIL','COND','P4','TANK','P6']
    names1 = ['50K', '4K', 'Still(700mK)', 'MC(10mK)']
    #####----------------------original data-----------------------------------
    datimes = []
    gaugeDatas = []
    tempDatas = []
    tempTimes = []
    for idx, datei in enumerate(date0):
        datime, gaugeData = getGaugeData(datei, PathDir)
        datime_, tempData = getTempData(datei, PathDir)
        if idx == 0:
            shift = 0
            shift1 = 0
        else:
            shift = datimes[-1]
            shift1 = np.array(tempTimes)[:,0][-1]
            
        datimes.extend((np.array(datime)+shift).tolist())
        # return np.array(datime_.tolist()), shift1
        tempTimes.extend((np.array(datime_)+shift1).tolist())
        
        gaugeDatas.extend(gaugeData)
        tempDatas.extend(tempData)
        
    gaugeDatas = np.array(gaugeDatas)   
    tempDatas = np.transpose(np.array(tempDatas)) 
    tempTimes = np.transpose(np.array(tempTimes)) +toff
    datimes = np.array(datimes)  + toff 

    #####----------------------new data-----------------------------------
    datimes_New = []
    gaugeDatas_New = []
    tempDatas_New = []
    tempTimes_New = []
    for jdx, datej in enumerate(date1):
        datime_New, gaugeData_New = getGaugeData(datej, PathDir)
        datime_New_, tempData_New = getTempData(datej, PathDir)
        if jdx == 0:
            shift = 0
            shift1 = 0
        else:
            shift = datimes_New[-1]
            shift1 = np.array(tempTimes_New)[:,0][-1]
        datimes_New.extend((np.array(datime_New)+shift).tolist())
        gaugeDatas_New.extend(gaugeData_New)
        tempDatas_New.extend(tempData_New)
        tempTimes_New.extend((np.array(datime_New_)+shift1).tolist())
        
    datimes_New = np.array(datimes_New) 
    gaugeDatas_New = np.array(gaugeDatas_New) 
    tempDatas_New = np.transpose(np.array(tempDatas_New))
    tempTimes_New = np.transpose(np.array(tempTimes_New))
    #####----------------------plotdata-----------------------------------
    
    if doPlot:
        if plotGauge:
            plt.figure(figs[0],figsize=(10,9))
            plt.subplot(321)
            plt.plot(datimes,gaugeDatas[:,0],'c.-',alpha=alphas[0], label=str(date0))
            plt.plot(datimes_New,gaugeDatas_New[:,0],'r.-',alpha=alphas[1], label=str(date1))
            plt.legend(loc=0)
            plt.title(names[0]+'(P1)', size=18)
            ylabel('Pressure(mBar)', size=16)
            plt.grid(True)
            
            plt.subplot(322)
            plt.plot(datimes,gaugeDatas[:,1],'c.-',alpha=alphas[0], label=str(date0))
            plt.plot(datimes_New,gaugeDatas_New[:,1],'r.-',alpha=alphas[1], label=str(date1))
            
            plt.title(names[1]+'(P2)', size=18)
            plt.grid(True)
            plt.subplot(323)
            plt.plot(datimes,gaugeDatas[:,2],'c.-',alpha=alphas[0], label=str(date0))
            plt.plot(datimes_New,gaugeDatas_New[:,2],'r.-',alpha=alphas[1], label=str(date1))
            plt.title(names[2]+'(P3)', size=18)
            ylabel('Pressure(mBar)', size=16)
            plt.grid(True)
            plt.subplot(324)
            plt.plot(datimes,gaugeDatas[:,3],'c.-',alpha=alphas[0], label=str(date0))
            plt.plot(datimes_New,gaugeDatas_New[:,3],'r.-',alpha=alphas[1], label=str(date1))
            plt.title(names[3], size=18)
            plt.grid(True)
            plt.subplot(325)
            plt.plot(datimes,gaugeDatas[:,4],'c.-',alpha=alphas[0], label=str(date0))
            plt.plot(datimes_New,gaugeDatas_New[:,4],'r.-',alpha=alphas[1], label=str(date1))
            plt.title(names[4]+'(P5)', size=18)
            ylabel('Pressure(mBar)', size=16)
            plt.grid(True)
            xlabel('Time (min)', size=16)
            plt.subplot(326)
            plt.plot(datimes,gaugeDatas[:,5],'c.-',alpha=alphas[0], label=str(date0))
            plt.plot(datimes_New,gaugeDatas_New[:,5],'r.-',alpha=alphas[1], label=str(date1))
            plt.title(names[5], size=18)
            plt.grid(True)
            xlabel('Time (min)', size=16)
            plt.show()
            plt.tight_layout()
    
        if plotTemp:
            plt.figure(figs[1], figsize=(10,9))
            plt.subplot(221)
            plt.plot(tempTimes[0],tempDatas[0],'c.-',label=str(date0)+'(50K)',alpha=alphas[0])
            plt.plot(tempTimes_New[0],tempDatas_New[0],'b.-',label=str(date1)+'(50K)',alpha=alphas[1])
            plt.title(names1[0], size=18)
            ylabel('Temperature(K)', size=16)
            plt.legend(loc=0)
            plt.grid(True)
            plt.subplot(222)
            plt.plot(tempTimes[1],tempDatas[1],'c.-',label=str(date0)+'(4K)',alpha=alphas[0])
            plt.plot(tempTimes_New[1],tempDatas_New[1],'y.-',label=str(date1)+'(4K)',alpha=alphas[1])
            plt.title(names1[1], size=18)
            plt.legend(loc=0)
            plt.grid(True)
            plt.subplot(223)
            plt.plot(tempTimes[2],tempDatas[2],'c.-',label=str(date0)+'(Still-700mK)',alpha=alphas[0])
            plt.plot(tempTimes_New[2],tempDatas_New[2],'k.-',label=str(date1)+'(Still-700mK)',alpha=alphas[1])
            plt.title(names1[2], size=18)
            ylabel('Temperature(K)', size=16)
            plt.legend(loc=0)
            xlabel('Time (min)', size=16)
            plt.grid(True)
            plt.subplot(224)
            plt.plot(tempTimes[3],tempDatas[3],'c.-',label=str(date0)+'(MC-10mK)',alpha=alphas[0])
            plt.plot(tempTimes_New[3],tempDatas_New[3],'r.-',label=str(date1)+'(MC-10mK)',alpha=alphas[1])
            plt.title(names1[3], size=18)
            plt.legend(loc=0)
            plt.grid(True)
            xlabel('Time (min)', size=16)
            plt.show()
            plt.tight_layout()
    return  datimes