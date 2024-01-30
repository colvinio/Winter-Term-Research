"""
This is were all functions related to accessing/editing files are located
"""
import os
import numpy as np


def getFileNames(directionOne, directionTwo):
    """
    Returns a list w/ 2 lists inside, one of the 22 dr15 file names and one of the 22 dr17 file names. Should be alphabetized, so files should line up appropriately.
    """

    drFifNames = []
    drSevNames = []

    for file in os.scandir(directionOne):
        drFifNames.append(file)

    for file in os.scandir(directionTwo):
        drSevNames.append(file)

    # sort_list(drFifNames)
    # sort_list(drSevNames)

    drFifNames = sorted(drFifNames, key=lambda entry: entry.name)
    drSevNames = sorted(drSevNames, key=lambda entry: entry.name)

    return [drFifNames, drSevNames]



    
def getTheInfo(fileName):
    """
    Takes name of the form <DirEntry 'dr17 D16_smc, 4963 galaxies, 95 percentile.pkl'>
    Returns ['dr{numTable}', '{metalType}', '{galaxiesUsed}', '{percentile}']
    """

    parts = str(fileName).rsplit()
    return [parts[1][1:], parts[2][:-1], parts[3], parts[5]]



def sort_list(list):
    """
    Take in a list where the arguments in the list are of the type <DirEntry 'dr17 D16_smc, 4963 galaxies, 95 percentile.pkl'>
    """

    list_copy = list

    for i in range(len(list_copy)):
        list_copy[i] = list_copy[i][10:-1]


    print(list_copy)

    indices = np.argsort(list_copy)
    list = [list[i] for i in indices]