import mysql.connector as sql
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import fileWork
import random



def graphIndivid(dictData, nameInfo, directory):
       """
       Graphs one metallicity type with all of its data
       """
       
       IDS = dictData.keys()

       #Graph labels should be: "Metallicity vs. radius for metallicity type from data set"
       #[dr{numTable}, {metalType}, {galaxiesUsed}, {percentile}]
       plt.title(f"Metallicity vs. Radius for {nameInfo[1]} from {nameInfo[0]} ({nameInfo[3]} galaxies)")
       plt.xlabel("Radius, from r_eff_nsa, units of sersic half light radii")
       plt.ylabel("Metallicity")

       for ID in IDS:
              if ID != "Unused galaxies":

                     #pull out the 8 pieces of data for the galaxy
                     fourData = dictData.get(ID)
                     
                     #Saved as: fourData = (metal, radii, BFslope, BFintercept, pLower, pUpper, minRadius, maxRadius, vertLowerBound, vertUpperBound)
                     #MUST CHANGE BELOW INDICES WHEN NEW DATA GOTTEN
                     graphingPoints = getPoints(fourData[0], fourData[1], fourData[4], fourData[5], 7, 10)
                     #My test with imposed vertical limits that ARENT WORKING UGHHHHH graphingPoints = getPoints(fourData[2], fourData[3], fourData[4], fourData[5], 7, 10)

                     #changing colors slightly
                     colTuple = (.5 + (random.randrange(0, 50, 1) - 25)/100, .5 + (random.randrange(0, 50, 1) - 25)/100, .5 + (random.randrange(0, 50, 1) - 25)/100)

                     xData = graphingPoints[0]
                     yData = graphingPoints[1]

                     plt.plot(xData, yData, color = colTuple, alpha = .3)

       plt.savefig(f"{directory}/Graph of {nameInfo[1]} from {nameInfo[0]}")
       plt.close()





def graphCompar(firDictData, secDictData, firNameInfo, secNameInfo, directory):
       """
       Graphs a comparison of a metallicity type from dr15 and dr17
       """


       plt.title(f"Avg Metallicity vs. Avg Radius for {firNameInfo[1]} from {firNameInfo[0]} and {secNameInfo[1]} from {secNameInfo[0]}")
       plt.xlabel("Radius, from r_eff_nsa, units of sersic half light radii")
       plt.ylabel("Metallicity")

       firAver = getAverages(firDictData)
       secAver = getAverages(secDictData)

       print(firAver, secAver)

       #graphing the first data set
       graphingPoints = getPoints(firAver[0], firAver[1], firAver[2], firAver[3], 7, 10)

       xData = graphingPoints[0]
       yData = graphingPoints[1]

       print(xData, yData)

       plt.plot(xData, yData, color = "red", alpha = .8)

       #same code but for other data set
       graphingPoints = getPoints(secAver[0], secAver[1], secAver[2], secAver[3], 7, 10)

       xData = graphingPoints[0]
       yData = graphingPoints[1]

       print(xData, yData)

       plt.plot(xData, yData, color = "blue", alpha = .8)

       plt.savefig(f"{directory}/Comparison of {firNameInfo[1]} between dr15 & dr17")
       plt.close()





def getPoints(slope, intercept, xlow, xhigh, ylow, yhigh):
       """
       Given parameters, return 2 lists of 2 points so that a line can be graphed
       """

       xData = [float(xlow), float(xhigh)]
       yData = []
       for value in xData:
              yData.append(float(intercept) + float(slope) * float(value))

       if yData[0] > yhigh:
              yData[0] = float(yhigh)
              xData[0] = (float(yhigh) - float(intercept)) / float(slope)
       if yData[1] > yhigh:
              yData[1] = float(yhigh)
              xData[1] = (float(yhigh) - float(intercept)) / float(slope)

       if yData[1] < ylow:
              yData[1] = float(ylow)
              xData[1] = (float(ylow) - float(intercept)) / float(slope)
       if yData[0] < ylow:
              yData[0] = float(ylow)
              yData[0] = (float(ylow) - float(intercept)) / float(slope)
       
       return xData, yData




def getAverages(data):
       """
       Returns [slopeAVG, interceptAVG, minRadAVG, maxRadAVG, lowVertAVG, uppVertAVG]
       """

       IDS = data.keys()

       slopes = []
       intercepts = []
       minRadii = []
       maxRadii = []
       lowerVerts = []
       upperVerts = []

       for ID in IDS:
              if ID != "Unused galaxies":

                     #pull out the 10 pieces of data for the galaxy
                     #(metal, radii, BFslope, BFintercept, pLower, pUpper, minRadius, maxRadius, vertLowerBound, vertUpperBound)
                     tenDatas = data.get(ID)

                     slopes.append(tenDatas[2])
                     intercepts.append(tenDatas[3])
                     minRadii.append(tenDatas[6])
                     maxRadii.append(tenDatas[7])
                     #lowerVerts.append(tenDatas[8])
                     #upperVerts.append(tenDatas[9])

       print(intercepts)

       slopeAVG = sum(slopes) / len(slopes)
       interceptAVG = sum(intercepts) / len(intercepts)
       minRadAVG = sum(minRadii) / len(minRadii)
       maxRadAVG = sum(maxRadii) / len(maxRadii)
       #lowVertAVG = sum(lowerVerts) / len(lowerVerts)
       #uppVertAVG = sum(upperVerts) / len(upperVerts)

       return [slopeAVG, interceptAVG, minRadAVG, maxRadAVG]#, lowVertAVG, uppVertAVG]



def main():
       print(datetime.datetime.now().time())
       print()

       #access the data
       fileNames = fileWork.getFileNames("dr15_data", "dr17_data")

       #Removes the "<DirEntry '.DS_Store'>" that is only popping up at the start of the dr15 data for some reason
       fileNames[0] = fileNames[0][1:]
       
       for i in range(1, len(fileNames[0])):
              drFifData = pickle.load(open(fileNames[0][i], 'rb'))
              drSevData = pickle.load(open(fileNames[1][i], 'rb'))

              #[dr{numTable}, {metalType}, {galaxiesUsed}, {percentile}]
              listFifInfo = fileWork.getTheInfo(fileNames[0][i])
              listSevInfo = fileWork.getTheInfo(fileNames[1][i])

              #Make new directory
              directory = f"Graphs for {listFifInfo[1]}"
              if not os.path.exists(f"{directory}"):
                     os.makedirs(f"{directory}")

              #graphIndivid(drFifData, listFifInfo, directory)
              #graphIndivid(drSevData, listSevInfo, directory)
              graphCompar(drFifData, drSevData, listFifInfo, listSevInfo, directory)

              exit()

              print(datetime.datetime.now().time())
              print()


       exit()


if __name__ == "__main__":
       main()