## Written by CJN on 20220617 to mimic the matlab function
# this will grab hycom data for given Lat/lon coordinates


def get_Hycom(targetlat, targetlon):
## this will grab the most recent (yesterday noon?) Hycom model output for a lat/lon pair
    import numpy as np
    import datetime.datetime as dt
    import netCDF4 as nc
    import 

    now = dt.datetime.now(dt.timezone.utc)
    time_base = now - dt.timedelta(days=6, hours=(now.hour -12), minutes = now.minute, seconds = now.second, microseconds = now.microsecond) # basis for time in the nc file.
    t = now - dt.timedelta(days=1)
    url = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0/FMRC/runs/GLBy0.08_930_FMRC_RUN_' + str(t.year) + '-' + str(t.month).zfill(2) + '-' + str(t.day).zfill(2) + 'T12:00:00Z';
    ds = nc.Dataset(url) # get the data set

    real_time = [time_base + dt.timedelta(hours=ttt) for ttt in list(ds['time'][:])] # convert hours from basis to datetimes.

    real_time = np.array(real_time)
    depths = np.array(ds['depth'][:]) #0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 125.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1250.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0
    lon = np.array(ds['lon'][:])
    lon = ((lon+180)%360)-180 # shift to -180 to 180
    lat = np.array(ds['lat'][:])
    #longrid,latgrid = np.meshgrid(lon,lat) # this can take a while, visualization of it will also take time # also this isn't helpful
    #dist_to_target = (lon_grid-targetlon)**2 + (lat_grid-targetlat)**2) # only used to find index, no need to find the square root

    latidx = list((lat-targetlat)**2).index(min((lat-targetlat)**2))
    lonidx = list((lon-targetlon)**2).index(min((lon-targetlon)**2))

    uu =ds['water_u'][:,:,latidx,lonidx].T
    vv =ds['water_v'][:,:,latidx,lonidx].T

    return(uu,vv,real_time,depths)
    