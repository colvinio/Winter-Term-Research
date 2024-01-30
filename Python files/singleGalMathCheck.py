import mysql.connector as sql
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle
import fileWork



def single_gal_math(file_name):
    #access the data
    dr17Data = pickle.load(open(file_name, 'rb'))

    #FORMAT OF DICTIONARY: Key is objid, value is (BFslope, BFintercept, pLower, pUpper, minRadius, maxRadius)

    data = list(dr17Data.keys())
    firstIDS = data[:-1]

    slopes = []
    intercepts = []
    ranges = []
    origRanges = []

    for ID in firstIDS:
            #Find the difference in the slopes, intercepts, range, and original range
        slopes.append( float(dr17Data[ID][0]) )
        intercepts.append( float(dr17Data[ID][1]) )
        ranges.append( float(dr17Data[ID][3]) - float(dr17Data[ID][2]) )
        origRanges.append( float(dr17Data[ID][5]) - float(dr17Data[ID][4]) )

    #Find the average of the differences
    slopeAvg = sum(slopes) / len(slopes)
    interceptAvg = sum(intercepts) / len(intercepts)
    rangeAvg = sum(ranges) / len(ranges)
    origRangesAvg = sum(origRanges) / len(origRanges)

    list_info = fileWork.getTheInfo(file_name)
    table = list_info[0]
    metal_type = list_info[1]

    print(f"""
    For {metal_type} from {table}:
    The average  slope for galaxies is {slopeAvg}.
    The average intercept is {interceptAvg}.
    The average range after the percentile cut is {rangeAvg}.
    The average original ranges is {origRangesAvg}.
    """)

    return slopeAvg, interceptAvg, rangeAvg, origRangesAvg



if __name__ == "__main__":
    single_gal_math("dr15 C17_N2_smc, 2528 galaxies, 95 percentile.pkl")
    single_gal_math("dr17 C17_N2_smc, 4980 galaxies, 95 percentile.pkl")