from nbformat import write
import numpy as np
import json
import preprocessing as pp
import kerasCNN as kc

def main():
    data = {}
    trueLen = 300

    print("Reading data...")
    with open("time_series_data_6h_4-8-22.txt", 'r') as j:
        data = json.loads(j.read())

    #original = copy.deepcopy(data)

    print("Preprocessing data...")
    data = pp.deleteInvalid(data, trueLen)
    data = pp.clipFrontData(data, trueLen)
    data = pp.fillData(data)
    data = pp.addAvgData(data)
    dataVec = pp.vectorize(data)
    dataVec = pp.deleteErrors(dataVec)
    dataVec = pp.normalize(dataVec)

    M = np.shape(dataVec)[0]
    N = np.shape(dataVec)[1]

    kc.singleFeature(dataVec)

if __name__== "__main__":
    main()