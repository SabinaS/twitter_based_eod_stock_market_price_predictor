#!/usr/bin/env python
import json 
import csv
from dateutil.parser import parse

def getEnglishEntries( filename ):
    ''' Method for prasing a file for English entries ''' 
    englishEntries = []
    with open( filename ) as jData:
        for line in jData:
            jLine = json.loads( line )
            if u'user' in jLine:
                if jLine[ u'user' ][ u'lang' ] == 'en':
                    englishEntries.append( jLine )
            else:
                continue
    jData.close()
    print '~~~~~~~~~~~~~ en {}'.format( len(englishEntries))
    return englishEntries

def getRelevantEntries( companyName, listOfEntries ):
    ''' Method that reads in a company name and a pre-filtered list of 
        dicts and further filters the list to only include dicts
        that have the company name in the text '''
    relevantEntries = []
    for entry in listOfEntries:
        if u'text' in entry and u'entities' in entry:
            if companyName in entry[ u'text' ] or companyName in entry[ u'entities' ]:
                relevantEntries.append( entry )
            else:
                continue
        else:
            continue
    print '~~~~~~~~~~~~~~~~~~~~~ rel {}'.format( len( relevantEntries) )
    return relevantEntries

def getDateAndText( listOfEntries ):
    parsedEntries = []
    for entry in listOfEntries:
        if u'user' in entry:
            tempDict = {}
            datetime = entry[ u'created_at' ]
	    datetimeObj = parse( datetime )
	    day = str( datetimeObj.day ) if len( str( datetimeObj.day ) )==2 else '0'+str( datetimeObj.day )
	    month = str( datetimeObj.month ) if len( str( datetimeObj.month ) )==2 else '0'+str( datetimeObj.month )
            year = str( datetimeObj.year )[ 2: ]
            formattedDate = month+'_'+day+'_'+year
            tempDict[ u'created_at' ] = formattedDate
            tempDict[ u'text' ] = entry[ u'text' ]
            parsedEntries.append( tempDict )
        else:
            continue
    print '~~~~~~~~~~~~~~~~ par {}'.format( len( parsedEntries ) )
    return parsedEntries


def createCSV( companyName, listOfEntries ):
    print '~~~~~~~~~~~~~ cre {}'.format( len( listOfEntries ) )
    if listOfEntries:
    	keys = listOfEntries[ 0 ].keys()
    	with open( companyName+'.csv', 'a+' ) as outputCSV:
            dictWriter = csv.DictWriter( outputCSV, keys )
            #dictWriter.writeheader()
            dictWriter.writerows( listOfEntries )    

def writeOutputJSON( companyName, listOfEntries) :
    ''' Method for taking in a list of entries and writing an output json
        file containing those entries '''
    strListOfEntries = [ str( entry ) for entry in listOfEntries ]
    with open( companyName+'.json', 'a+' ) as en:
        en.write( '\n'.join( strListOfEntries ) )
    en.close()

if __name__ == "__main__":
    import sys
    englishEntries = getEnglishEntries( sys.argv[ 1 ] ) 
    relevantEntries = getRelevantEntries( sys.argv[ 2 ], englishEntries )
    parsedEntries = getDateAndText( relevantEntries )
    createCSV( sys.argv[ 2 ], parsedEntries )
    #writeOutputJSON( sys.argv[ 2 ], relevantEntries )
