import netCDF4 as nc
import numpy as np


def get_Hs(qqq):
    # qqq is a list of wave hieghts (use either t2p or p2t )
    www=qqq
    www.sort()
    ordered=list(www)
    ordered.reverse()
    top3rd = int(np.floor(len(qqq)/3))
    return np.mean(ordered[:top3rd])

def find_rogues(qqq):
    ## qqq is a raw .nc file path
    ds = nc.Dataset(qqq)
    records = ds.variables['VertDisp'].shape[0]
    #record_length = ds.variables['VertDisp'].shape[1]
    rogue_up=[]
    rogue_down=[]
    for rec_idx in np.arange(records):
        #print(f'Working on record #: {rec_idx}')
        zzz = ds.variables['VertDisp'][rec_idx,:]
        h_up,h_down = waveheights2(zzz)
        hs_up = get_Hs(h_up)
        hs_down = get_Hs(h_down)
        hmax_up = np.max(h_up)
        hmax_down = np.max(h_down)
        if hmax_up/hs_up >= 2:
            rogue_up.append(rec_idx)
        if hmax_down/hs_down >=2:
            rogue_down.append(rec_idx)
            
    return rogue_up,rogue_down

def waveheights(www):
    peaks = [idx for idx in np.arange(1,len(www)-1) if (www[idx]>www[idx-1]) and (www[idx]>www[idx+1]) and (www[idx]>0)] # in dexes of troughs (>0)
    troughs = [idx for idx in np.arange(1,len(www)-1) if (www[idx]<www[idx-1]) and (www[idx]<www[idx+1]) and (www[idx]<0)] # indexes of troughs (<0)
    
    pf =0 # peaks first boolean
    pl =0 # peaks last boolean
    
    ## determine which starts the record and which ends the record
    if peaks[0]<troughs[0]:
        pf=1
    if peaks[-1]>troughs[-1]:
        pl=1

    peaks2=[]
    troughs2=[]
    
    if pf: # if the record starts with a peak
        peaks2.append([idx for idx in np.arange(troughs[0]) if www[idx] == np.max(www[:troughs[0]])][0]) # re-find first real peak
        for idx,vvv in enumerate(peaks[:-1]):
            front = vvv
            back = peaks[idx+1]
            try:
                troughs2.append([idx for idx in np.arange(front,back) if www[idx] == np.min(www[front:back]) and www[idx] < 0][0]) # just uses list comprehension to find get the index of the troughs below zero
            except IndexError:
                continue
        for idx,vvv in enumerate(troughs2[:-1]):
            front = vvv
            back = troughs2[idx+1]
            try:
                peaks2.append([idx for idx in np.arange(front,back) if www[idx] == np.max(www[front:back]) and www[idx] > 0][0]) # same as before but with peaks
            except IndexError:
                continue        
        #find the last peak (removed as we searching inside the troughs that were inside the peaks)
        peaks2.append([idx for idx in peaks if idx > troughs2[-1] and www[idx] == np.max(www[[idx for idx in peaks if idx > troughs2[-1]]])][0])
        if not pl:# if the record ends with a trough
            troughs2.append([idx for idx in np.arange(peaks2[-1],len(www)) if www[idx] == np.min(www[peaks2[-1]:len(www)]) and www[idx] < 0][0])
    
    else: # if the record starts with a trough
        troughs2.append([idx for idx in np.arange(peaks[0]) if www[idx] == np.max(www[:peaks[0]])][0]) # re-find first real trough
        for idx,vvv in enumerate(troughs[:-1]):
            front = vvv
            back = troughs[idx+1]
            try:
                peaks2.append([idx for idx in np.arange(front,back) if www[idx] == np.max(www[front:back]) and www[idx] > 0][0]) # just uses list comprehension to find get the index of the troughs below zero
            except IndexError:
                continue
        for idx,vvv in enumerate(peaks2[:-1]):
            front = vvv
            back = peaks2[idx+1]
            try:
                troughs2.append([idx for idx in np.arange(front,back) if www[idx] == np.min(www[front:back]) and www[idx] < 0][0]) # same as before but with peaks
            except IndexError: 
                continue
        #find the last peak (removed as we searching inside the troughs that were inside the peaks)
        troughs2.append([idx for idx in troughs if idx > peaks2[-1] and www[idx] == np.min(www[[idx for idx in troughs if idx > peaks2[-1]]])][0])
        if pl:# if the record ends with a peak
            peaks2.append([idx for idx in np.arange(troughs2[-1],len(www)) if www[idx] == np.max(www[troughs2[-1]:len(www)]) and www[idx] > 0][0])

    if pf: # starts with a peak
        if pl: # ends with a peak
            p2t = www[peaks2[:-1]] - www[troughs2]
            t2p = www[peaks2[1:]] - www[troughs2]
        else: # ends with a tough
            p2t = www[peaks2] - www[troughs2]
            t2p = www[peaks2[1:]] - www[troughs2[:-1]]
    else: # starts with a tough
        if pl: # ends with a peak
            p2t = www[peaks2[:-1]] - www[troughs2[1:]]
            t2p = www[peaks2] - www[troughs2]
        else: # ends with a trough
            p2t = www[peaks2] - www[troughs2[1:]]
            t2p = www[peaks2] - www[troughs2[:-1]]
            
    return t2p, p2t