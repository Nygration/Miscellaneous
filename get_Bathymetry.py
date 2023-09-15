## copied from an example on https://oceanpython.org/2013/03/21/bathymetry-topography-srtm30/ to be modified for my needs
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import requests
from mpl_toolkits import mplot3d
import cmocean
from scipy import interpolate
import warnings
warnings.filterwarnings("ignore") ######### THIS SUPPRESSES ALL WARNINGS, COMMENT OUT AS NEEDED #############

def get_Bathymetry(targetlat,targetlon,showmap=False,showtext=True):
    if showmap:
        minlat = targetlat-0.5
        maxlat = targetlat+0.5
        minlon = targetlon-0.5
        maxlon = targetlon+0.5
    else:
        ## find the bathymetery (or elevation for a given lat/lon pair)
        minlat = targetlat-0.125
        maxlat = targetlat+0.125
        minlon = targetlon-0.125
        maxlon = targetlon+0.125

    # Read data from: http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.html
    response = requests.get('http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.csv?topo[(' \
                                +str(maxlat)+'):1:('+str(minlat)+')][('+str(minlon)+'):1:('+str(maxlon)+')]', verify=False);
    
    raw =response.content.decode('utf-8');
    lines = raw.split('\n');
    lat, lon, topo = [],[],[];
    for line in lines[2:]:
        try:
            parts =line.split(',');
            lat.append(float(parts[0]));
            lon.append(float(parts[1]));
            topo.append(float(parts[2]));
        except:
            continue
    if showmap:
        alat =np.array(lat).reshape(121,121);
        alon =np.array(lon).reshape(121,121);
        atopo = np.array(topo).reshape(121,121);
    else:
        alat =np.array(lat).reshape(31,31);
        alon =np.array(lon).reshape(31,31);
        atopo = np.array(topo).reshape(31,31);
    # interpolate 
    tck = interpolate.bisplrep(alat, alon, atopo, s=0.1)
    znew = interpolate.bisplev(targetlat, targetlon, tck)
    znew
    
    if showmap:
        plt.figure(figsize=(10,10))
        ax = plt.axes(projection='3d')
        #ax.scatter3D(lon,lat,topo,c=-topo,cmap='cmo.deep',s=0.5)
        ax.plot_surface(alon,alat,atopo, cmap='cmo.deep', edgecolor='none', zorder =10) # rstride=1, cstride=1
        ax.plot3D([targetlon,targetlon],[targetlat,targetlat],[atopo[60,60],np.max(atopo)],'k',linewidth=2, zorder =10)
        #ax.scatter3D(targetlon,targetlat,atopo[60,60],c='black', s=50,zorder =50)
        plt.xlabel('longitude')
        plt.ylabel('latitude')
    
        if showtext: 
            print(f'Closest model point is at {alat[60,60]}, {alon[60,60]} with a depth of {atopo[60,60]} meters.\nSpline interpolated depth estimate for {targetlat}, {targetlon} is {znew:3.2f} meters.')
        return np.round(znew,2)
    
    else:
        if showtext: # if map is not shown the indexing changes
            print(f'Closest measurement is at {alat[15,15]}, {alon[15,15]} with a depth of {atopo[15,15]} meters.\nSpline interpolated depth estimate for {targetlat}, {targetlon} is {znew:3.2f} meters.')
        return np.round(znew,2)


def minsec2dd(deg,mmm,sss):
    return (deg+ ((mmm+ (sss/60))/60))