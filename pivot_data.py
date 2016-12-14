#!/usr/bin/env python
import csv

def pivotCSVFile( fileName ):
    # Temp dictionary to store values
    pivotData = {}
    # Open the file and read the contents
    # Add texts for same dates to a list
    with open( fileName ) as inFile:
        readr = csv.reader( inFile )
        for row in readr:
            text = row[ 0 ]
            date = row[1 ]
            if date in pivotData:
                pivotData[ date ].append( text )
            else:
                pivotData[ date ] = [ text ]
    inFile.close()
    # Convert the list of values to comma seperated string
    for k,v in pivotData.iteritems():
        strValues = ",".join( v )
        pivotData[ k ] = strValues
    # Write back the dictionary as a csv
    with open( fileName[:-4 ]+'_pivot.csv', 'a+' ) as outFile:
        w = csv.DictWriter( outFile, pivotData.keys() )
        w.writerow( pivotData.items() )
    outFile.close()

if __name__ == "__main__":
    import sys
    pivotCSVFile( sys.argv[ 1 ] )
