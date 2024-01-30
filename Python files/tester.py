import fileWork
import pickle
import mysql.connector as sql
import numpy


dataDict = pickle.load(open('dr17_data/dr17 KE08_mw, 4921 galaxies, 95 percentile.pkl', 'rb'))

largest = 0
second = 0
third = 0
fourth = 0
itsID = None
otherID = None
anotherid = None 
finalID = None

for galaxy in dataDict:
    if dataDict[galaxy][3] > largest:
        largest = dataDict[galaxy][3]
        itsID = galaxy
    elif dataDict[galaxy][3] > second:
        second = dataDict[galaxy][3]
        otherID = galaxy
    elif dataDict[galaxy][3] > third:
        third = dataDict[galaxy][3]
        anotherid = galaxy
    elif dataDict[galaxy][3] > fourth:
        fourth = dataDict[galaxy][3]
        finalID = galaxy

print(itsID, largest)
print(otherID, second)
print(anotherid, third)
print(finalID, fourth)
print(dataDict[itsID])
print(dataDict[otherID])
print(dataDict[anotherid])
print(dataDict[finalID])






















# db = sql.connect(host="localhost", user="colvin", password="c0LV1n", database="sdss")
# c = db.cursor()
# c.execute(f'''select dr17_metallicities.KE08_mw, dr17_spaxels_uber.r_eff_nsa from dr17_metallicities, dr17_spaxels_uber where dr17_metallicities.objid=dr17_spaxels_uber.objID='588016878823014879' and dr17_metallicities.KE08_mw is not NULL limit 5;''')
# rows = c.fetchall()
# db.close()

# values=numpy.asarray(rows)
# spaxid=values[:, 1] #this slices the array, and gets the zeroth column for all rows. 
# metal=values[:,0].astype(float)