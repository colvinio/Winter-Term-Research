import mysql.connector as sql
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle


def main():
    print(datetime.datetime.now().time())
    print()

    #Choosing radius type
    radiusType = "r_eff_nsa"
    
    #Iterate through data sets
    tableNums = ["17", "15"] #either 15 or 17
    for numTable in tableNums:
    
        #Iterate through all metallicity types
        metalTypes = ["Z94_smc", "M91_smc", "KK04_smc", 'KE08_smc', 'D16_smc', 'PP04_O3N2_smc', 'PP04_N2_smc', "M13_N2_smc", "M13_O3N2_smc", "C17_O3N2_smc", "C17_N2_smc", "Z94_mw", "M91_mw", "KK04_mw", "KE08_mw", "D16_mw", "PP04_O3N2_mw", "PP04_N2_mw", "M13_N2_mw", "M13_O3N2_mw", "C17_O3N2_mw", "C17_N2_mw"]
        metNumThru = 0
        for metalType in metalTypes:

            #Resetting universe data dictionary every time
            universe_data = {}

            #List of galaxies that have either 1 or 2 metallicity points
            unusedGalaxies = []

            db = sql.connect(host="ip-******.main.oberlin.edu", user="******", password="******", database="****")
            c = db.cursor()

            #Get all objids where there are at least 3 metallicites, currently the limit has been removed
            c.execute(f'''select distinct(objid) from dr{numTable}_metallicities where {metalType} is not NULL;''')
            
            galaxiesIDS = c.fetchall()
            db.close()

            totalNum = len(galaxiesIDS)
            numSoFar = 0

            print(datetime.datetime.now().time())
            print(f"Objids pulled for {metalType} from dr{numTable}. {metNumThru}/{len(metalTypes)} thru table.")
            print()

            galaxiesUsed = 0

            for galaxyID in galaxiesIDS:
                
                useID = galaxyID[0]

                db = sql.connect(host="ip-******.main.oberlin.edu", user="******", password="******", database="****")
                c = db.cursor()

                #"""
                #Gets metallicities and radii, no edits
                c.execute(f'''select m.{metalType}, r.{radiusType} from dr{numTable}_metallicities m, dr{numTable}_spaxels_uber r where m.objid='{useID}' and m.{metalType} is not NULL and m.spaxid=r.spaxID;''')
                #"""
                
                # #Same as above, but without any points where the radius is longer than 3 
                # c.execute(f'''select dr17_metallicities.D16_smc, dr17_spaxels_uber.r_eff_nsa from dr17_metallicities, dr17_spaxels_uber where dr17_metallicities.objid={useID} and dr17_metallicities.D16_smc is not NULL and dr17_metallicities.spaxid=dr17_spaxels_uber.spaxID and dr17_spaxels_uber.r_eff_nsa <= 3;''')

                rows = c.fetchall()
                db.close()

                #Here we are splitting the arraw into two 
                values = np.asarray(rows)
                metal = values[:,0].astype(float)
                radii = values[:, 1].astype(float)

                maxRadius = max(radii)
                minRadius = min(radii)
                
                #percentile cut, only take the middle whatever percent
                percentile = 95 #give full percent
                if len(metal) >= 20:
                    lower_bound = (100 - percentile) / 2
                    upper_bound = (100 - percentile) / 2 + percentile
                    pLower = np.percentile(radii, lower_bound)
                    pUpper = np.percentile(radii, upper_bound)
                    #using a mask to do this
                    mask = (radii >= pLower) & (radii <= pUpper)
                    radii, metal = radii[mask], metal[mask]
                else:
                    pLower = minRadius
                    pUpper = maxRadius

                vertUpperBound = max(metal)
                vertLowerBound = min(metal)

                if len(metal) > 2:
                    #returns the slope then the intercept in an array
                    slopeAndIntercept = np.polyfit(radii, metal, 1)
                    BFslope = slopeAndIntercept[0]
                    BFintercept = slopeAndIntercept[1]
                    
                    #STORE GALAXYID AND 4 (+ 4) OTHER PIECES OF DATA IN A FILE
                    universe_data[useID] = (metal, radii, BFslope, BFintercept, pLower, pUpper, minRadius, maxRadius, vertLowerBound, vertUpperBound)

                    galaxiesUsed += 1
                    numSoFar += 1
                    print(datetime.datetime.now().time())
                    print(f"Galaxy data stored. {numSoFar} galaxies out of {totalNum} done for {metalType}.")
                    print(f"{metNumThru}/{len(metalTypes)} metallicity types thru dr{numTable}.")
                    print()
                
                else:
                    print(datetime.datetime.now().time())
                    unusedGalaxies.append(useID)
                    numSoFar += 1
                    print(f"{numSoFar} galaxies out of {totalNum} done for {metalType}.")
                    print(f"{metNumThru}/{len(metalTypes)} metallicity types thru dr{numTable}.")
                    print()

            #SAVE THE FILE
            pickle.dump(universe_data, open(f"dr{numTable} {metalType}, {galaxiesUsed} galaxies, {percentile} percentile.pkl", 'wb'))

            metNumThru += 1
            print(datetime.datetime.now().time())

    exit()





if __name__ == "__main__":
    main()