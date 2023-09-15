def keysort(filepath):
    if ('direction' in str(filepath)) and ('miros_' not in str(filepath)):
        sort = 1 # standard directions, keys are [0])Datetime and [1:])Depths
    elif ('speed' in str(filepath)):
        sort = 2 # current speeds, keys are [0])Datetime and [1:])Depths
    elif ('direction' in str(filepath)) and ('miros_' in str(filepath)):
        sort = 3 # Wave Directions keys are ['DateTime', 'Dp', 'Dm', 'Dp1', 'Dm1', 'Dp2', 'Dm2']
    elif ('height' in str(filepath)):
        sort = 4 # Miros Wave Heights, keys are ['DateTime', 'Hm0', 'Hmax']
    elif ('periods' in str(filepath)):
        sort = 5 # miros wave periods , keys are ['DateTime', 'Tp', 'Tmax', 'Tp1', 'Tp2']
    else:
        sort = 0 # did not recognize the naming convention
        
    return sort
