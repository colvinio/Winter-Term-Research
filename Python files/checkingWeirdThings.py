
#universe_data[useID] = (BFslope, BFintercept, pLower, pUpper, minRadius, maxRadius, vertLowerBound, vertUpperBound)
#f'''select distinct(objid) from dr{numTable}_metallicities where {metalType} is not NULL;'''
#'''select m.{metalType}, r.{radiusType} from dr{numTable}_metallicities m, dr{numTable}_spaxels_uber r where m.objid='{useID}' and m.{metalType} is not NULL and m.spaxid=r.spaxID;'''


import mysql.connector as sql






def main():
    db = sql.connect(host="localhost", user="colvin", password="c0LV1n", database="sdss")
    c = db.cursor()

    c.execute(f''';''')

    galaxiesIDS = c.fetchall()
    db.close()



if __name__ == "__main__":
    main()