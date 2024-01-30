import mysql.connector as sql
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle


def main():
    print(datetime.datetime.now().time())
    print()
    
    vertical_limits = {}
    
    #Iterate through 15, then 17
    tableNums = ["17", "15"] #either 15 or 17
    for numTable in tableNums:
    
        #Iterate through all metallicity types
        metalTypes = ["Z94_smc", "M91_smc", "KK04_smc", 'KE08_smc', 'D16_smc', 'PP04_O3N2_smc', 'PP04_N2_smc', "M13_N2_smc", "M13_O3N2_smc", "C17_O3N2_smc", "C17_N2_smc", "Z94_mw", "M91_mw", "KK04_mw", "KE08_mw", "D16_mw", "PP04_O3N2_mw", "PP04_N2_mw", "M13_N2_mw", "M13_O3N2_mw", "C17_O3N2_mw", "C17_N2_mw"]

        for metalType in metalTypes:

                db = sql.connect(host="localhost", user="colvin", password="c0LV1n", database="sdss")
                c = db.cursor()

                #Get all objids where there are at least 3 metallicites, currently the limit has been removed
                c.execute(f'''select distinct(objid) from dr{numTable}_metallicities where {metalType} is not NULL;''')
                
                galaxiesIDS = c.fetchall()
                db.close()

                print()
                print(f"Now on {metalType} from dr{numTable}.")
                print(datetime.datetime.now().time())
                print()

                galNum = 0

                #iterate through all galaxies
                for id in galaxiesIDS:
                    
                    db = sql.connect(host="localhost", user="colvin", password="c0LV1n", database="sdss")
                    c = db.cursor()

                    #Get the max and min values from the metallicity table
                    c.execute(f'''select max({metalType}) from  dr{numTable}_metallicities where objid='{id[0]}';''')
                    max_metal = c.fetchall()

                    c.execute(f'''select min({metalType}) from  dr{numTable}_metallicities where objid='{id[0]}';''')
                    min_metal = c.fetchall()
                    
                    db.close()
                    
                    
                    key = f"{numTable} {metalType} {id}"
                    vertical_limits[key] = [max_metal, min_metal]

                    galNum += 1
                    print(galNum)

    
    pickle.dump(vertical_limits, open(f"All vertical maxes and mins (to set limits)", 'wb'))

    exit()





if __name__ == "__main__":
    main()