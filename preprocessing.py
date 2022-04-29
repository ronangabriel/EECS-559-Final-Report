import math
import numpy as np

# delete all items that do not contain the correct number of data points
def deleteInvalid(data, trueLen):
    invalidId = []
    for id in data:
        if len(data[id][1]) < trueLen:
            invalidId.append(id)
    
    for id in invalidId:
        data.pop(id)

    return data

# delete all invalid data points (both high and low prices are None) at the beginning of a series
def clipFrontData(data, trueLen):
    firstId = list(data.keys())[0]
    maxClip = 0
    for id in data:
        tempMax = 0
        while len(data[id][1]) > 0 and not (data[id][1][0]['avgHighPrice'] or data[id][1][0]['avgLowPrice']):
            data[id][1].pop(0)
            tempMax += 1
            if (tempMax > maxClip):
                maxClip = tempMax

    # clip all data to be the same length
    for id in data:
        while len(data[id][1]) > trueLen - maxClip:
            data[id][1].pop(0)
    
    return data
    
        
# fill empty data points (gaps/None vals) with the last value seen
def fillData(data):
    for id in data:
        avgHighPricePast = None
        avgLowPricePast = None
        highPriceVolumePast = None
        lowPriceVolumePast = None

        for point in data[id][1]:
            avgHighPrice = point['avgHighPrice']
            avgLowPrice = point['avgLowPrice']
            highPriceVolume = point['highPriceVolume']
            lowPriceVolume = point['lowPriceVolume']
            
            if (avgHighPrice and avgHighPrice > 0) or (avgLowPrice and avgLowPrice > 0):
                avgHighPricePast = avgHighPrice
                avgLowPricePast = avgLowPrice
                highPriceVolumePast = highPriceVolume
                lowPriceVolumePast = lowPriceVolume
            else:
                point['avgHighPrice'] = avgHighPricePast
                point['avgLowPrice'] = avgLowPricePast
                point['highPriceVolume'] = highPriceVolumePast
                point['lowPriceVolume'] = lowPriceVolumePast

    return data


# calculate the average price based on high and low prices
def addAvgData(data):
    for id in data:
        for point in data[id][1]:
            avgHighPrice = point['avgHighPrice']
            avgLowPrice = point['avgLowPrice']
            highPriceVolume = point['highPriceVolume']
            lowPriceVolume = point['lowPriceVolume']

            if avgHighPrice and avgLowPrice and highPriceVolume and lowPriceVolume and highPriceVolume > 0 and lowPriceVolume > 0:
                point['avgPrice'] = (avgHighPrice * highPriceVolume + avgLowPrice * highPriceVolume) / (highPriceVolume + lowPriceVolume)
            elif avgHighPrice and avgLowPrice and not highPriceVolume and not lowPriceVolume:
                point['avgPrice'] = (avgHighPrice + avgLowPrice) / 2
            elif avgHighPrice:
                point['avgPrice'] = avgHighPrice
            elif avgLowPrice:
                point['avgPrice'] = avgLowPrice

    return data

# create 2D numpy array from dictionary
def vectorize(data):
    firstId = list(data.keys())[0]
    vec = np.zeros((len(data), len(data[firstId][1])))

    i = 0
    for id in data:
        j = 0
        for point in data[id][1]:
            vec[i][j] = point['avgPrice']
            j += 1
        i += 1

    return vec

# min-max(x) = (x - min(x)) / (max(x) - min(x))
def normalize(data):
    data = np.divide((data - np.amin(data, axis=1, keepdims=True)), (np.amax(data, axis=1, keepdims=True) - np.amin(data, axis=1, keepdims=True)))
    return data

# if there is a clear error (price < 1% of max), use the previous data point if valid
def deleteErrors(data):
    M = np.shape(data)[0]
    N = np.shape(data)[1]

    for m in range(M):
        avg = np.mean(data[m, :])
        for n in range(1, N):
            if data[m][n] <= 0.02 * avg and data[m][n - 1] > 0.02 * avg:
                data[m][n] = data[m][n - 1]

    return data
    
