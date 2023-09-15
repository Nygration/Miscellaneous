import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib
import datetime
import cmocean
import matplotlib.dates as mdates

import keysort

def csvshow(target1):
    ## for a generalized function to view the data in CSV files obtained from OceansMonitor 
    # target1 is the path to the file to view
    df = pd.read_csv(target1)
    keys = df.keys()
    sortnum = keysort(target1)
    dts=[]
    for dt in df[keys[0]][:]:
        dts.append(datetime.datetime.fromisoformat(dt)) # get the data times 
    fig = plt.figure(figsize=(10,5))
    match sortnum:
        case 0:
            print ('did not recognize the file naming convention')
        case 1:
            depths = [float(iii[:-2]) for iii in keys[1:]] # first key is Datetime, the rest are depths (for currents)
            if len(depths)==1: # surface currents from Miros
                plt.plot(dts,df[keys[1]][:])
                plt.title('Miros Surface Current Direction')
                plt.xlabel('Time [Date]')
                plt.ylabel('Direction [°]')
                plt.ylim((0,360))
                ax=plt.gca()
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
                fig.autofmt_xdate()
            
            else:
                ddd = np.array(df)
                ddd=ddd[:,1:].T
                dt_grid,depth_grid = np.meshgrid(dts,depths)
                plt.pcolor(dt_grid,-depth_grid,ddd.astype(np.float32),cmap='cmo.phase')
                plt.colorbar()
                plt.ylabel('Depth')
                plt.xlabel('Time [Date]')
                plt.title('Direction')
                ax=plt.gca()
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
                fig.autofmt_xdate()
            
        case 2:
            depths = [float(iii[:-2]) for iii in keys[1:]] # first key is Datetime, the rest are depths (for currents)
            if len(depths)==1: # surface currents from Miros
                plt.plot(dts,df[keys[1]][:])
                plt.title('Miros Surface Current Speed')
                plt.xlabel('Time [Date]')
                plt.ylabel('Speed [m/s]')
                ax=plt.gca()
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
                fig.autofmt_xdate()
            
            else:
                ddd = np.array(df)
                ddd=ddd[:,1:].T
                dt_grid,depth_grid = np.meshgrid(dts,depths)
                plt.pcolor(dt_grid,-depth_grid,ddd.astype(np.float32),cmap='cmo.speed')
                plt.colorbar()
                plt.ylabel('Depth')
                plt.xlabel('Time [Date]')
                plt.title('Speed')
                ax=plt.gca()
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
                fig.autofmt_xdate()
            
        case 3: # wave directions
#             Dp = keys[1];
#             Dm = keys[2];
#             Dp1 = keys[3];
#             Dm1 = keys[4];
#             Dp2 = keys[5];
#             Dm2 = keys[6];
            for key in keys[1:]:
                plt.plot(dts, df[key][:],alpha=0.5)
            plt.legend(['Dp','Dm','Dp1','Dm1','Dp2','Dm2'])
            plt.ylabel('Direction [°]')
            plt.xlabel('Time [Date]')
            plt.title('Miros Wave Directions')
            ax=plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
            fig.autofmt_xdate()

        case 4: # wave heights
#             Hm0 = keys[1];
#             Hmax = keys[2];
            for key in keys[1:]:
                plt.plot(dts, df[key][:],alpha=0.75)
            plt.legend(['Hm0', 'Hmax'])
            plt.ylabel('Height [m]]')
            plt.xlabel('Time [Date]')
            plt.title('Miros Wave Heights')
            ax=plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
            fig.autofmt_xdate()
            
        case 5: # wave periods
#             Tp = keys[1];
#             Tmax = keys[2];
#             Tp1 = keys[3];
#             Tp2 = keys[4];
            for key in keys[1:]:
                plt.plot(dts, df[key][:],alpha=0.5)
            plt.legend(['Tp', 'Tmax', 'Tp1', 'Tp2'])
            plt.ylabel('Height [m]]')
            plt.xlabel('Time [Date]')
            plt.title('Miros Wave Heights')
            ax=plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H%M'))
            fig.autofmt_xdate()            

        case _:
            print ('sort number was not recognized')
