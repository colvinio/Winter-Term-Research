import mysql.connector as sql
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle
import fileWork
import singleGalMathCheck





def main():

    #access the data
    fileNames = fileWork.getFileNames("/Users/hina/Documents/Colvin's_code/dr15_data", "/Users/hina/Documents/Colvin's_code/dr17_data")

    for i in range(1, len(fileNames[0])):

        singleGalMathCheck.single_gal_math(fileNames[1][i])
        singleGalMathCheck.single_gal_math(fileNames[0][i])


        dr17Data = pickle.load(open(fileNames[1][i], 'rb'))
        dr15Data = pickle.load(open(fileNames[0][i], 'rb'))
        
        #FORMAT OF DICTIONARY: Key is objid, value is (BFslope, BFintercept, pLower, pUpper, minRadius, maxRadius)
        firstIDS = list(dr17Data.keys())[:-1]
        otherIDS = list(dr15Data.keys())[:-1]
        totalIDS = firstIDS
        for ID in otherIDS:
            if ID not in totalIDS:
                totalIDS.append(ID)

        slopesDif = []
        interceptsDif = []
        rangesDif = []
        origRangesDif = []
        inSevNotFif = 0
        inFifNotSev = 0
        unused = 0

        for ID in totalIDS:
            #check if key has values in both dictionaries
            if ID != "Unused galaxies":
                if dr17Data.get(ID) is not None and dr15Data.get(ID) is not None:
                    #Find the difference in the slopes, intercepts, range, and original range

                    # #Gotta test this shit
                    # print(dr17Data.get(ID), dr15Data.get(ID))
                    # exit()

                    slopesDif.append( float(dr17Data[ID][0]) - float(dr15Data[ID][0]) )
                    interceptsDif.append( float(dr17Data[ID][1]) - float(dr15Data[ID][1]) )
                    rangesDif.append( (float(dr17Data[ID][3]) - float(dr17Data[ID][2])) - (float(dr15Data[ID][3]) - float(dr15Data[ID][2])) )
                    origRangesDif.append( (float(dr17Data[ID][5]) - float(dr17Data[ID][4])) - (float(dr15Data[ID][5]) - float(dr15Data[ID][4])) )
                elif dr17Data.get(ID) is None and dr15Data.get(ID) is not None:
                    inFifNotSev += 1
                elif dr17Data.get(ID) is not None and dr15Data.get(ID) is None:
                    inSevNotFif += 1
                else:
                    unused += 1


        #Find the average of the differences
        slopeAvgDif = sum(slopesDif) / len(slopesDif)
        interceptAvgDif = sum(interceptsDif) / len(interceptsDif)
        rangeAvgDif = sum(rangesDif) / len(rangesDif)
        origRangesAvgDif = sum(origRangesDif) / len(origRangesDif)

        #Getting names so we can indicate which metallicity type we are talking about
        #[dr{numTable}, {metalType}, {galaxiesUsed}, {percentile}]
        listFifInfo = fileWork.getTheInfo(fileNames[0][i])
        listSevInfo = fileWork.getTheInfo(fileNames[1][i])

        print(f"""
        Between {listFifInfo[1]} from {listFifInfo[0]} and {listSevInfo[1]} from {listSevInfo[0]}:
        The average difference in the slope for galaxies is {slopeAvgDif}.
        The average difference in the intercept is {interceptAvgDif}.
        The average difference in the range after the percentile cut is {rangeAvgDif}.
        The average difference in the original ranges is {origRangesAvgDif}.
        There were {inSevNotFif} galaxies that had enough values in dr17 but not dr15, and there were {inFifNotSev} with enough in dr15 but not dr17.
        Something went wrong {unused} times.
        """)




if __name__ == "__main__":
    main()