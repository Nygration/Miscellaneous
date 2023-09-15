def hycom_hindcast(tlat,tlon,ttime,tdep=0):
    import numpy as np
    import datetime
    import urllib
    import warnings
    warnings.filterwarnings("ignore") ######### THIS SUPPRESSES ALL WARNINGS, COMMENT OUT AS NEEDED #############
    import hycomlinesplit
    
    ## provide a lat, lon, and time, (after Dec 4,2018 1200 if you want it to work)
    ## time should be a string in iso format as YYYY-MM-DD or YYYY-MM-DDTHH:mm:ss
    ## remember that the time resolution is every 3 hours, so there is no sense in trying to pull minute or second resolution data
    ## the lat lon resolution is less obvious so you may want minute(/second?) data depending on how fast the asset is moving
#     laturl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?lat%5B0:1:4250%5D'
#     lonurl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?lon%5B0:1:4499%5D'
#     timeurl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?time%5B0:1:11048%5D'
#     depurl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?depth%5B0:1:39%5D'
    if tlon<0:
        tlon=tlon+360 # range 0-360 instead of -180 to 180
    startdt = datetime.datetime.fromisoformat(ttime)
    ttime = (startdt - datetime.datetime(2000,1,1,0,0,0)).total_seconds()/3600 # match units for the HYCOM API

    
    laturl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?lat'
    lonurl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?lon'
    timeurl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?time'
    depurl = 'http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?depth'    
    urllist = [laturl,lonurl,timeurl,depurl]
    
    labellist = ['latitude', 'longitude', 'time', 'depth']
    
    latlist = [] ## degrees
    lonlist = [] ## degrees
    timelist = [] ## hours since Jan 1, 2000
    deplist = [] ## meters
    listlist=[latlist,lonlist,timelist,deplist]

    for urlidx,uuu in enumerate(urllist):
        rrr0 = urllib.request.Request(uuu)
        rrr1 = urllib.request.urlopen(rrr0)
        data = (rrr1.read())
        data = data.decode()
        parts = data.split('\n')
        strlist = parts[5].split(',')
        for sss in strlist:
            listlist[urlidx].append(float(sss))
        #print(f"Done pulling {labellist[urlidx]} indexes")
    
    latlist = np.array(latlist)
    lonlist = np.array(lonlist)
    timelist = np.array(timelist)
    deplist = np.array(deplist)
    
    ### this is where the loop should start if the inputs are arrays instead of scalars.
    
    lonidx = [idx for idx,val in enumerate(np.abs(lonlist-tlon)) if val == np.min(np.abs(lonlist-tlon))][0]
    latidx = [idx for idx,val in enumerate(np.abs(latlist-tlat)) if val == np.min(np.abs(latlist-tlat))][0]
    timeidx = [idx for idx,val in enumerate(np.abs(timelist - ttime)) if val == np.min(np.abs(timelist-ttime))][0]
    if tdep==0:
        depidx = f"0:1:{len(deplist)-1}"; # all bins
    else:
        depidx = [idx for idx,val in enumerate(np.abs(deplist - tdep)) if val == np.min(np.abs(deplist-tdep))][0]
    #print(f'Done with Depth index')
    
    uurl = f"http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?water_u[{timeidx}][{depidx}][{latidx}][{lonidx}]"
    vurl = f"http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0.ascii?water_v[{timeidx}][{depidx}][{latidx}][{lonidx}]"
    urllist=[uurl,vurl]
    #print(urllist)
          
    ulist=[]
    vlist=[]
    currentlist=[]
    
    for urlidx,uuu in enumerate(urllist):
        rrr0 = urllib.request.Request(uuu)
        rrr1 = urllib.request.urlopen(rrr0)
        data = (rrr1.read())
        data = data.decode()
        parts = data.split('\n\n') # split by section (cuts off the indexes at the end)
        lines = parts[0].split('\n')[12:] ## using 12 provides the shape of the data being returned
        result = hycomlinesplit(lines)
        currentlist.append(result)
                
    ulist = currentlist[0]
    vlist = currentlist[1]
    print(f"Results are of shape {np.shape(ulist)}")
    return listlist,currentlist