def hycomlinesplit(lines):
    import numpy as np
    # This is to be used in hycom_hindcast (1 nd 2) to deal with data parsing based on Hycom output
    #first get the indexes of the data being provided
    header = lines[0]
    headerparts = header.split('[')
    arrayshape=[]
    for idxpart in headerparts[1:]:
        arrayshape.append(int(idxpart[:-1]))
    currentarray = np.empty(np.array(arrayshape)) ## make an array to hold the values
    for line in lines[1:]: # for each line except the header
        parts = line.split(',') # grab the indexes
        idxestr = parts[0].split('[') 
        idxlist=[]
        for idx in idxestr[1:]:
            idxlist.append(int(idx[:-1])) # get the indexes as ints
        values = [int(value) for value in parts[1:]] # get the values into 
        currentarray[idxlist[0],idxlist[1],idxlist[2],:] = values[:]

    currentarray = currentarray.ravel() # to deal with some annoyances

    for idx,val in enumerate(currentarray):
        if val == -30000:
            currentarray[idx]=np.nan # remove bad data
    currentarray = currentarray * 0.001 # account for format - change to m/s
    currentarray = currentarray.reshape(arrayshape[0],arrayshape[1],arrayshape[2],arrayshape[3])

    return currentarray